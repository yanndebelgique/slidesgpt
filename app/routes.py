import re
from threading import Thread
import glob
from flask import send_from_directory
from pdf2image import convert_from_path
from flask import Blueprint, render_template, request, redirect, url_for
from PyPDF2 import PdfReader
from PIL import Image
import os
import io


main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/pdfs')
def list_pdfs():
    pdfs = []
    print('getcwd', os.getcwd(), os.listdir(UPLOAD_FOLDER))
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith('.pdf'):
            pdfs.append(filename)
    print('pdfs', pdfs)
    return render_template('pdfs.html', pdfs=pdfs)


@main.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print('POST')
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        print('file name', file)
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            Thread(target=convert_pdf_to_jpeg, args=(filename,)).start()
            print('file saved')
            return redirect(url_for('main.index'))

    return render_template('upload.html')


def convert_pdf_to_jpeg(pdf_path):
    images = convert_from_path(pdf_path)
    pdf_name = os.path.basename(pdf_path).split('.')[0]
    output_folder = os.path.join('split_uploads', pdf_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, image in enumerate(images):
        jpeg_path = os.path.join(
            output_folder, f"{pdf_name}_page_{i + 1}.jpeg")
        image.save(jpeg_path, 'JPEG')


@main.route('/pdfs/<pdf_name>/view')
def pdf_name_view(pdf_name):
    print('pdf_name', pdf_name)
    return send_from_directory('../' + UPLOAD_FOLDER, pdf_name)


@main.route('/pdfs/<pdf_name>/split')
def split_view_pdf(pdf_name):
    pdf_name = pdf_name[:-4] if pdf_name.endswith('.pdf') else pdf_name
    img_folder = os.path.join('split_uploads', pdf_name)
    img_files = glob.glob(f"{img_folder}/*.jpeg")

    # Updated sorting logic
    def sort_key(filename):
        page_number = re.search(r'_page_(\d+)', filename)
        return int(page_number.group(1)) if page_number else 0

    img_files = sorted(img_files, key=sort_key)
    img_files = [os.path.basename(img) for img in img_files]

    return render_template('show_images.html', img_files=img_files, folder=img_folder)


@main.route('/split_uploads/<pdf_name>/<img_name>')
def serve_image(pdf_name, img_name):
    pdf_name = pdf_name[:-4] if pdf_name.endswith('.pdf') else pdf_name
    print('dddddd', pdf_name)
    print('image', img_name)
    return send_from_directory(os.path.join('..', 'split_uploads', pdf_name), img_name)

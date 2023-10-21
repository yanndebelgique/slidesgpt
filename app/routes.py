from flask import Blueprint, render_template, request, redirect, url_for
import os

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
            print('file saved')
            return redirect(url_for('main.index'))

    return render_template('upload.html')


@main.route('/pdfs/<pdf_name>')
def hello_pdf(pdf_name):
    return f'hello {pdf_name}'

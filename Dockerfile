# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install Poppler utilities
RUN apt-get update && apt-get install -y poppler-utils

# Working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Create directories to store uploads and split_uploaded files
RUN mkdir -p /app/uploads /app/split_uploaded

# Make ports 80 available to the world outside this container
EXPOSE 80

# Run your Flask app
CMD ["gunicorn", "-b", "0.0.0.0:80", "run:app"]


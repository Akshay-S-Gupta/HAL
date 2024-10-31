# HAL
This is a scaled-down demo version of the "On-Premise Digital Signature" project I worked on during my internship at the Helicopter division, IT Department, HAL Bengaluru.

# Onpremise document Digital Signature with QR Code

This project is a Flask web application that allows users to upload PDF and non-PDF documents, add a digital signature (including user details such as name, ID, IP Address, and timestamp), and generate a QR code with relevant information. The system converts various file formats (e.g., images, Word documents) to PDF and appends a signature page at the end of the document.

## Features

- Converts non-PDF files (DOCX, PNG, JPG) to PDF.
- Adds a signature page with user details (name, ID, IP Address, timestamp).
- Embed a QR code with the user's details for verification.
- Supports batch file uploads.
- Designed to run in a local environment or deploy on a server.

## File Structure

project_root/
├── app.py                      # Flask app entry point
├── sign_pdf.py                 # PDF signing logic
├── convert_to_pdf.py           # Conversion logic for non-PDF files
├── templates/                  # HTML template
│   ├── index.html              # HTML form for file upload and user input
├── static/                     # HTML static resources
│   ├── favicon.png             # Favicon for the web app
│   ├── BG.jpg                  # Background for the web app
├── original_files/             # Directory to store uploaded original files
├── signed_files/               # Directory to store signed PDF files
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation

## Instructions

1. Prerequisites:
    Python 3.6 or higher
    pip package manager

2. Install the required dependencies:
    python get-pip.py                                                           # Intsalling pip from /packages folder        
    pip install -r requirements.txt
    pip install --no-index --find-links=./packages -r requirements.txt          # To install on an offline system from the /packages folder.

3. Run the Flask application:
    python app.py

4. Access the app at `http://localhost:5000` to upload a PDF, provide user details, and get a signed PDF with a QR code.

## Requirements

- Flask
- PyPDF2
- reportLab
- Pillow
- qrcode
- docx2pdf
- pdf2image
- Werkzeug

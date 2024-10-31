from flask import Flask, render_template, request, jsonify
from sign_pdf import sign_pdf
from werkzeug.utils import secure_filename
import os
from PIL import Image
import docx2pdf

app = Flask(__name__)
UPLOAD_FOLDER = 'original_files/'
SIGNED_FOLDER = 'signed_files/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SIGNED_FOLDER'] = SIGNED_FOLDER

# Check wheater the directories exist.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SIGNED_FOLDER, exist_ok=True)

# Function to convert image files to PDF.
def convert_image_to_pdf(image_path):
    img = Image.open(image_path)
    pdf_path = os.path.splitext(image_path)[0] + '.pdf'
    img.save(pdf_path, 'PDF', resolution=100.0)
    return pdf_path

# Function to convert Word files to PDF.
def convert_docx_to_pdf(docx_path):
    pdf_path = os.path.splitext(docx_path)[0] + '.pdf'
    docx2pdf.convert(docx_path)
    return pdf_path

# Function to check file type and convert to PDF if necessary.
def handle_non_pdf_files(filepath):
    file_ext = os.path.splitext(filepath)[1].lower()
    if file_ext in ['.png', '.jpg', '.jpeg']:
        return convert_image_to_pdf(filepath)
    elif file_ext == '.docx':
        return convert_docx_to_pdf(filepath)
    else:
        return filepath                     # PDF & unsupported file type

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or len(request.files.getlist('file')) == 0:
        return jsonify({'error': 'No files provided'}), 400

    files = request.files.getlist('file')
    for file in files:
        if file.filename == '':
            continue

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Convert non-PDF files to PDF
            converted_pdf_path = handle_non_pdf_files(filepath)

            # Get user inputs
            user_name = request.form.get('name', '')
            user_id = request.form.get('id', '')

            # Path for signed PDF
            signed_pdf_filename = secure_filename(f"signed_{os.path.splitext(filename)[0]}.pdf")
            signed_pdf_path = os.path.join(app.config['SIGNED_FOLDER'], signed_pdf_filename)

            # Sign the PDF
            sign_pdf(converted_pdf_path, signed_pdf_path, user_name, user_id)

    return jsonify({'message': 'Digital signature was successful!'})

if __name__ == "__main__":
    app.run(debug=True)
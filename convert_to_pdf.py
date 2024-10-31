from fpdf import FPDF                               # Generate PDF files with pure PHP.
from docx import Document
from PIL import Image
import os

# Convert .docx file to PDF
def docx_to_pdf(input_path, output_path):
    doc = Document(input_path)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    for para in doc.paragraphs:
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 10, para.text)
    
    pdf.output(output_path)

# Convert image file (.jpg, .png, etc.) to PDF
def image_to_pdf(input_path, output_path):
    image = Image.open(input_path)
    pdf = image.convert('RGB')
    pdf.save(output_path)

# Convert .txt file to PDF
def txt_to_pdf(input_path, output_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    with open(input_path, "r") as file:
        for line in file:
            pdf.multi_cell(200, 10, line)
    
    pdf.output(output_path)

# Generic function to handle the conversion based on file extension
def convert_to_pdf(input_file, output_file):
    _, ext = os.path.splitext(input_file)                       # split input_file path into file name and extension.
    
    if ext == ".docx":
        docx_to_pdf(input_file, output_file)
    elif ext in [".jpg", ".jpeg", ".png"]:
        image_to_pdf(input_file, output_file)
    elif ext == ".txt":
        txt_to_pdf(input_file, output_file)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
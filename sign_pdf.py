from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import qrcode
import socket
import os

# Function to generate QR code
def generate_qr_code(data, qr_code_path):
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(qr_code_path)

# Function to create the signature overlay on a separate page
def create_signature_overlay(user_name, user_id, qr_code_path, overlay_pdf_path):
    c = canvas.Canvas(overlay_pdf_path, pagesize=letter)

    # Signature text with name & ID
    signature_text = f"Signed by: {user_name}\n\tID: {user_id}"

    # Draw the signature text
    c.drawString(200, 150, f"Signed by: {user_name}")
    c.drawString(200, 135, f"            ID: {user_id}")

    # Add the QR code
    c.drawImage(qr_code_path, 250, 35, 100, 100)

    # Save as a PDF
    c.save()

# Function to sign the PDF
def sign_pdf(input_pdf_path, output_pdf_path, user_name, user_id):
    # Paths for temporary files
    qr_code_path = "qr_code.png"                                        # Temporary QR code image
    overlay_pdf_path = "signature_overlay.pdf"                          # Temporary overlay PDF

    # Get IP address of the computer
    ip_address = socket.gethostbyname(socket.gethostname())

    # Generate QR code with user details
    # qr_data = f"{user_name}\nID: {user_id}\nIP: {ip_address}\nTime: {datetime.now().strftime('%d/%m/%Y %I:%M %p')}"                # Format: 27/10/2024 03:47 PM
    # qr_data = f"{user_name}\nID: {user_id}\nIP: {ip_address}\nTime: {datetime.now().strftime('%A, %B %d, %Y %H:%M:%S')}"           # Format: Sunday, October 27, 2024 15:47:12
    qr_data = f"{user_name}\nID: {user_id}\nIP: {ip_address}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"                  # Format: 2024-10-27 15:47:12
    generate_qr_code(qr_data, qr_code_path)

    # Create the signature overlay with text and QR code
    create_signature_overlay(user_name, user_id, qr_code_path, overlay_pdf_path)

    # Read the original PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Add all pages from the original PDF
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        writer.add_page(page)

    # Add the signature overlay page as the last page
    with open(overlay_pdf_path, "rb") as overlay_file:
        overlay_pdf = PdfReader(overlay_file)
        signature_page = overlay_pdf.pages[0]
        writer.add_page(signature_page)

    # Save the signed PDF
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

    # Clean up temporary files
    os.remove(qr_code_path)
    os.remove(overlay_pdf_path)
import os
import google.generativeai as genai
from flask import Flask, Blueprint, request, jsonify
from PIL import Image
import pytesseract
import io
import sys
import re

genai.__version__

# Configure the generative AI API key
genai.configure(api_key="AIzaSyB71LU4uET4YpYf5Acu9jEJViajNWdpW-0")

# Define the Blueprint for invoice processing
invoice_processing_bp = Blueprint('invoice_processing', __name__)

# OCR processing function
def perform_ocr(image_data):
    try:
        # Convert image data to a PIL Image object
        image = Image.open(io.BytesIO(image_data))
        
        # Perform OCR on the image
        ocr_text = pytesseract.image_to_string(image)
        
        return ocr_text
    except Exception as e:
        return str(e)

# Route for processing invoice
@invoice_processing_bp.route('/process-invoice-ocr', methods=['POST'])
def process_invoice():
    try:
        # Check if the request has files
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        # Get the uploaded file
        uploaded_file = request.files['file']

        # Check if the file is actually uploaded
        if uploaded_file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Perform OCR on the uploaded image
        ocr_text = perform_ocr(uploaded_file.read())

        print("OCR Text:", ocr_text)  # Debugging

        # Extract vendor name from OCR text
        vendor_name = re.search(r'(?<=po NO:)\s*([^\n]+)', ocr_text)
        vendor_name = vendor_name.group(1).strip() if vendor_name else None

        # Extract invoice number, invoice date, and invoice amount using regex
        invoice_number = re.search(r'(?<=po NO:)(.*?)[\s\d]*_.*?dt:(\d{2}\.\d{2}\.\d{4})', ocr_text)
        invoice_date = re.search(r'dt:(\d{2}\.\d{2}\.\d{4})', ocr_text)
        invoice_amount = re.search(r'Total\s*([\d.]+)', ocr_text)

        print("Vendor Name:", vendor_name)  # Debugging
        print("Invoice Number:", invoice_number)  # Debugging
        print("Invoice Date:", invoice_date)  # Debugging
        print("Invoice Amount:", invoice_amount)  # Debugging

        # Create JSON response for extracted information
        extracted_info = {
            "vendor_name": vendor_name,
            "invoice_number": invoice_number.group(1).strip() if invoice_number else None,
            "invoice_date": invoice_date.group(1) if invoice_date else None,
            "invoice_amount": invoice_amount.group(1) if invoice_amount else None
        }

        # Create JSON response with OCR text and extracted information
        response_data = {
            "success": True,
            "ocr_text": ocr_text,
            "extracted_info": extracted_info
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

# Create Flask app
app = Flask(__name__)

# Register blueprint
app.register_blueprint(invoice_processing_bp)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, jsonify, session, request
from flask_cors import CORS
from flask_session import Session
from app.config import ApplicationConfig
from app.models import db, User, UserRole, Invoice, Supplier, Buyer
from app.authentication import authentication_bp
from app.preprocessing import preprocessing_bp
from app.tesseractOCR import tesseract_bp
from app.paddleOCR import paddleocr_bp
from app.companyAPI import companyAPI_bp
from app.organizations import organizations_bp
from app.getData import getData_bp
from flask_bcrypt import Bcrypt
import logging
import time
# import pytesseract
from PIL import Image
import base64
import io
from app.invoice_processing import invoice_processing_bp



app = Flask(__name__)
app.config.from_object(ApplicationConfig)
app.config.update(ENV='development')
app.config['SESSION_SQLALCHEMY'] = db
app.config['CORS_HEADERS'] = 'Content-Type'

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

CORS(app, origins='http://localhost:3000', supports_credentials=True)

app.register_blueprint(authentication_bp)
app.register_blueprint(preprocessing_bp)
app.register_blueprint(tesseract_bp)
# app.register_blueprint(paddleocr_bp)
app.register_blueprint(companyAPI_bp)
app.register_blueprint(organizations_bp)
app.register_blueprint(getData_bp)
app.register_blueprint(invoice_processing_bp)

bcrypt = Bcrypt()
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()

    admin_user = User.query.filter_by(email='admin').first()
    if not admin_user:
        hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
        admin_user = User(email='admin', name='Admin', password=hashed_password)
        admin_user.role = UserRole.ADMIN
        db.session.add(admin_user)
        db.session.commit()

@app.route("/@me")
def get_current_user():
    try:
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        user = User.query.get(user_id)

        return jsonify({
            "name": user.name,
            "email": user.email,
            "role": user.role.value
        })
    except Exception as e:
        logger.error(f"Error in /@me route: {str(e)}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}),

@app.route("/edit-role", methods=["POST"])
def edit_role():
    try:
        role = request.json["role"]
        user_id = request.json["user_id"]

        user = User.query.get(user_id)
        user.role = UserRole[role]
        db.session.commit()

        return jsonify({"success": True}), 200
    except Exception as e:
        logger.error(f"Error in /edit-role route: {str(e)}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@app.route("/update-user", methods=["POST"])
def update_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(user_id)
    user.name = request.json["name"]
    user.email = request.json["email"]
    db.session.commit()

    return jsonify({"success": True}), 200

@app.route('/delete-invoice', methods=['DELETE'])
def delete_invoice():
    invoice_id = request.args.get('id', type=int)

    if not invoice_id:
        return jsonify({"error": "ID parameter is missing"}), 400

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404

    if invoice.supplier_id:
        supplier = Supplier.query.get(invoice.supplier_id)
        if supplier:
            db.session.delete(supplier)

    if invoice.buyer_id:
        buyer = Buyer.query.get(invoice.buyer_id)
        if buyer:
            db.session.delete(buyer)

    performance = invoice.performance

    if performance:
        db.session.delete(performance)

    db.session.delete(invoice)
    db.session.commit()

    return jsonify({"message": f"Invoice {invoice_id} has been deleted"}), 200

@app.route('/update-invoice', methods=['POST'])
def update_invoice():
    new_data = request.json["new_data"]
    invoice_id = new_data["id"]

    if not invoice_id:
        return jsonify({"error": "ID parameter is missing"}), 400

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404

    invoice.invoice_number = new_data.get("invoice_number", invoice.invoice_number)
    invoice.var_symbol = new_data.get("var_symbol", invoice.var_symbol)
    invoice.date_of_issue = new_data.get("date_of_issue", invoice.date_of_issue)
    invoice.due_date = new_data.get("due_date", invoice.due_date)
    invoice.delivery_date = new_data.get("delivery_date", invoice.delivery_date)
    invoice.payment_method = new_data.get("payment_method", invoice.payment_method)
    invoice.total_price = new_data.get("total_price", invoice.total_price)
    invoice.bank = new_data.get("bank", invoice.bank)
    invoice.swift = new_data.get("swift", invoice.swift)
    invoice.iban = new_data.get("iban", invoice.iban)

    supplier_data = new_data.get("supplier_data", {})
    if invoice.supplier:
        invoice.supplier.ico = supplier_data.get("ICO", invoice.supplier.ico)
        invoice.supplier.name = supplier_data.get("Name", invoice.supplier.name)
        invoice.supplier.address = supplier_data.get("Street", invoice.supplier.address)
        invoice.supplier.psc = supplier_data.get("PSC", invoice.supplier.psc)
        invoice.supplier.city = supplier_data.get("City", invoice.supplier.city)
        invoice.supplier.dic = supplier_data.get("DIC", invoice.supplier.dic)

    buyer_data = new_data.get("buyer_data", {})
    if invoice.buyer:
        invoice.buyer.ico = buyer_data.get("ICO", invoice.buyer.ico)
        invoice.buyer.name = buyer_data.get("Name", invoice.buyer.name)
        invoice.buyer.psc = buyer_data.get("PSC", invoice.buyer.psc)
        invoice.buyer.address = buyer_data.get("Street", invoice.buyer.address)
        invoice.buyer.city = buyer_data.get("City", invoice.buyer.city)
        invoice.buyer.dic = buyer_data.get("DIC", invoice.buyer.dic)

    db.session.commit()

    return jsonify({"message": f"Invoice has been updated"}), 200

# New route for OCR processing
@app.route('/upload-and-process', methods=['POST'])
def upload_and_process():
    try:
        # Check if file is present in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        # Get the uploaded file
        uploaded_file = request.files['file']

        # Perform preprocessing
        processed_image, preprocess_error = preprocess_image(uploaded_file)

        # Check if preprocessing was successful
        if processed_image is None:
            return jsonify({"error": preprocess_error}), 400

        # Perform OCR
        ocr_text = perform_ocr(processed_image)

        return jsonify({
            "success": True,
            "ocr_text": ocr_text
        }), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


import pytesseract
from PIL import Image

def generate_gemini_response(input_prompt, image_loc, question_prompts, output_file_path):
    # Perform OCR using Tesseract on the specified image location
    ocr_text = ""
    try:
        # Load the image
        image = Image.open(image_loc)

        # Perform OCR
        ocr_text = pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Error during OCR processing: {str(e)}")

    # Here you would typically extract relevant information from the OCR text
    # and format it as needed for further processing or storage
    # For simplicity, let's just return the OCR text for now
    return ocr_text

if __name__ == '__main__':
    app.debug = True
    app.run(port=3000)

from flask import Blueprint, request, jsonify
from services.pdf_service import PDFService

upload_controller = Blueprint('upload_controller', __name__)
pdf_service = PDFService(upload_folder='uploads/', allowed_extensions={'pdf'})

@upload_controller.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    file_path, error = pdf_service.save_file(file)
    if error:
        return jsonify({"error": error}), 400

    # Process the PDF file
    pdf_service.process_pdf(file_path)
    return jsonify({"message": "File successfully uploaded and processed"}), 200
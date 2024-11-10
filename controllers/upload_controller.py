import logging

from flask import Blueprint, request, jsonify


class UploadController:
    def __init__(self, pdf_service):
        self.pdf_service = pdf_service
        self.logger = logging.getLogger(__name__)
        self.blueprint = Blueprint('upload_controller', __name__)
        self.blueprint.add_url_rule('/upload', 'upload_file', self.upload_file, methods=['POST'])

    def upload_file(self):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        file_path, error = self.pdf_service.save_file(file)
        if error:
            self.logger.error(f"Error saving file: {error}")
            return jsonify({"error": error}), 400

        return jsonify({"message": "File successfully uploaded and processed"}), 200

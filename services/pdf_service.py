import os
from werkzeug.utils import secure_filename
from util.pdf_to_text import PDFTextConverter

class PDFService:
    def __init__(self, upload_folder, allowed_extensions):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def save_file(self, file):
        if file.filename == '':
            return None, "No selected file"
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(self.upload_folder, filename)
            file.save(file_path)
            return file_path, None
        else:
            return None, "Invalid file type"

    def process_pdf(self, file_path):
        converter = PDFTextConverter()
        converter.store_pdf_embeddings_in_chromadb(file_path)
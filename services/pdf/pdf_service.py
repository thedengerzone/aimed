# services/pdf_service.py
import logging
import os
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)


class PDFService:
  def __init__(self, converter, upload_folder=os.environ.get("UPLOAD_FOLDER"), allowed_extensions=os.environ.get("ALLOWED_EXTENSIONS")):
    self.upload_folder = upload_folder
    self.allowed_extensions = allowed_extensions
    self.converter = converter

  def allowed_file(self, filename):
    return '.' in filename and filename.rsplit('.', 1)[
      1].lower() in self.allowed_extensions

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

  def process_pdf(self, file_path, filename):
    self.converter.preprocess_file(file_path,filename)

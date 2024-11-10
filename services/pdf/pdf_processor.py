# pdf_processor.py
import logging
import os
import threading
import time

from services.pdf.pdf_service import PDFService

logger = logging.getLogger(__name__)


class PDFProcessor:
    def __init__(self, pdf_service: PDFService,
                 upload_folder=os.environ.get("UPLOAD_FOLDER"),
                 allowed_extensions=os.environ.get("ALLOWED_EXTENSIONS")):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions
        self.pdf_service = pdf_service
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.process_files)
        self.thread.start()

    def process_files(self):
        while not self.stop_event.is_set():
            for filename in os.listdir(self.upload_folder):
                file_path = os.path.join(self.upload_folder, filename)
                if os.path.isfile(file_path) and self.pdf_service.allowed_file(filename):
                    logger.info(f"Processing file: {filename}")
                    self.pdf_service.process_pdf(file_path, filename)
                    os.remove(file_path)  # Remove the file after processing
            time.sleep(10)

    def stop(self):
        self.stop_event.set()
        self.thread.join()

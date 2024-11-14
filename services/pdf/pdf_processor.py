import os
import threading
import time
import logging

from services.pdf.pdf_service import PDFService

logger = logging.getLogger(__name__)

def remove_file(file_path, retries=5, delay=15):
    """
    Try to remove a file, retrying a specified number of times with a delay
    if the file is being used by another process.
    """
    for attempt in range(retries):
        try:
            os.remove(file_path)
            logger.info(f"Successfully removed file: {file_path}")
            return True
        except PermissionError as e:
            logger.warning(f"Attempt {attempt + 1}: File is locked and cannot be removed: {file_path}")
            time.sleep(delay)  # Wait before trying again
    logger.error(f"Failed to remove file after {retries} attempts: {file_path}")
    return False

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
                    # Use the remove_file method to handle file removal with retries
                    remove_file(file_path)  # Remove the file after processing
            time.sleep(10)

    def stop(self):
        self.stop_event.set()
        self.thread.join()

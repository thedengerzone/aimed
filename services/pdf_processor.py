# pdf_processor.py
import os
import threading
import time
from services.pdf_service import PDFService

class PDFProcessor:
    def __init__(self, upload_folder, allowed_extensions):
        self.thread = None
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions
        self.pdf_service = PDFService(upload_folder, allowed_extensions)
        self.stop_event = threading.Event()

    def process_files(self):
        while not self.stop_event.is_set():
            for filename in os.listdir(self.upload_folder):
                file_path = os.path.join(self.upload_folder, filename)
                if os.path.isfile(file_path) and self.pdf_service.allowed_file(filename):
                    print(f"Processing file: {filename}")
                    self.pdf_service.process_pdf(file_path)
                    os.remove(file_path)  # Remove the file after processing
            time.sleep(60)  # Check for new files every 1 minute

    def start(self):
        print("Starting PDF processor...")
        self.thread = threading.Thread(target=self.process_files)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()
import os
from flask import Flask

from controllers.retrival_controller import retrieval_controller
from controllers.upload_controller import upload_controller
from services.pdf_processor import PDFProcessor

app = Flask(__name__)
app.register_blueprint(upload_controller)
app.register_blueprint(retrieval_controller)

if __name__ == '__main__':
    if not os.path.exists(os.environ.get('UPLOAD_FOLDER')):
        os.makedirs(os.environ.get('UPLOAD_FOLDER'))

    pdf_processor = PDFProcessor(os.environ.get('UPLOAD_FOLDER'), os.environ.get('ALLOWED_EXTENSIONS'))
    pdf_processor.start()

    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        pdf_processor.stop()
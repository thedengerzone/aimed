import os
import logging
from flask import Flask
from container.config import Container
from controllers.retrival_controller import RetrievalController
from controllers.upload_controller import UploadController

def create_app() -> Flask:
    container = Container()
    container.config.from_dict({
        'upload_folder': os.environ.get('UPLOAD_FOLDER', 'upload'),
        'allowed_extensions': os.environ.get('ALLOWED_EXTENSIONS', {'pdf'})
    })

    flask = Flask(__name__)
    flask.container = container

    upload_controller = UploadController(container.pdf_service())
    retrieval_controller = RetrievalController(container.retrieval_service())
    flask.register_blueprint(upload_controller.blueprint)
    flask.register_blueprint(retrieval_controller.blueprint)

    if not os.path.exists(container.config.upload_folder()):
        os.makedirs(container.config.upload_folder())

    container.pdf_processor()
    container.pdf_service()

    return flask

if __name__ == '__main__':
    # Configure logging globally
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    app = create_app()
    app.run(debug=True)
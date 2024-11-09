import logging
import re
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

logger = logging.getLogger(__name__)


def sanitize_file_name(file_name):
  # Define a regex pattern to remove invalid characters
  pattern = r'[^a-zA-Z0-9_\-\.]'

  # Remove invalid characters from the file name
  sanitized_file_name = re.sub(pattern, '_', file_name)

  # Ensure the file name is not empty
  if not sanitized_file_name:
    sanitized_file_name = 'file'

  return sanitized_file_name


class PDFTextConverter:
  def __init__(self, embeddings_model, chroma_client):
    self.embeddings_model = embeddings_model
    self.chroma_client = chroma_client

  def preprocess_file(self, pdf_path, filename):
    # Resolve the absolute path
    absolute_path = Path(pdf_path).resolve()
    loader = PyPDFLoader(file_path=str(absolute_path))
    full_text = "\n".join([page.page_content for page in loader.load()])

    page_embedding = self.embeddings_model.embed_query(full_text)

    self.chroma_client.store_page_embedding(
        document_id=sanitize_file_name(filename),
        content=full_text,
        page_embedding=page_embedding
    )
    logger.info(f"Stored PDF document {absolute_path} in ChromaDB.")

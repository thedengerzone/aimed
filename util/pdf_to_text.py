from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

from db.vector_db import ChromaDBHandler
from util.preprocessing.text_preprocessing import preprocess_text


class PDFTextConverter:
  def __init__(self, collection_name="pdf_documents"):
    self.vector_store = ChromaDBHandler()
    self.collection_name = collection_name

  # Whole Text Storage
  def store_pdf_embeddings_in_chromadb(self, pdf_path):
    # Resolve the absolute path
    absolute_path = Path(pdf_path).resolve()
    loader = PyPDFLoader(file_path=str(absolute_path))
    full_text = "\n".join([page.page_content for page in loader.load()])

    # Preprocess the text
    processed_text = preprocess_text(full_text)

    self.vector_store.store_to_database(
        collection_name=self.collection_name,
        data={"id": str(absolute_path), "content": processed_text}
    )
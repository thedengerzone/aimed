

from langchain_community.document_loaders import PyPDFLoader
from db.vector_db import ChromaDBHandler

class PDFTextConverter:
    def __init__(self, collection_name="pdf_documents"):
        self.vector_store = ChromaDBHandler()
        self.collection_name = collection_name

    # Function to load PDF and store all pages in ChromaDB
    def store_pdf_embeddings_in_chromadb(self, pdf_path):
        """
        Loads a PDF, generates embeddings for each page, and stores them in ChromaDB.

        Args:
            pdf_path (str): Path to the PDF file.
        """
        # Initialize PDF loader
        loader = PyPDFLoader(pdf_path)

        # Process each page, embed the content, and store it
        for idx, page in enumerate(loader.load()):
            self.vector_store.store_page_embedding(
                idx=idx,
                page=page
            )


# Usage example
# Initialize the PDFTextConverter
converter = PDFTextConverter()

# Load and store PDF embeddings in ChromaDB
converter.store_pdf_embeddings_in_chromadb("doc.pdf")



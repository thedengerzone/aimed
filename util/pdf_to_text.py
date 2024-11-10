import concurrent.futures
import logging
import re
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

logger = logging.getLogger(__name__)

def sanitize_file_name(file_name):
    pattern = r'[^a-zA-Z0-9_\-\.]'
    return re.sub(pattern, '_', file_name) or 'file'


class PDFTextConverter:
    def __init__(self, embeddings_model, chroma_client):
        self.embeddings_model = embeddings_model
        self.chroma_client = chroma_client

    def preprocess_file(self, pdf_path, filename):
        absolute_path = Path(pdf_path).resolve()
        loader = PyPDFLoader(file_path=str(absolute_path))
        pages = loader.load()

        # Combine all pages into one large string
        full_text = " ".join(page.page_content for page in pages)
        full_text = re.sub(r'\s+', ' ', full_text)  # Normalize whitespace
        full_text = re.sub(r'(?<=\S)\n(?=\S)', ' ', full_text)  # Remove unwanted newlines

        # Split the full text by chapters (assuming chapters are denoted by "SOP – ")
        chapters = full_text.split("SOP – ")

        def process_chapter(chapter_number, chapter):
            if chapter_number == 0:
                return

            chapter_content = "SOP – " + chapter  # Add the chapter prefix back
            document_id = f"{sanitize_file_name(filename)}_chapter_{chapter_number}"

            # Embed the full chapter content
            embed_query = self.embeddings_model.embed_query(chapter_content)

            # Store the full chapter as a single entry in the database
            self.chroma_client.store_embedding(
                collection_name=filename,
                content=chapter_content,
                document_id=document_id,
                embeddings=embed_query,
                metadata={"chapter": chapter_number}
            )

        # Use ThreadPoolExecutor to process chapters concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(process_chapter, chapter_number, chapter)
                for chapter_number, chapter in enumerate(chapters)
            ]
            concurrent.futures.wait(futures, timeout=600)

        logger.info(f"Completed processing for {absolute_path}")

import concurrent.futures
import logging
import re
import pymupdf4llm
from langchain_text_splitters import MarkdownTextSplitter, SentenceTransformersTokenTextSplitter

logger = logging.getLogger(__name__)

def sanitize_file_name(file_name):
    pattern = r'[^a-zA-Z0-9_\-\.]'
    sanitized = re.sub(pattern, '_', file_name) or 'file'
    if sanitized == 'file':
        logger.warning(f"Sanitized filename was empty; defaulting to 'file'. Original filename: '{file_name}'")
    return sanitized

def clean_text(text):
    text = re.sub(r'[-#*]{2,}', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

class PDFTextConverter:
    def __init__(self, embeddings_model, chroma_client):
        self.embeddings_model = embeddings_model
        self.chroma_client = chroma_client
        self.text_splitter = MarkdownTextSplitter(chunk_size=5000, chunk_overlap=500)
        self.token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=256)

    def preprocess_file(self, pdf_path, filename):
        pages = pymupdf4llm.to_markdown(pdf_path)
        full_text = clean_text(" ".join(pages) if isinstance(pages, list) else pages)

        chunks = self.text_splitter.create_documents([full_text])

        def process_chunk(chunk_number, chunk):
            chunk_id = f"{sanitize_file_name(filename)}_chunk_{chunk_number}"
            token_text = self.token_splitter.split_text(chunk.page_content)

            metadata = {
                "filename": filename,
                "chunk_number": chunk_number,
                "chunk_length": len(chunk.page_content),
                "chunk_id": chunk_id,
            }

            logger.debug(f"Storing chunk {chunk_number} with metadata: {metadata}")
            self.chroma_client.store_embedding(
                collection_name=filename,
                document_id=chunk_id,
                content=token_text,
                metadata=metadata
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(process_chunk, chunk_number, chunk)
                       for chunk_number, chunk in enumerate(chunks)]
            concurrent.futures.wait(futures, timeout=1000)

        logger.info(f"Completed processing for {filename}")

logging.basicConfig(level=logging.INFO)

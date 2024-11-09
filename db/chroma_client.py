import logging
import os

import chromadb
from chromadb.api.types import IncludeEnum
from chromadb.config import Settings

logger = logging.getLogger(__name__)

class ChromaDBHandler:
    def __init__(self, host=os.environ.get("DB_HOST"), port=int(os.environ.get("DB_PORT")), auth_token=os.environ.get("AUTH_TOKEN")):
        self.client = chromadb.HttpClient(
            host=host,
            port=port,
            settings=Settings(
                chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
                chroma_client_auth_credentials=auth_token
            )
        )

    # Ensure the collection exists or create it if it doesn't
    def get_or_create_collection(self, collection_id):
        collections = self.client.list_collections()
        if collection_id not in [col.name for col in collections]:
            self.client.create_collection(collection_id)
        return self.client.get_collection(collection_id)

    # Store a document in the database
    def store_page_embedding(self, document_id, content, page_embedding):
        collection = self.get_or_create_collection(document_id)
        collection.upsert(
            ids=[document_id],
            embeddings=[page_embedding],
            documents=[content]
        )
        logger.info(f"Stored PDF document {document_id} in ChromaDB.")

    # Retrieve a document by ID
    def retrieve_from_database(self, collection_name, doc_id):
        collection = self.get_or_create_collection(collection_name)
        document = collection.get(ids=[doc_id])
        return document

    # Update a document in the database
    def update_database_entry(self, collection_name, doc_id, updated_data):
        collection = self.get_or_create_collection(collection_name)
        document = collection.get(ids=[doc_id])
        if document:
            collection.update(ids=[doc_id], documents=[updated_data])
            logger.info(f"Document {doc_id} updated successfully.")
        else:
            logger.info(f"Document {doc_id} does not exist.")

    # Delete a document from the database
    def delete_from_database(self, collection_name, doc_id):
        collection = self.get_or_create_collection(collection_name)
        collection.delete(ids=[doc_id])
        logger.info(f"Document {doc_id} deleted successfully.")

    # Perform a similarity search based on a query
    def similarity_search(self, collection_name, query_embedding, top_k=3):
        collection = self.get_or_create_collection(collection_name)
        results = collection.query(query_embedding, n_results=top_k, include=[IncludeEnum.documents])
        return results['documents']

    # Get similarity scores based on a query
    def get_similarity_score(self, collection_name, query_embedding, top_k=5):
        collection = self.get_or_create_collection(collection_name)
        results = collection.query(query_embedding, n_results=top_k,include=[IncludeEnum.distances])
        return results['distances']
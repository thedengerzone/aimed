
from pathlib import Path

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
import chromadb
from chromadb.config import Settings

class ChromaDBHandler:
    def __init__(self, host="localhost", port=8000, auth_token="test-token", model_name="llama3.2:1b"):
        self.client = chromadb.HttpClient(
            host=host,
            port=port,
            settings=Settings(
                chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
                chroma_client_auth_credentials=auth_token
            )
        )
        self.model_name = model_name
        self.embeddings_model = OllamaEmbeddings(model=self.model_name)

    # Ensure the collection exists or create it if it doesn't
    def get_or_create_collection(self, collection_name):
        if collection_name not in [col.name for col in self.client.list_collections()]:
            self.client.create_collection(collection_name)
        return self.client.get_collection(collection_name)

    # Store a document in the database
    def store_to_database(self, collection_name, data):
        collection = self.get_or_create_collection(collection_name)
        doc_id = data.get("id")
        content = data.get("content")
        metadata = data.get("metadata", {})  # Optional metadata

        collection.add(documents=[{

            "content": content,
            "metadata": metadata
        }])
        print(f"Document {doc_id} stored successfully.")

    # Retrieve a document by ID
    def retrieve_from_database(self, collection_name, doc_id):
        collection = self.get_or_create_collection(collection_name)
        document = collection.get_document(doc_id)
        return document

    # Update a document in the database
    def update_database_entry(self, collection_name, doc_id, updated_data):
        collection = self.get_or_create_collection(collection_name)
        document = collection.get_document(doc_id)
        if document:
            collection.update_document(doc_id, updated_data)
            print(f"Document {doc_id} updated successfully.")
        else:
            print(f"Document {doc_id} does not exist.")

    # Delete a document from the database
    def delete_from_database(self, collection_name, doc_id):
        collection = self.get_or_create_collection(collection_name)
        collection.delete_document(doc_id)
        print(f"Document {doc_id} deleted successfully.")

    # Store an embedded page in ChromaDB
    def store_page_embedding(self, idx, page: Document):
        """
        Generates an embedding for a PDF page and stores it in ChromaDB.

        Args:
            collection_name (str): Collection name in the database.
            idx (int): Page index for unique ID generation.
            page (Document): The page content to embed and store.
        """
        # Generate embedding for the page content
        print(page)

        page_embedding = self.embeddings_model.embed_query(page.page_content)

        # Generate a unique ID for each page
        doc_id = f"{Path(page.id).stem}_page_{idx + 1}"

        # Get collection
        collection = self.get_or_create_collection(doc_id)

        # Store in ChromaDB
        collection.add(
            documents=[{
                "id": doc_id,
                "content": page.page_content,
                "embedding": page_embedding,
                "metadata": {"page_number": idx + 1}
            }]
        )
        print(f"Stored page {idx + 1} with ID {doc_id}")

    # Perform a similarity search based on a query
    def similarity_search(self, collection_name, query, top_k=5):
        collection = self.get_or_create_collection(collection_name)
        query_embedding = self.embeddings_model.embed_query(query)
        results = self.similarity_search(collection,query_embedding,top_k)
        return results

from db.vector_db import ChromaDBHandler

class RetrievalService:
    def __init__(self):
        self.db_handler = ChromaDBHandler()

    def retrieve_results(self, collection_name, prompt, top_k=5):
        return self.db_handler.similarity_search(collection_name, prompt, top_k)
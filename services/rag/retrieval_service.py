import numpy as np
import spacy
from chromadb.utils.embedding_functions.sentence_transformer_embedding_function import \
    SentenceTransformerEmbeddingFunction


class RetrievalService:
    def __init__(self, chroma_client, embeddings_model, gpt_client):
        self.embeddings_model = embeddings_model
        self.chroma_client = chroma_client
        self.gpt_client = gpt_client
        self.embedding_function = SentenceTransformerEmbeddingFunction()

    def retrieve_results(self, collection_name, prompt, top_k=3):
        prompts = self.gpt_client.generate_multiple_prompts_from_request(prompt)
        embeddings = []

        # Embed the original prompt
        prompt_embedding = self.embedding_function(prompt)
        embeddings.append(prompt_embedding)

        # Embed generated prompts and store each individually
        for generated_prompt in prompts['questions']:
            embedding = self.embedding_function(generated_prompt)
            embeddings.append(embedding)

        # Perform similarity search for each embedding, including averaged embedding
        best_score = 0
        best_result = None

        for embedding in embeddings:
            score = self.chroma_client.get_similarity_score(
                collection_name,
                embedding,
                top_k=top_k
            )
            print(score)
            if score[0][0] > best_score:
                best_score = score[0][0]
                best_result = embedding


        result = self.chroma_client.similarity_search(
                collection_name,
                best_result,
                top_k=top_k
            )
        prompt_response = self.gpt_client.generate_response(prompt, result)
        print(f"Retrieved response: {prompt_response['response']} with best score: {best_score}")
        return prompt_response['response']


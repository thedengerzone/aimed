class RetrievalService:
    def __init__(self, chroma_client, embeddings_model, gpt_client):
        self.embeddings_model = embeddings_model
        self.chroma_client = chroma_client
        self.gpt_client = gpt_client

    def retrieve_results(self, collection_name, prompt):
        # Generate multiple prompts using gpt_client
        prompts = self.gpt_client.generate_multiple_prompts_from_request(prompt)
        all_scores = []

        for generated_prompt in prompts:
            query_embedding = self.embeddings_model.embed_query(generated_prompt)
            scores = self.chroma_client.get_similarity_score(collection_name, query_embedding)
            all_scores.extend(scores)

        # Sort all scores and return the top 3
        top_scores = sorted(all_scores, reverse=True)[:3]
        return top_scores
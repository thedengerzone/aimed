import logging
from flask import Blueprint, request, jsonify

class RetrievalController:
    def __init__(self, retrieval_service):
        self.retrieval_service = retrieval_service
        self.logger = logging.getLogger(__name__)
        self.blueprint = Blueprint('retrieval_controller', __name__)
        self.blueprint.add_url_rule('/retrieve', 'retrieve_results', self.retrieve_results, methods=['POST'])

    def retrieve_results(self):
        data = request.get_json()
        collection_name = data.get('collection_name')
        prompt = data.get('prompt')
        if not collection_name or not prompt:
            return jsonify({"error": "collection_name and prompt are required"}), 400

        results = self.retrieval_service.retrieve_results(collection_name, prompt)
        return jsonify(results), 200
from flask import Blueprint, request, jsonify
from services.retrieval_service import RetrievalService

retrieval_controller = Blueprint('retrieval_controller', __name__)
retrieval_service = RetrievalService()


@retrieval_controller.route('/retrieve', methods=['POST'])
def retrieve_results():
  data = request.get_json()
  collection_name = data.get('collection_name')
  prompt = data.get('prompt')
  top_k = data.get('top_k', 5)

  if not collection_name or not prompt:
    return jsonify({"error": "collection_name and prompt are required"}), 400

  results = retrieval_service.retrieve_results(collection_name, prompt, top_k)
  return jsonify(results), 200
import json
import os
import logging

from langchain_ollama import ChatOllama

logger = logging.getLogger(__name__)


class OllamaClient:
  def __init__(self):
    self.gpt = ChatOllama(model=os.environ.get("MODEL_NAME"), temperature=1,
                          num_predict=256)

  def generate_response(self, role, content):
    try:
      response = self.gpt.invoke(input=[
        (role, content)
      ])
      logger.info(f"Response: {response}")
      if 'message' in response and 'content' in response['message']:
        return response['message']['content']
      else:
        logger.error(f"Unexpected response format: {response}")
        return None
    except Exception as e:
      logger.error(f"Error generating response: {e}")
      return None

  def generate_multiple_prompts_from_request(self, content):
    prompt = f"""
        You are an AI assistant. The user has asked the following question: "{content}".
        Please generate 5 related questions that can be used to search for relevant information in a database.
        The output should be in JSON format as an array of questions.

        Example output:
            "questions": [
                "Related question 1",
                "Related question 2",
                "Related question 3"
            ]
        """
    try:
      response = self.gpt.invoke(input=[
        ("system", prompt)
      ])
      logger.info(f"Response: {response}")
      if 'message' in response and 'content' in response['message']:
        try:
          questions = json.loads(response['message']['content'])
          return questions
        except json.JSONDecodeError:
          logger.error("Failed to decode JSON from response")
          return None
      else:
        logger.error(f"Unexpected response format: {response}")
        return None
    except Exception as e:
      logger.error(f"Error generating multiple prompts: {e}")
      return None

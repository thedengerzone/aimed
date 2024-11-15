import json
import logging
import os
from openai import OpenAI

logger = logging.getLogger(__name__)


class OpenAIClient:
    def __init__(self):
        self.gpt = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), project=os.getenv("OPEN_AI_PROJECT_ID"))

    def translate_to_english(self, content):
        try:
            response = self.gpt.chat.completions.create(
                model="gpt-4o",
                temperature=0,
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system",
                     "content": "You are a helpful assistant tasked with translating Croatian text into English. The translations will be used for vector embeddings, so the output must be accurate and returned in JSON format."},
                    {
                        "role": "user",
                        "content": content
                    }
                ]

            )
        except Exception as e:
            print(f"Error: {e}")

            logger.info(f"Response: {response}")
            if 'message' in response and 'content' in response['message']:
                return response['message']['content']
            else:
                logger.error(f"Unexpected response format: {response}")
                return None
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return None

    def generate_response(self, content):
        try:
            response = self.gpt.chat.completions.create(
                model="gpt-4o",
                temperature=0,
                messages=[
                    {"role": "system", "content": "You are helpful assistant which is translating croatian text to english."},
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )
        except Exception as e:
            print(f"Error: {e}")

            logger.info(f"Response: {response}")
            if 'message' in response and 'content' in response['message']:
                return response['message']['content']
            else:
                logger.error(f"Unexpected response format: {response}")
                return None
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return None

    def get_embedding(self, text):
        response =  self.gpt.embeddings.create(model="text-embedding-3-large", input=text)
        return response['data']

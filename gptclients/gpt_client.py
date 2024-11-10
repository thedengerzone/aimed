import json
import logging
import os

from openai import AzureOpenAI

logger = logging.getLogger(__name__)


class AzureClient:
    def __init__(self):
        self.gpt = AzureOpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("ENDPOINT"), api_version="2024-02-01")

    def generate_response(self, prompt, content):
        prompt = f"""
    Vi ste AI pomoćnik. Korisnik je postavio sljedeće pitanje: "{prompt}".
    Iz baze smo izvukli sljedeće informacije o pitanju: "{content}".
    Kreiraj 1 odgovor na postavljeno pitanje.

    Primjer izlaza:
        {{
            "response": 
                "Odgovor"
        }}
    """

        try:
            response = self.gpt.invoke(input=prompt, format="json")
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

    def generate_multiple_prompts_from_request(self, content):
        prompt = f"""
                    Vi ste AI pomoćnik. Korisnik je postavio sljedeće pitanje: "{content}".
                    Molimo generirajte 5 sličnih pitanja koja se mogu koristiti za pretragu relevantnih informacija u bazi podataka.
                    Izlaz treba biti u JSON formatu kao niz pitanja.

                    Primjer izlaza:
                        "questions": [
                            "Povezano pitanje 1",
                            "Povezano pitanje 2",
                            "Povezano pitanje 3"
                        ]
                    """
        try:
            response = self.gpt.invoke(input=prompt, format="json")
            logger.info(f"Response: {response}")
            if response.content:
                try:
                    questions = json.loads(response.content)
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

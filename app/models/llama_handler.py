import ollama
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s")

class OllamaHandler:
    def __init__(self, model_name="llama3.2:latest"):
        logging.info(f"Initializing OllamaHandler with model: {model_name}")
        self.model_name = model_name
        self.base_url = "http://localhost:11434/api/generate"
        logging.info("OllamaHandler initialized successfully.")
        
    def generate(self, prompt: str, max_tokens=1024) -> str:
        logging.info(f"Generating response with model: {self.model_name}, max_tokens: {max_tokens}")
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "max_tokens": max_tokens,
                "top_p": 0.9
            }
        }
        
        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            logging.info(f"Response received successfully. Length: {len(response.text)} characters")
            return response.json()["response"]
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            return ""

    def generate_response(self, system_prompt: str, user_prompt: str, model: str = "llama3.2:latest") -> str:
        """
        Generate a response using the specified Ollama model with system and user roles.

        Parameters:
        - system_prompt (str): Instructional message to set the system behavior.
        - user_prompt (str): User's message or query.
        - model (str): The Ollama model to use (default is 'llama3.2:latest').

        Returns:
        - str: The response from the model.
        """
        print(f"system prompt: {system_prompt}")
        print(f"user prompt: {user_prompt}")
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response["message"]["content"]


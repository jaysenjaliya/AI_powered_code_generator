import logging
import json
from app.models.llama_handler import OllamaHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s")

class SyntaxQueryParser:
    def __init__(self):
        logging.info("Initializing SyntaxQueryParser with OllamaHandler...")
        self.llama = OllamaHandler()
        logging.info("SyntaxQueryParser initialized successfully.")
        
    def parse(self, query: str) -> list:
        logging.info(f"Parsing query: {query}")
        
        system_prompt = f"""Analyze this programming query and extract atomic syntax requirements:
        Input Format: 
        User Query: Complex Programming Task Query
        Output Format: 
        Return ONLY a JSON array of syntax elements.
        Instructions:
        1. Breakdown Query into simpler task.
        2. Identify Syntax requirements for the task.
        3. Return a combined single JSON array of all the tasks' Syntax requirements. 
        4. **Strictly give only the necessary syntax requirements.**
        ######################################################
        Example 1:
        User Query: how to open csv file
        Output: ["file handling", "CSV parsing"]
        ######################################################
        Example 2:
        User Query: how to initialize array and append an element into it
        Output: ["Array Initialization", "Operation on Arrays"]
        ######################################################
        Note: **STRICTLY STICK TO THE FORMAT**
        """
        user_prompt = f"""
        User Query: {query}. In python
        """
        
        logging.info("Generating syntax elements using OllamaHandler...")
        response = self.llama.generate_response(system_prompt, user_prompt)
        logging.info(f"Generated response: {response[:100]}... (truncated for logging)")
        
        parsed_response = self._clean_response(response)
        logging.info(f"Extracted {len(parsed_response)} syntax elements.")
        print(f"parsed response: {parsed_response}")
        
        return parsed_response
    
    def _clean_response(self, response: str) -> list:
        logging.info("Cleaning response from OllamaHandler...")
        try:
            cleaned_response = json.loads(response)
            logging.info("Successfully parsed JSON response.")
            return cleaned_response
        except json.JSONDecodeError:
            logging.warning("JSON decoding failed, falling back to simple splitting.")
            fallback_response = [r.strip("- ").strip() for r in response.split("\n") if r.strip()]
            logging.info(f"Extracted {len(fallback_response)} elements using fallback method.")
            return fallback_response

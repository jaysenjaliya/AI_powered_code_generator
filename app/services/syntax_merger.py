import logging
from app.models.llama_handler import OllamaHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
)


class CodeMerger:
    def __init__(self):
        logging.info("Initializing CodeMerger with OllamaHandler...")
        self.llama = OllamaHandler()
        logging.info("CodeMerger initialized successfully.")

    def format_document_chunk(self, snippet):
        chunk = snippet.get("chunk", "")
        summary = snippet.get("summary", "")
        code_snippet = snippet.get("code_snippet", "")
        chunk_title = snippet.get("chunk_title", "")
        use_case = snippet.get("use_case", "")

        return f"""
        ######################################
        Title: {chunk_title}
        Summary: {summary}
        Code:
        {code_snippet}
        ######################################
        """

    

    def merge_code(self, snippets: list, query: str) -> str:
        logging.info(f"Merging {len(snippets)} code snippets for query: {query}")

        context = "\n=======================================\n".join(
            [self.format_document_chunk(snippet) for snippet in snippets]
        )
        logging.debug(f"Generated context for merging:")
        logging.debug(context)

        code_prompt = f"""Combine these code snippets into working Python code:
        Query: {query}
        Documentation:
        {context}
        
        Requirements:
        1. Include relevant imports
        2. Follow PEP8 guidelines
        3. Add type hints
        4. Include error handling
        5. Use relevant documentation code only
        6. If documentation is not enough just give functions that can help in writing code
        7. **Don't add any extra logic**
        
        **Return ONLY the code without explanations.**
        """

        logging.info("Generating code using OllamaHandler...")
        code = self.llama.generate(code_prompt)
        logging.info(f"Generated code of length {len(code)} characters.")

        explanation_prompt = f"""Explain the syntax choices in this code:
        {code}
        
        Focus on:
        - Key Python features used
        - Standard library modules
        - Error handling patterns
        - Best practices followed
        """

        logging.info("Generating explanation using OllamaHandler...")
        explanation = self.llama.generate(explanation_prompt)
        logging.info(f"Generated explanation of length {len(explanation)} characters.")

        return code, explanation

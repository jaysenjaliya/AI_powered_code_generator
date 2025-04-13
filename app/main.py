from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.api_schemas import CodeRequest, CodeResponse
from app.services.query_parser import SyntaxQueryParser
from app.services.document_retrieval import DocumentRetriever
from app.services.syntax_merger import CodeMerger
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s")

# Create the FastAPI app instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for testing)
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

BASE_DIR = Path(__file__).parent.parent

# Initialize components
logging.info("Initializing DocumentRetriever, SyntaxQueryParser, and CodeMerger...")
retriever = DocumentRetriever(
    docs_path="data/faiss_index/documentation_chunks.json",
    summary_index_path="C:\\code_gen_backend\\backend2\\data\\faiss_index\\summary_index.index",
    usecase_index_path="C:\\code_gen_backend\\backend2\\data\\faiss_index\\usecase_index.index"
)
parser = SyntaxQueryParser()
merger = CodeMerger()
logging.info("Components initialized successfully.")

@app.post("/generate", response_model=CodeResponse)
async def generate_code(request: CodeRequest):
    try:
        logging.info(f"Received request: {request.prompt}")
        
        # Parse query into syntax components
        syntax_elements = parser.parse(request.prompt)
        logging.info(f"Parsed syntax elements: {syntax_elements}")
        
        doc_indices = set()

        # Retrieve relevant docs
        for element in syntax_elements:
            retrieved_indices = retriever.retrieve(element, k=2)
            doc_indices.update(retrieved_indices)
            logging.info(f"Retrieved {len(retrieved_indices)} snippets for element: {element}")
        
        snippets = retriever.fetch_docs(list(doc_indices))

        # Generate final code
        code, explanation = merger.merge_code(snippets, request.prompt)
        logging.info(f"Generated code of length {len(code)} characters.")
        
        # Properly format response for canvas-like display
        formatted_response = CodeResponse(
            generated_code=code,  # Raw code string (not inside markdown)
            explanation=explanation,
            references=list({s['source'] for s in snippets})
        )
        with open("./output_code.md", "w", encoding="utf-8") as f:
            f.write(code)
        with open("./output_explanation.md", "w", encoding="utf-8") as f:
            f.write(explanation)
        logging.info("Code generation successful.")
        return formatted_response
    
    except Exception as e:
        logging.error(f"🔥 Error in generate_code: {str(e)}", exc_info=True)
        return CodeResponse(
            generated_code="",  # Ensure response model structure is maintained
            explanation=f"An error occurred: {str(e)}",
            references=[])
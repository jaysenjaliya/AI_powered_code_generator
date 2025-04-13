import os
import json
import logging
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# def extract_json(text: str) -> dict:
#     """Extracts and parses JSON from text response."""
#     try:
#         match = re.search(r'```json\n(.*?)\n```', text, re.DOTALL)
#         if match:
#             json_content = match.group(1).strip()
#             logging.info(f"json content: {json_content}")
#             return json.loads(json_content)
#     except json.JSONDecodeError as e:
#         logging.error(f"Error decoding JSON: {e}")
#     return {}

# def generate_llama_response(prompt: str, text_chunk: str) -> dict:
#     """Generates structured output using Ollama's LLaMA model."""
#     try:
#         response = ollama.chat(model="llama3.2:latest", messages=[
#             {"role": "system", "content": prompt},
#             {"role": "user", "content": text_chunk}
#         ])
        
#         logging.info(f"Output of LLaMA response: {response}")
        
#         content = response.get("message", {}).get("content", "").strip()
        
#         result = extract_json(content)
#         logging.info(f"extracted json: {result}")
        
#         return {
#             "summary": result.get("summary", ""),
#             "code_snippet": result.get("code_snippet", ""),
#             "chunk_title": result.get("chunk_title", ""),
#             "use_case": result.get("use_case", "")
#         }
#     except (KeyError, TypeError) as e:
#         logging.error(f"Error processing LLaMA response: {e}")
#         return {"summary": "", "code_snippet": "", "chunk_title": "", "use_case": ""}

# def load_documentation(file_path: str) -> str:
#     """Loads text from a documentation file."""
#     logging.info(f"Loading documentation: {file_path}")
#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             return f.read()
#     except Exception as e:
#         logging.error(f"Error loading {file_path}: {e}")
#         return ""

# def split_into_chunks(text, chunk_size=2000, chunk_overlap=200):
#     """Splits text into smaller chunks for processing."""
#     logging.info("Splitting text into chunks...")
#     try:
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=chunk_size,
#             chunk_overlap=chunk_overlap,
#             separators=["\n\n", "\n", " ", ""]
#         )
#         return text_splitter.split_text(text)
#     except Exception as e:
#         logging.error(f"Error splitting text: {e}")
#         return []

# def generate_chunk_metadata(text_chunk):
#     with open("C:\\code_gen_backend\\backend2\\scripts\\prompt.txt","r",encoding="utf-8") as f:
#         prompt = f.read()
#     try:
#         response = generate_llama_response(prompt, text_chunk)
#         logging.info(f"chunk metadata: {response}")
#         return response
#     except Exception:
#         return None

def process_prebuilt_chunks(chunks_json: Path, summary_faiss_path: Path, usecase_faiss_path: Path):
    """Loads prebuilt chunks and generates FAISS indexes."""
    logging.info(f"Loading prebuilt chunks from {chunks_json}")
    
    try:
        with open(chunks_json, "r", encoding="utf-8") as f:
            chunks = json.load(f)
    except Exception as e:
        logging.error(f"Error loading chunks JSON: {e}")
        return
    
    summaries = [chunk["summary"] for chunk in chunks]
    use_cases = [chunk["use_case"] for chunk in chunks]
    
    logging.info("Creating FAISS index for summaries and use cases...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Create FAISS index for summaries
    summary_vectors = np.array(model.encode(summaries, convert_to_numpy=True)).astype('float32')
    dimension = summary_vectors.shape[1] if summary_vectors.size > 0 else 384
    summary_index = faiss.IndexFlatIP(dimension)
    if summary_vectors.size > 0:
        summary_index.add(summary_vectors)
    faiss.write_index(summary_index, str(summary_faiss_path))
    
    # Create FAISS index for use cases
    usecase_vectors = np.array(model.encode(use_cases, convert_to_numpy=True)).astype('float32')
    usecase_index = faiss.IndexFlatIP(dimension)
    if usecase_vectors.size > 0:
        usecase_index.add(usecase_vectors)
    faiss.write_index(usecase_index, str(usecase_faiss_path))
    
    logging.info(f"FAISS indexes saved at {summary_faiss_path} and {usecase_faiss_path}")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent.parent
    chunks_json = BASE_DIR / "data" / "faiss_index" / "documentation_chunks.json"
    summary_faiss_path = BASE_DIR / "data" / "faiss_index" / "summary_index.index"
    usecase_faiss_path = BASE_DIR / "data" / "faiss_index" / "usecase_index.index"
    
    process_prebuilt_chunks(chunks_json, summary_faiss_path, usecase_faiss_path)

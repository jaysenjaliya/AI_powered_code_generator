import json
import faiss
import logging
from typing import List, Dict,Any
from sentence_transformers import SentenceTransformer
from rich import print


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s")

class DocumentRetriever:
    def __init__(self, summary_index_path: str, usecase_index_path: str, docs_path: str, model_name: str = "all-MiniLM-L6-v2"):
        logging.info(f"Initializing DocumentRetriever with summary index: {summary_index_path} and docs: {docs_path}")
        logging.info(f"Initializing DocumentRetriever with usecase index: {usecase_index_path} and docs: {docs_path}")
        self.summary_index = faiss.read_index(summary_index_path)
        self.usecase_index = faiss.read_index(usecase_index_path)
        self.model = SentenceTransformer(model_name)
        logging.info(f"Loaded FAISS index and SentenceTransformer model: {model_name}")
        
        with open(docs_path, "r") as f:
            self.docs = json.load(f)
            logging.info(f"Loaded {len(self.docs)} documentation snippets from {docs_path}")
    
    def retrieve_from_index(self, task: str, index: Any, k: int = 2) -> List[Dict]:
        """Retrieve the closest match from each FAISS index, ensuring score > 0.53."""
        logging.info(f"Retrieving {k} most relevant snippets for task: {task}")
    
        embedding = self.model.encode([task]).astype('float32')
        logging.info("Generated embedding for task query.")

        scores, indices = index.search(embedding, k )  # Retrieve extra for filtering
        logging.info(f"Retrieved {len(indices[0])} snippets before filtering with scores: {scores[0].tolist()}")

        print(f"scores: {scores}")
        print(f"indices: {indices}")

        # Filter out results where the similarity score is <= 0.53
        valid_results = [(i, scores[0][j]) for j, i in enumerate(indices[0]) if scores[0][j] > 0.6]

        # Ensure we have at least 2 valid results
        # if len(valid_results) < 2:
        #     logging.warning("Not enough valid results found above the threshold.")
        #     return []  # Return an empty list instead of causing an IndexError

        # Sort results by similarity score (highest first)
        valid_results.sort(key=lambda x: x[1], reverse=True)
        
        retrieved_docs = [self.docs[index[0]] for index in valid_results]

        # Select the two closest matches
        # best_match_index_1 = valid_results[0][0]
        # best_match_index_2 = valid_results[1][0]

        # print(f"best match index 1: {best_match_index_1}")
        # print(f"best match index 2: {best_match_index_2}")

        # retrieved_docs = [self.docs[best_match_index_1], self.docs[best_match_index_2]]
        print(f"retrieve docs: {retrieved_docs}")
        logging.info(f"Returning {len(retrieved_docs)} relevant documentation snippets.")

        return valid_results
    
    def retrieve(self, task: str, k: int = 2) -> List[Dict]:
        summary_valid_results = self.retrieve_from_index(task, self.summary_index, k)
        usecase_valid_results = self.retrieve_from_index(task, self.usecase_index, k)
        
        # Combine results from both indices
        combined_results = summary_valid_results + usecase_valid_results
        
        # Sort results by similarity score in descending order
        combined_results.sort(key=lambda x: x[1], reverse=True)
        
        # Retrieve the top k results
        top_results = combined_results[:k]
        
        # Extract document indices
        doc_indices = [result[0] for result in top_results]
        
        # # Fetch the corresponding documents
        # retrieved_docs = [self.docs[i] for i in doc_indices if i < len(self.docs)]
        
        # logging.info(f"Returning {len(retrieved_docs)} relevant documentation snippets.")
        return doc_indices
    
    def fetch_docs(self, indices):
        retrieved_docs = [self.docs[i] for i in indices if i < len(self.docs)]
        
        logging.info(f"Returning {len(retrieved_docs)} relevant documentation snippets.")
        return retrieved_docs


        



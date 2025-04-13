from pydantic import BaseModel
from typing import List

class CodeRequest(BaseModel):
    prompt: str

class CodeResponse(BaseModel):
    generated_code: str  # Changed from 'code' to match your implementation
    explanation: str
    references: List[str]
from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

class Evidence(BaseModel):
    document: str
    chunk_index: int
    text: str
    score: float

class SearchResponse(BaseModel):
    query: str
    results: List[Evidence]

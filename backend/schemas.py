from pydantic import BaseModel
from typing import List


class SearchRequest(BaseModel):
    query: str
    top_k: int = 3


class EvidenceChunk(BaseModel):
    document: str
    chunk_index: int
    text: str


class SearchResponse(BaseModel):
    answer: str
    confidence: float
    evidence: List[EvidenceChunk]

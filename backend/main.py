from fastapi import FastAPI, UploadFile, File
from backend.schemas import SearchRequest, SearchResponse
from backend.ingest import ingest_document
from backend.search import search_similar_chunks

app = FastAPI(title="Semantic Search API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    text = (await file.read()).decode("utf-8")
    ingest_document(file.filename, text)
    return {"message": "Document ingested successfully"}

@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    results = search_similar_chunks(req.query, req.top_k)

    formatted = [
        {
            "document": r["document_name"],
            "chunk_index": r["chunk_index"],
            "text": r["chunk_text"],
            "score": round(r["score"], 3),
        }
        for r in results
    ]

    return {
        "query": req.query,
        "results": formatted
    }

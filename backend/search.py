from backend.db import get_connection
from backend.embeddings import generate_embedding
from backend.similarity import cosine_similarity
from backend.llm import generate_answer

import json


def search_similar_chunks(query: str, top_k: int = 3):
    query_embedding = generate_embedding(query)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            document_name,
            chunk_index,
            chunk_text,
            embedding
        FROM document_chunks
    """)

    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        embedding = json.loads(row["embedding"])
        score = cosine_similarity(query_embedding, embedding)

        results.append({
            "document_name": row["document_name"],
            "chunk_index": row["chunk_index"],
            "chunk_text": row["chunk_text"],
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def answer_query(query: str, top_k: int = 3):
    results = search_similar_chunks(query, top_k)

    if not results:
        return {
            "answer": "I don't know based on the provided context.",
            "confidence": 0.0,
            "chunks": []
        }

    context_chunks = [r["chunk_text"] for r in results]

    answer = generate_answer(context_chunks, query)

    #confidence = sum(r["score"] for r in results) / len(results)
    confidence = float(sum(r["score"] for r in results) / len(results))


    return {
        "answer": answer,
        "confidence": round(confidence, 3),
        "chunks": results
    }
from backend.db import get_connection
from backend.embeddings import generate_embedding
from backend.similarity import cosine_similarity
from backend.llm import generate_answer
import json


def search_similar_chunks(query: str, top_k: int = 3):
    query_embedding = generate_embedding(query)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            document_name,
            chunk_index,
            chunk_text,
            embedding
        FROM document_chunks
    """)

    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        embedding = json.loads(row["embedding"])
        score = cosine_similarity(query_embedding, embedding)

        results.append({
            "document_name": row["document_name"],
            "chunk_index": row["chunk_index"],
            "chunk_text": row["chunk_text"],
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def answer_query(query: str, top_k: int = 3):
    results = search_similar_chunks(query, top_k)

    if not results:
        return {
            "answer": "I don't know based on the provided context.",
            "confidence": 0.0,
            "evidence": []
        }

    context_chunks = [r["chunk_text"] for r in results]

    # ✅ LLM IS CALLED HERE
    answer = generate_answer(context_chunks, query)

    confidence = sum(r["score"] for r in results) / len(results)

    evidence = [
        {
            "document": r["document_name"],
            "chunk_index": r["chunk_index"],
            "text": r["chunk_text"]
        }
        for r in results
    ]

    return {
        "answer": answer,
        "confidence": round(confidence, 3),
        "evidence": evidence
    }

from backend.db import get_connection
from backend.chunking import semantic_chunk_text
from backend.embeddings import generate_embedding
import json

def ingest_document(document_name: str, text: str):
    chunks = semantic_chunk_text(text)

    conn = get_connection()
    cursor = conn.cursor()

    for idx, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)

        cursor.execute(
            """
            INSERT INTO document_chunks (document_name, chunk_index, chunk_text, embedding)
            VALUES (%s, %s, %s, %s)
            """,
            (document_name, idx, chunk, json.dumps(embedding))
        )

    conn.commit()
    cursor.close()
    conn.close()

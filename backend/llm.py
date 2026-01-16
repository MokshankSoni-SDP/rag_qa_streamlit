import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_answer(context_chunks: list[str], question: str) -> str:
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    context_text = "\n\n".join(context_chunks)

    prompt = f"""
You are a factual assistant.
Answer the question ONLY using the context below.
If the answer is not present, say:
"I don't know based on the provided context."

Context:
{context_text}

Question:
{question}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0
        }
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

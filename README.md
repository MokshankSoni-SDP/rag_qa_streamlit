# RAG-Based Semantic Search System (FastAPI + MySQL + Streamlit)

This project implements a **Retrieval-Augmented Generation (RAG)** system that allows users to upload documents, perform semantic search over them, and generate **fact-grounded answers** using a Large Language Model (LLM).

The system is built with:

- **FastAPI** for backend APIs
- **Sentence Transformers** for embeddings
- **MySQL (Aiven)** for persistent storage
- **Custom cosine similarity** for retrieval
- **OpenRouter LLM API** for answer generation
- **Streamlit** as the frontend UI

---

## 1. Chunking Strategy

### What We Did

We use a **custom semantic-aware chunking approach** (without external chunking libraries), as required.

- Documents are split into **fixed-size text chunks**
- Chunk size is chosen to:
  - Preserve semantic meaning
  - Fit within embedding and LLM context limits
- Each chunk is stored with:
  - `document_name`
  - `chunk_index`
  - `chunk_text`
  - `embedding`

### Why This Works

- Smaller chunks improve retrieval precision
- Prevents irrelevant context from being passed to the LLM
- Enables fine-grained semantic search

### Why No External Chunking Library

- Full control over logic
- Transparent behavior
- Easier debugging and explanation in interviews

---

## 2. Embedding Choice

### Model Used - sentence-transformers/all-MiniLM-L6-v2

### Why This Model

- Lightweight and fast
- Produces high-quality semantic embeddings
- 384-dimensional vectors (efficient for storage and similarity search)
- Widely used and well-tested for semantic search tasks

### How Embeddings Are Used

- Each chunk is converted into an embedding vector
- Query text is embedded using the same model
- Cosine similarity is computed between query embedding and stored chunk embeddings

---

## 3. Confidence Logic

### How Confidence Is Calculated

Confidence is computed as: average cosine similarity of the top-k retrieved chunks

### Why This Makes Sense

- Higher similarity = stronger semantic match
- Averaging avoids overconfidence from a single chunk
- Produces a normalized, interpretable confidence score

### Example

- Confidence ≈ `0.30` → moderate semantic match
- Confidence ≈ `0.60+` → strong semantic grounding

This confidence reflects **retrieval certainty**, not LLM certainty.

---

## 4. Hallucination Prevention

Hallucination prevention is a **core design goal** of this project.

### Techniques Used

#### 1. Retrieval-Augmented Generation (RAG)

- LLM never answers from its own knowledge
- It only sees **retrieved document chunks**

#### 2. Strict Prompting

The LLM prompt explicitly instructs:
Answer ONLY using the provided context.
If the answer is not present, say:
"I don't know based on the provided context."

#### 3. Temperature = 0

- Forces deterministic outputs
- Reduces creative guessing

#### 4. Context Limiting

- Only top-k most relevant chunks are passed
- Prevents irrelevant information leakage

---

## 5. Limitations

While the system works reliably, it has some limitations:

### 1. No Vector Indexing

- Cosine similarity is computed in Python
- Not optimized for very large datasets
- Can be improved using FAISS or pgvector in the future

### 2. Basic Chunking Strategy

- Chunking is size-based, not discourse-aware
- Future improvement: sentence-boundary or topic-based chunking

### 3. Confidence Is Heuristic-Based

- Confidence is derived from similarity scores
- Not a calibrated probability
- Intended for guidance, not guarantees

### 4. External LLM Dependency

- Requires OpenRouter API availability
- Offline usage is not supported

---

## Summary

This project demonstrates a **clean, explainable, and interview-ready RAG pipeline**, with:

- Custom chunking
- Semantic embeddings
- Transparent similarity scoring
- Strong hallucination control
- Production-style backend + UI

It prioritizes **correctness, explainability, and real-world design choices** over unnecessary complexity.

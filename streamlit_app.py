import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG Semantic Search", layout="wide")
st.title("📄 RAG Semantic Search (MySQL + LLM)")

# ---------- Upload Section ----------
st.header("📤 Upload a Document")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(
        f"{API_URL}/ingest",
        files={"file": uploaded_file}
    )

    if response.status_code == 200:
        st.success("Document ingested successfully")
    else:
        st.error("Ingestion failed")

# ---------- Search Section ----------
st.header("🔍 Ask a Question")

query = st.text_input("Enter your question")
top_k = st.slider("Top K Chunks", 1, 5, 3)

if st.button("Search") and query:
    with st.spinner("Thinking..."):
        response = requests.post(
            f"{API_URL}/search",
            json={
                "query": query,
                "top_k": top_k
            }
        )

    if response.status_code != 200:
        st.error("Search failed")
    else:
        data = response.json()

        # ---------- Answer ----------
        st.subheader("🧠 Answer")
        st.write(data["answer"])

        st.metric("Confidence", round(data["confidence"], 3))

        # ---------- Evidence ----------
        st.subheader("📚 Evidence Chunks")

        if not data["evidence"]:
            st.warning("No relevant chunks found")
        else:
            for i, chunk in enumerate(data["evidence"], 1):
                with st.expander(f"Chunk {i} — {chunk['document']}"):
                    st.write(chunk["text"])

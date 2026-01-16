import streamlit as st
import requests

# =========================
# CONFIG
# =========================
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Semantic Search System",
    layout="centered"
)

# =========================
# UI HEADER
# =========================
st.title("📄 Semantic Search with MySQL + FastAPI")
st.markdown(
    """
This system allows you to:
- Upload a text document
- Store semantic embeddings in MySQL
- Search using cosine similarity
"""
)

# =========================
# FILE INGESTION
# =========================
st.header("📤 Upload Document")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded_file is not None:
    with st.spinner("Uploading and processing document..."):
        response = requests.post(
            f"{API_URL}/ingest",
            files={"file": (uploaded_file.name, uploaded_file.getvalue())}
        )

    if response.status_code == 200:
        st.success("✅ Document ingested successfully")
    else:
        st.error(f"❌ Ingest failed (Status {response.status_code})")
        st.code(response.text)

# =========================
# SEARCH
# =========================
st.header("🔍 Ask a Question")

query = st.text_input("Enter your query")
top_k = st.slider("Number of results", min_value=1, max_value=5, value=3)

if st.button("Search") and query:
    with st.spinner("Searching relevant chunks..."):
        response = requests.post(
            f"{API_URL}/search",
            json={"query": query, "top_k": top_k}
        )

    if response.status_code != 200:
        st.error(f"❌ Search failed (Status {response.status_code})")
        st.code(response.text)
    else:
        data = response.json()
        results = data.get("results", [])

        if not results:
            st.warning("⚠️ No relevant chunks found.")
        else:
            st.success(f"Found {len(results)} relevant chunks")

            for idx, r in enumerate(results, start=1):
                st.markdown(f"### 📌 Result {idx}")
                st.markdown(f"**Document:** {r['document']}")
                st.markdown(f"**Similarity Score:** `{r['score']}`")
                st.write(r["text"])
                st.markdown("---")

# =========================
# FOOTER
# =========================
st.caption("🚀 Built with FastAPI, Sentence Transformers, MySQL & Streamlit")

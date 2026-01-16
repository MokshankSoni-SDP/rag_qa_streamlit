import re

def semantic_chunk_text(text, max_words=150):
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        word_count = len(sentence.split())

        if current_word_count + word_count <= max_words:
            current_chunk.append(sentence)
            current_word_count += word_count
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_word_count = word_count

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

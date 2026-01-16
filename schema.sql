CREATE TABLE IF NOT EXISTS document_chunks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_name VARCHAR(255) NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

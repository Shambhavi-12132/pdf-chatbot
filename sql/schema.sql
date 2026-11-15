PRAGMA foreign_keys = ON;
-- uploaded pdfs
CREATE TABLE IF NOT EXISTS documents (
    document_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_size INTEGER);

-- text of each pdf page
CREATE TABLE IF NOT EXISTS document_chunks (
    chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    page_number INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES documents(document_id) ON DELETE CASCADE);

-- faster lookup of chunks by document
CREATE INDEX IF NOT EXISTS idx_document_chunks_document_id ON document_chunks(document_id);
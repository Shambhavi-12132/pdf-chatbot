-- insert a sample pdf
INSERT INTO documents (file_name, file_size)
VALUES ('sql_demo.pdf', 1024);

-- add a chunk for it (uses the id we just got)
INSERT INTO document_chunks (document_id, page_number, chunk_text)
VALUES (last_insert_rowid(), 1, 'This is a sample text extracted from a PDF document.');

-- all documents
SELECT * FROM documents;

-- chunks of one document
SELECT * FROM document_chunks WHERE document_id = 1;

-- file name with its text
SELECT documents.file_name, document_chunks.page_number, document_chunks.chunk_text
FROM documents
INNER JOIN document_chunks ON documents.document_id = document_chunks.document_id;

-- change the file size
UPDATE documents SET file_size = 2048 WHERE file_name = 'sql_demo.pdf';

-- delete it, chunks go too because of ON DELETE CASCADE
DELETE FROM documents WHERE file_name = 'sql_demo.pdf';
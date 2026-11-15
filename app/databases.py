import sqlite3
class Database: #database class to handle the database operations
    def __init__(self):
        self.connection = sqlite3.connect("files/chatbot.db")
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.create_tables()
        
#creates all tables
    def create_tables(self):
        self.create_documents_table()
        self.check_file_size_column()
        self.create_chunks_table()
        self.connection.commit()
#table for the uploaded pdfs
    def create_documents_table(self):
        self.connection.execute("""
CREATE TABLE IF NOT EXISTS documents (
document_id INTEGER PRIMARY KEY AUTOINCREMENT,
file_name TEXT NOT NULL,
upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
file_size INTEGER)""")

    # older db files don't have file_size, so add it if it's missing
    def check_file_size_column(self):
        columns = self.connection.execute("PRAGMA table_info(documents)").fetchall()
        column_names = [col[1] for col in columns]

        if "file_size" not in column_names:
            self.connection.execute("ALTER TABLE documents ADD COLUMN file_size INTEGER")

    # text of each pdf page goes here
    def create_chunks_table(self):
        self.connection.execute("""
CREATE TABLE IF NOT EXISTS document_chunks (
chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
document_id INTEGER NOT NULL,
page_number INTEGER NOT NULL,
chunk_text TEXT NOT NULL,
FOREIGN KEY (document_id)
REFERENCES documents(document_id)
ON DELETE CASCADE )""")
#save pdf info and return its id
    def save_document(self, file_name, file_size):
        cursor = self.connection.execute(
    "INSERT INTO documents (file_name, file_size) VALUES (?, ?)",
    (file_name, file_size) )
        self.connection.commit()
        return cursor.lastrowid

#save all chunks for one pdf
    def save_chunks(self, document_id, chunks):
        rows = [(document_id, c["page_number"], c["text"]) for c in chunks]
        self.connection.executemany( "INSERT INTO document_chunks (document_id, page_number, chunk_text) VALUES (?, ?, ?)", rows)
        self.connection.commit()
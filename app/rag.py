import os
from pdf_reader import PDFReader
from pdfchunks import TextChunker
from embedder import Embedder
from vector_store import VectorStore
from databases import Database
from llm import LLM

class RAG:
    def __init__(self): #constructor for the rag class
        self.pdf_reader, self.chunker = PDFReader(), TextChunker() #pdf reader- chunker instances
        self.embedder, self.vector_store = Embedder(), VectorStore()#embedder- vector store instances
        self.database, self.llm = Database(), LLM()#llm instance

    def add_pdf(self, file_path, original_file_name=None): #add pdf method to read the pdf
        pages = self.pdf_reader.read_pdf(file_path)
        file_name = original_file_name or os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        chunks = [ {"text": text, "page_number": page["page_number"]}
            for page in pages
            for text in self.chunker.create_chunks(page["text"]) ]
        if not chunks:
            raise ValueError("No readable text found in the PDF.")
        
        texts = [chunk["text"] for chunk in chunks] #texts list comphrns to extract text from chunks
        embeddings = self.embedder.create_embeddings(texts)
        document_id = self.database.save_document(file_name, file_size)
        self.database.save_chunks(document_id, chunks)
        metadatas = [ {"file_name": file_name, "page_number": c["page_number"], "document_id": document_id}
    for c in chunks ]
        self.vector_store.add_chunks(texts, embeddings, metadatas)
        return document_id

    def find_relevant_text(self, question): #que mtd to find relevnt txt
        embedding = self.embedder.create_embeddings([question])[0]
        results = self.vector_store.search_chunks(embedding, number_of_results=3)
        return [ {"text": text, "file_name": meta.get("file_name", "Unknown file"), "page_number": meta.get("page_number", "Unknown page")}
            for text, meta in zip(results["documents"][0], results["metadatas"][0])
            if meta is not None]

    def ask_question(self, question): #ask question mtd to find answer to the que
        chunks = self.find_relevant_text(question)
        answer = self.llm.generate_answer(question, chunks)
        sources = [{"file_name": c["file_name"], "page_number": c["page_number"]} for c in chunks]
        return {"answer": answer, "sources": sources}

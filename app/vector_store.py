import chromadb
from uuid import uuid4
class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="files/chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="pdf_chunks")
#save text chunks and embeddings
    def add_chunks(self, chunks, embeddings, metadatas=None):
        ids = [str(uuid4()) for _ in chunks]
        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

#Return an empty result if no data is stored
    def empty_result(self):
        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]  }

#keep only useful search results
    def filter_results(self, documents, metadatas, distances, max_distance):
        return [
            (doc, meta, dist)
            for doc, meta, dist in zip(documents, metadatas, distances)
            if dist <= max_distance]
#Search for text related to the question
    def search_chunks(
        self, query_embedding, number_of_results=3, max_distance=1.5):
        total = self.collection.count()
        print("Total stored chunks:", total)
        if total == 0:
            return self.empty_result()
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=min(number_of_results, total)
        )
        print("Retrieved text:", results["documents"][0])
        print("Retrieved distances:", results["distances"][0])
        relevant = self.filter_results(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
            max_distance
        )
        return {
            "documents": [[x[0] for x in relevant]],
            "metadatas": [[x[1] for x in relevant]],
            "distances": [[x[2] for x in relevant]]
        }
    # Check if the uploaded file is temporary
    def is_temporary_pdf(self, file_name):
        name = file_name.lower()
        return name.startswith("tmp") and name.endswith(".pdf")
    # Remove temporary files from storage
    def remove_temporary_uploads(self):
        records = self.collection.get(include=["metadatas"])
        ids = []
        for chunk_id, metadata in zip(records["ids"], records["metadatas"]):
            name = (metadata or {}).get("file_name", "")
            if self.is_temporary_pdf(name):
                ids.append(chunk_id)
        if ids:
            self.collection.delete(ids=ids)
        return len(ids)

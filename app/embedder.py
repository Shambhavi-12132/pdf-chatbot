from sentence_transformers import SentenceTransformer
class Embedder:
    def __init__(self): #constructor for the embedder class
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
    def create_embeddings(self, texts): #method to create embeddings for the given texts
        embeddings = self.model.encode(texts)
        return embeddings
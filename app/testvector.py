from embedder import Embedder
from vector_store import VectorStore
texts = ["A PDF chatbot can read documents and answer questions.",
"Python is a programming language."]
embedder = Embedder()
embeddings = embedder.create_embeddings(texts)
store = VectorStore()
store.add_chunks(texts, embeddings)
question = "How does the chatbot answer questions from PDFs?"
question_embedding = embedder.create_embeddings([question])[0]
results = store.search_chunks(question_embedding, number_of_results=1)
print(results["documents"])
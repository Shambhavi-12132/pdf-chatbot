from embedder import Embedder

embedder = Embedder() #EMEDDER testing 
texts = ["The chatbot reads PDF documents."]
embeddings = embedder.create_embeddings(texts)
print("Number of embeddings:", len(embeddings))
print("Vector length:", len(embeddings[0])) #length of the vector for the first text
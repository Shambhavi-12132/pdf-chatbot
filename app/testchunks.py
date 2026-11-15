from pdfchunks import TextChunker

text = "Hi, I'm Shambhavi, and I'm creating a PDF chatbot that reads the documents and answers questions using the information in the document."
chunker = TextChunker() # testing the chunker
chunks = chunker.create_chunks(text, chunk_size=20, overlap=5)

for chunk in chunks:#loop thruu the chunks and print them
    print(chunk)
    print("---") 
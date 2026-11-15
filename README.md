"PDF Chatbot"

- About

This is a small PDF chatbot project made using Python.

It allows users to upload a PDF and ask questions related to the document. The chatbot reads the PDF and gives answers based on its content.

I have used RAG to find relevant information from the PDF before generating an answer.

- Technologies used

Python, FastAPI, SQLite, ChromaDB, Hugging Face Transformers and Sentence Transformers

- How it works

The application follows these steps:
1. The user uploads a PDF file.
2. The application extracts the text from each page.
3. The extracted text is divided into smaller chunks.
4. Embeddings are generated for the text chunks.
5. The chunks and their metadata are stored in ChromaDB.
6. When a user asks a question, the application searches for relevant chunks.
7. The language model uses the retrieved information to generate an answer.
8. The response includes the source filename and page number.

- How to run

First activate the virtual environment

bash: .\venv\Scripts\Activate.ps1


- Install the required packages

bash : pip install -r requirements.txt

- Start the application

bash: python -m uvicorn main:app --app-dir app --reload

- API endpoints
The API will be available at: http://127.0.0.1:8000
Interactive API documentation: http://127.0.0.1:8000/docs

- POST /upload: Used to upload a PDF file.

- POST /chat: Used to ask questions about the uploaded PDF and get answers with source page details.

- Database

SQLite is used to store document details and extracted text chunks.

ChromaDB is used to store the embeddings and find relevant text from the PDF.
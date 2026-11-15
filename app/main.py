import os, shutil, tempfile  # file handling ke liye
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from rag import RAG

# API ki basic details aur Swagger settings
app = FastAPI(
    title="PDF Chatbot",
    description="Upload your PDF documents and ask questions about their content.",
    version="1.0.0",
    swagger_ui_parameters={"docExpansion": "none", "defaultModelsExpandDepth": -1},
    openapi_tags=[
        {"name": "PDF Documents", "description": "Upload a PDF document to get started."},
        {"name": "Ask Questions", "description": "Ask questions and get answers based on your uploaded PDFs."}])
rag = RAG()  # RAG pipeline ka object

class ChatRequest(BaseModel):
    question: str  # User ka question receive karega

@app.post("/upload", tags=["PDF Documents"], summary="Upload a PDF document",
          description="Select a PDF file to upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Check karte hain ki file PDF hai ya nahi
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Upload a PDF file")

    temporary_path = None
    try:
        # PDF ko temporary file mein save karte hain
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir="files") as temp:
            shutil.copyfileobj(file.file, temp)
            temporary_path = temp.name

        document_id = rag.add_pdf(temporary_path, file.filename)  # PDF process karte hain
        return {"message": "PDF uploaded and executed successfully",
                "document_id": document_id, "file_name": file.filename}

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Could not process PDF: {str(error)}")
    finally:
        # Processing ke baad temporary file delete karte hain
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)
        await file.close()

@app.post("/chat", tags=["Ask Questions"], summary="Ask a question", 
description="Enter a question about your uploaded pdf ")
def chat(request: ChatRequest):
    question = request.question.strip()  # Extra spaces remove karte hain
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
#exception hndling thru which rag asks ques and provides ans
    try:
        return rag.ask_question(question)  # Que rag ko bhejte hain
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Could not answer question: {str(error)}")

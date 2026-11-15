import torch 
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
class LLM:

    def __init__(self): #constructor for the llm class
        model = "google/flan-t5-small"
        self.tokenizer = AutoTokenizer.from_pretrained(model) #model and tokenizer initialization
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model) 
        self.model.to("cpu")# cpu pe model ko load karte hain
        self.model.eval() #model sets to evaluation mode
    def prepare_context(self, chunks):
        return "\n\n".join( f"File: {c.get('file_name')}, Page: {c.get('page_number')}\n{c.get('text')}"
for c in chunks)
    def generate_answer(self, question, retrieved_chunks):
        if not retrieved_chunks:
            return "I could not find this information in the uploaded document."

        context = self.prepare_context(retrieved_chunks) #retrieved chunks ko context m convert karte hain
        prompt = f""" Answer using only the context below.
If the answer is not there say you could not find it.
Context: {context}
Question: {question}  Answer: """
        inputs = self.tokenizer(prompt, return_tensors="pt",truncation=True, max_length=512)
        with torch.no_grad():
            output = self.model.generate(**inputs, max_new_tokens=128)
        return self.tokenizer.decode( output[0], skip_special_tokens=True).strip()

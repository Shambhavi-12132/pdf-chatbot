import os
from databases import Database

db = Database() #database testing
file_name = "sample.pdf" #sample pdf file name
file_size = os.path.getsize("files/sample.pdf")

document_id = db.save_document(file_name, file_size)
print("Saved document ID:", document_id) 

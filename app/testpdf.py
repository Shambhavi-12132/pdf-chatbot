from pdf_reader import PDFReader #pdf testing
reader = PDFReader()
pages = reader.read_pdf("files/sample.pdf")
print(pages)
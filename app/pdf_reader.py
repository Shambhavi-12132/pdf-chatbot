from pypdf import PdfReader
from pathlib import Path
class PDFReader: #pdf reader class to read the pdf
    def read_pdf(self, file_path):
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")

        if path.suffix.lower() != ".pdf": #not a pdf file
            raise ValueError("Please provide a PDF file.")

        reader = PdfReader(str(path))
        pages = []
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append({ "page_number": page_number, "text": text })
        return pages
class TextChunker:
    def create_chunks(self, text, chunk_size=500, overlap=50): #chunk cretion mtd to crt chunks
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]

            chunks.append(chunk)
            start = end - overlap
        return chunks
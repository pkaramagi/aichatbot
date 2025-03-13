from app.document_loaders.base import DocumentLoader
from pypdf import PdfReader

class PdfLoader(DocumentLoader):
    def load(self, path:str)->str:
        text = ""
        try:
            with open(path, 'rb') as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
                return text
        except FileNotFoundError:
            raise FileNotFoundError(f"File {path} not found") 
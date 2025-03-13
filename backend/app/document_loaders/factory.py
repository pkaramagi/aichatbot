from app.document_loaders.base import DocumentLoader
from app.document_loaders.text_loader import TextLoader
from app.document_loaders.pdf_loader import PdfLoader


class DocumentLoaderFactory:
    @staticmethod
    def get_loader(path:str) -> DocumentLoader:
        if path.endswith('txt'):
            return TextLoader()
        elif path.endswith('pdf'):
            return PdfLoader()
        raise ValueError("Unsupported File Format")
    
    
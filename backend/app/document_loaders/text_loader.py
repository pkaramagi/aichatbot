from app.document_loaders.base import DocumentLoader
class TextLoader(DocumentLoader):
    
    def load(self, path:str) -> str:
        try:
            with open(path,'r') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File {path} not found") 

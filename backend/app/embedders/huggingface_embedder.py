from typing import List
from sentence_transformers import SentenceTransformer
from app.embedders.base import Embedder


class HuggingFaceEmbedder(Embedder):
    def __init__(self, model_name:str = "sentence-transformers/all-MiniLM-L6-v2", device:str = None):
        self.device = device or "cpu"
        self.model = SentenceTransformer(model_name).to(self.device)
        self.embedder_type = "huggingface"
        

    def embed(self, text:str) -> List[float]:
        return self.model.encode(text, convert_to_nuppy=True).tolist()
    
    def embed_batch(self, texts:List[str]) -> List[List[float]]:
        return self.model.encode(texts, convert_to_nuppy=True).tolist()
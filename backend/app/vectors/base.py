from abc import ABC, abstractmethod
from typing import Any, Dict, List

class VectorDB(ABC):
    @abstractmethod
    def save_vectors(self, vectors:List[Dict[str,Any]]):
        pass

    def search_vectors(self, query_vector: List[float], top_k: int = 7):
        pass

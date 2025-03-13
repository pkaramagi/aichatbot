from abc import ABC, abstractmethod
from typing import List
class TextSplitter(ABC):
    @abstractmethod
    def split(self, text:str) -> List[str]:
        pass

    @abstractmethod
    def chunk_text(self, text:str, token_limit:int, model:str)-> List[str]:
        pass
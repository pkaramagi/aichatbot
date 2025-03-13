from typing import List
import tiktoken
from nltk.tokenize import sent_tokenize
from app.helpers.nltk_resource_manager import NLTKResourceManager
from app.text_splitters.base import TextSplitter

class CharacterTextSplitter(TextSplitter):
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        if chunk_size <= 0:
            raise ValueError("Chunk Size must be a positive integer")
        if chunk_overlap < 0:
            raise ValueError("Chunk Overlap must be non-negative")
        if chunk_overlap >= chunk_size:
            raise ValueError ("Chunk Overlap must be less than Chunk Size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text:str) -> List[str]:
        chunks = []
        start_point = 0
        while start_point < len(text):
            end_point = start_point + self.chunk_size
            chunks.append(text[start_point:end_point])
            start_point += (self.chunk_size - self.chunk_overlap)
        return chunks
    
    def chunk_text(self, text:str, token_limit:int, model:str):

        #check if nulk_tab is installed
        nltk_manager = NLTKResourceManager()
        if not nltk_manager.resource_exists:
            nltk_manager.download_resource()
            
        tokenzier = tiktoken.encoding_for_model(model)
        sentences = sent_tokenize(text)

        chunks = []
        current_chunk = []
        current_tokens = 0

        for sentence in sentences:
            token_count = len(tokenzier.encode(sentence))

            if current_tokens + token_count > token_limit:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_tokens = 0

            current_chunk.append(sentence)
            current_tokens += token_count

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks
    
    

        
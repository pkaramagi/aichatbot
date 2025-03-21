from typing import List
from openai import OpenAI, OpenAIError
from app.embedders.base import Embedder
from app.core.config.settings import Settings

class OpenAIEmbedder(Embedder):
    def __init__(self, model_name:str="text-embedding-3-small"):
        self.model_name = model_name
        self.embedder_type = "openai"

    def embed(self, text:str) -> List[float]:
        settings = Settings()
        try:
            
            openai_client = OpenAI(api_key=settings.openai.api_key)

            response = openai_client.embeddings.create(
                model= self.model_name,
                input= text
                )
            return response.data[0].embedding
        except OpenAIError as error:
            raise(OpenAIError(f"OpenAI API Error: {error}"))
        
        return []
        
        

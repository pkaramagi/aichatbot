from app.embedders.base import Embedder
from app.embedders.huggingface_embedder import HuggingFaceEmbedder
from app.embedders.openai_embedder import OpenAIEmbedder
from app.core.config.settings import settings
class EmbedderFactory:
    @staticmethod
    def get_embedder(embedder_type:str) -> Embedder:
        if embedder_type == "openai":
            return OpenAIEmbedder(model_name=settings.openai.model_name)
        elif embedder_type == "huggingface":
            return HuggingFaceEmbedder(model_name=settings.openai.model_name)
        else:
            raise ValueError(f"Invalid vector db type: {embedder_type}")
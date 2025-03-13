from typing import Dict
from app.vectors.base import VectorDB
from app.vectors.chroma_db import ChromaDB
from app.vectors.elastic_search import ElasticSearchDB
from app.core.config.settings import settings
class VectorDBFactory:
    @staticmethod
    def get_vector_db(db_type:str) -> VectorDB:
        if db_type == "chroma":
            return ChromaDB(settings.chroma.collection_name, settings.chroma.persist_dir)
        elif db_type == "elasticsearch":
            return ElasticSearchDB(settings.elasticsearch.host, settings.elasticsearch.port)
        else:
            raise ValueError(f"Invalid vector db type: {db_type}")

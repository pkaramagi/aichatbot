from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv


load_dotenv()

class BaseConfig(BaseSettings):
    
    model_config: ConfigDict = {
        "env_file": ".env",  # Load from .env file
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "env_nested_delimiter": "__",
        "case_sensitive": False
    }

class OpenAIConfig(BaseConfig):
   
    api_key: str = Field(..., env="API_KEY")
    model_name: str = "text-embedding-3-small"
    timeout: int = 30

   
    model_config: ConfigDict = {
        "env_prefix": "DOCVECTOR_OPENAI__",  # Prefix to look for in the environment variables
        "extra": "ignore"
    }

class ElasticSearchConfig(BaseConfig):
    host: str = "localhost"
    port: int = 9200
    user: Optional[str] = None
    password: Optional[str] = None

   
    model_config: ConfigDict = {
        "extra": "ignore"
    }

class ChromaConfig(BaseConfig):
    persist_dir: str = "./chromadb"
    collection_name: str = "documents"

    
    model_config: ConfigDict = {
        "extra": "ignore"
    }

class Settings(BaseConfig):
    environment: str = "development"
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    elasticsearch: ElasticSearchConfig = Field(default_factory=ElasticSearchConfig)
    chroma: ChromaConfig = Field(default_factory=ChromaConfig)

    @property
    def is_production(self) -> bool:
        return self.environment == "production"



settings = Settings()
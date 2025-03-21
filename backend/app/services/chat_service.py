from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from fastapi.responses import StreamingResponse
import asyncio
import openai

from app.embedders.openai_embedder import OpenAIEmbedder
from app.embedders.huggingface_embedder import HuggingFaceEmbedder
from app.vectors.base import VectorDB
from app.embedders.base import Embedder
from app.embedders.factory import EmbedderFactory
from app.vectors.factory import VectorDBFactory
from app.core.config.settings import settings
from app.vectorizer_pipeline import VectorizationPipeline
from app.text_splitters.character_splitter import CharacterTextSplitter


class ChatService:
    def __init__(self):
        self.messages = []
        self.message_id = 0
        self.openai_client = openai.OpenAI(api_key=settings.openai.api_key)


    @property
    def instruction(self):
        instruction ="You are a Customer Chatbot, that provides responses to Clients"
        return instruction

    async def ask_question(self, question:str)-> StreamingResponse:
        embedder = EmbedderFactory.get_embedder("openai")
        vector_db = VectorDBFactory.get_vector_db("chroma")
        async def generate_stream():
            results = self.get_possible_vector(vector_db, embedder, question, top_k=1)
            context = results["documents"][0][0]
            full_prompt = f"""
              System: {self.instruction} \n    
                {context}\n\n 
            """
            gpt_response = self.openai_client.chat.completions.create(
                 model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.instruction},
                    {"role": "system", "content": context},
                     {"role": "user", "content": question}
                ],
                stream=True
            )
            # Stream OpenAI's response
            for chunk in gpt_response:
                if chunk.choices[0].delta.content:
                    yield f"{chunk.choices[0].delta.content}"
            yield "[DONE]\n\n"

        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
        )
            
    def setup(self):
       try:
        docs_path = Path(__file__).resolve().parent.parent / "docs"
        embedder = EmbedderFactory.get_embedder("openai")
        vector_db = VectorDBFactory.get_vector_db("chroma")
        splitter = CharacterTextSplitter()
        vector_pipeline = VectorizationPipeline(embedder=embedder, splitter=splitter, vector_db=vector_db)
        if Path(docs_path).is_dir():
            vector_pipeline.process_directory(docs_path)
        else:
            vector_pipeline.process_document(docs_path)
        
        return {"status": "success", "message": "Setup completed"}
       except Exception as e:
           return {"status": "error", "message": f"Error during setup: {e}"}
        
    def get_possible_vector(self, vector_db: VectorDB, embedder:Embedder, question:str, top_k: int ) -> Dict[str, Any]:
        question_vector = embedder.embed(question)
        results = vector_db.search_vectors(question_vector, top_k)
        return results
       
 
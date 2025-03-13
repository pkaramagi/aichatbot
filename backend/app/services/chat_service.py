from datetime import datetime
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


class ChatService:
    def __init__(self):
        self.messages = []
        self.message_id = 0
        self.openai_client = openai.OpenAI(settings.openai.api_key)


    @property
    def instruction(self):
        instruction ="You are a Customer Chatbot, that provides responses to Clients"
        return instruction

    async def ask_question(self, question:str)-> StreamingResponse:
        embedder = EmbedderFactory.get_embedder("openai")
        vector_db = VectorDBFactory.get_vector_db("chroma")
        async def generate_stream():
            results = self.get_possible_vector(vector_db, embedder, question, top_k=1)
            context = results["document"][0]["text"]
            gpt_response = self.openai_client.completions.create(
                context=context,
                model="gpt-4o",
                input = question,
                stream=True
            )

            for chunk in gpt_response:
                yield chunk
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream"
        )

    
    def get_possible_vector(self, vector_db: VectorDB, embedder:Embedder, question:str, top_k: int ) -> Dict[str, Any]:
        question_vector = embedder.embed(question)
        results = vector_db.search_vectors(question_vector, top_k)
        return results
       
 
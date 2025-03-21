from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.chat import QuestionRequest
from app.services.chat_service import ChatService

router = APIRouter()

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        chat_service = ChatService()
        return await chat_service.ask_question(request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/setup")
def setup():
    chat_service = ChatService()
    return  chat_service.setup()
    

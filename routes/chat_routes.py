from fastapi import APIRouter, status
from services.langchain_service import LangChainService

langchain = LangChainService()


chat_router = APIRouter(
    prefix='/api/v1/llm',
    tags=['Chat Bot']
)






@chat_router.post('/chat', status_code=status.HTTP_201_CREATED)
def chat_with_bot(prompt:str):
    return langchain.chat_with_bot(prompt)

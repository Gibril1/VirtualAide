from fastapi import APIRouter, status
from services.langchain_service import LangChainService
from services.chatbot_services import ChatBotService

langchain = LangChainService()
chat_bot = ChatBotService()

chat_router = APIRouter(
    prefix='/api/v1/llm',
    tags=['Chat Bot']
)






@chat_router.post('/chat', status_code=status.HTTP_201_CREATED)
def chat_with_bot(prompt:str):
    return langchain.chat_with_bot(prompt)


@chat_router.post('/chat/invoke', status_code=status.HTTP_201_CREATED)
def chat_with_llm(prompt:str):
    return chat_bot.invoke_llm(prompt)

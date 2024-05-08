from fastapi import APIRouter, status
from services.fetch_data import MongoDBCrudService
from services.chroma_service import ChromaDBCRUDService
from services.langchain_service import LangChainService

mongo = MongoDBCrudService()
chroma = ChromaDBCRUDService()
langchain = LangChainService()

chroma_router = APIRouter(
    prefix='/api/v1/chroma',
    tags=['Chroma']
)

chat_router = APIRouter(
    prefix='/api/v1/llm',
    tags=['Chat Bot']
)

mongo_router = APIRouter(
    prefix='/api/v1/mongo',
    tags=['MongoDB']
)


@mongo_router.post('/group-chat', status_code=status.HTTP_201_CREATED)
async def add_group_chat_messages_to_chromadb(collection='group-messages'):
    return await mongo.add_records_to_database_group_messages(collection)

@mongo_router.post('/private-chat', status_code=status.HTTP_201_CREATED)
async def add_private_chat_messages_to_chromadb(collection='direct-messages'):
    return await mongo.add_records_to_database_private_messages(collection)

@mongo_router.get('/docs', status_code=status.HTTP_200_OK)
async def get_all_records_from_mongo_collection(collection:str):
    return await mongo.find(collection)

@chroma_router.get('/peek', status_code=status.HTTP_200_OK)
def peek_chroma_collection():
    return chroma.peek_collection()

@chroma_router.get('/all', status_code=status.HTTP_200_OK)
def get_all_collections():
    return chroma.get_all_collections()

@chroma_router.delete('/delete', status_code=status.HTTP_200_OK)
def delete_all_collections():
    return chroma.delete_collections()

@chat_router.post('/chat', status_code=status.HTTP_201_CREATED)
def chat_with_bot(prompt:str):
    return langchain.chat_with_bot(prompt)

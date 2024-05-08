from fastapi import APIRouter, status
from services.fetch_data import MongoDBCrudService
from services.chroma_service import ChromaDBCRUDService
from services.langchain_service import LangChainService

mongo = MongoDBCrudService()
chroma = ChromaDBCRUDService()
langchain = LangChainService()

router = APIRouter(
    prefix='/api/v1/chroma',
    tags=['Chroma']
)

chat_router = APIRouter(
    prefix='/api/v1/llm',
    tags=['Chat Bot']
)


@router.post('/fetch', status_code=status.HTTP_201_CREATED)
async def add_documents_to_chromadb(model:str):
    return await mongo.add_records_to_database_group_messages(model)

@router.get('/peek', status_code=status.HTTP_200_OK)
def peek_chroma_collection():
    return chroma.peek_collection()

@router.get('/docs', status_code=status.HTTP_200_OK)
async def get_all_records(model:str):
    return await mongo.find(model)

@router.get('/all', status_code=status.HTTP_200_OK)
def get_all_collections():
    return chroma.get_all_collections()

@router.delete('/delete', status_code=status.HTTP_200_OK)
def delete_all_collections():
    return chroma.delete_collections()

@chat_router.post('/chat', status_code=status.HTTP_201_CREATED)
def chat_with_bot(prompt:str):
    return langchain.chat_with_bot(prompt)

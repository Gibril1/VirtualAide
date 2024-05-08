from fastapi import status, APIRouter
from services.fetch_data import MongoDBCrudService

mongo = MongoDBCrudService()

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

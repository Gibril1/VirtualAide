from fastapi import APIRouter, status

from services.chroma_service import ChromaDBCRUDService
chroma = ChromaDBCRUDService()


chroma_router = APIRouter(
    prefix='/api/v1/chroma',
    tags=['Chroma']
)

@chroma_router.get('/peek', status_code=status.HTTP_200_OK)
def peek_chroma_collection():
    return chroma.peek_collection()

@chroma_router.get('/all', status_code=status.HTTP_200_OK)
def get_all_collections():
    return chroma.get_all_collections()

@chroma_router.delete('/delete', status_code=status.HTTP_200_OK)
def delete_all_collections():
    return chroma.delete_collections()

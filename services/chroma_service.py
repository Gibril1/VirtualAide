from config.chromadb import ChromaDb
import logging
from fastapi import HTTPException, status


class ChromaDBCRUDService:
    def __init__(
        self,
        embedding_model="text-embedding-ada-002",
        collection_name: str = "ceo_project_collection",
    ):
        self.embedding_model = embedding_model
        chromadb = ChromaDb()
        self.client = chromadb.client
        self.embedding_function = chromadb.ef_function
        self.collection = self.create_collection(collection_name)

    def create_collection(self, name):
        try:
            return self.client.get_or_create_collection(
                name=name, embedding_function=self.embedding_function
            )
        except Exception as e:
            logging.error(f"Error creating collection: {e}")
            raise e
    
    def get_all_collections(self):
        try:
            return self.client.list_collections()
        except Exception as e:
            logging.error(f"Error getting all collections: {e}")
            raise e
        
    def delete_collections(self):
        try:
            collection_names = self.get_all_collections()
            for name in collection_names:
                self.client.delete_collection(name)
            logging.info("Collections deleted successfully")
        except Exception as e:
            logging.error(f"Error deleting collections: {e}")
            raise e

    def add_documents(self, documents, ids):
        try:
            # Add documents to the default collection with metadata and unique IDs
            new_docs = self.collection.add(documents=documents, ids=ids)
            logging.info("Successfully added data to chromaDB")
            return new_docs
        except Exception as e:
            logging.error(f"Error adding data to chromaDB: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    
    def peek_collection(self):
        try:
            return self.collection.peek()
        except Exception as e:
            logging.error(f"Error peeping through the collection. {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

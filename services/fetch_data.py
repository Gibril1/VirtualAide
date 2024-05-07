import logging
from fastapi import HTTPException, status
from config.mongodb import connect_to_database
from services.chroma_service import ChromaDBCRUDService

# init logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

chroma_service = ChromaDBCRUDService()

class MongoDBCrudService:
    def __init__(self) -> None:
        pass

    
    async def find(self, model):
        try:
            db = await connect_to_database()
            logging.info("DB has been connected")
            records = []
            async for record in db[model].find({}):
                records.append(record)
            return {"records": records}
        except Exception as e:
            logging.error(f'Failed to find all records: {str(e)}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to find all records')
        
    
    async def add_records_to_database(self, model):
        try:
            records = await self.find(model)
            # ids = []
            # metadata = []
            # documents = []

            # for record in records:
            #     data = {}
            #     ids.append(record["_id"])
            #     documents.append(record["message"])
            #     data["sender"] = record["sender"]
            #     data["receiver"] = record["receiver"]
            #     data["source"] = record["source"]
            #     data["date"] = record["date"]
            #     data["ref_id"] = record["ref_id"]
            #     metadata.append(data)
            
            # add_documents = chroma_service.add_documents(documents=documents, metadatas=metadata, ids=ids)
            # logging.info(f"All documents have been added to chroma. {add_documents}")
            return records
        except Exception as e:
            logging.error(f'Failed to add records to chroma')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to find all records')

 
import logging
import uuid
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
            async for record in db[model].find({}, {"_id": 0}):
                records.append(record)
            return {"records": records}
        except Exception as e:
            logging.error(f'Failed to find all records: {str(e)}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to find all records')
        
    def template_message_string(self, message, source, date, sender):
        message = f"On {date}, {sender} sent  to his team via {source}, a message with content '{message}"

        return message
    
    def template_message_string_private(self, message, source, date, sender, receiver):
        message = f"On {date}, {sender} sent a message with content '{message}' to {receiver} via {source}"

        return message
    
    async def add_records_to_database_group_messages(self, model):
        try:
            records = await self.find(model)
            ids = [str(uuid.uuid4()) for _ in range(len(records['records']))]
            documents = []

            for record in records['records']:
                message = self.template_message_string(
                    message=record["message"],
                    source=record["source"],
                    date= record["date"],
                    sender=record["sender"]
                )
                documents.append(message)
                logging.info(f'Chroma Docs: {message}')
                
            
            add_documents = chroma_service.add_documents(documents=documents, ids=ids)
            logging.info(f"All documents have been added to chroma. {add_documents}")
            return 1
        except Exception as e:
            logging.error(f'Failed to add records to chroma. {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to add all records')
    
    async def add_records_to_database_private_messages(self, model):
        try:
            records = await self.find(model)
            ids = [str(uuid.uuid4()) for _ in range(len(records['records']))]
            documents = []

            for record in records['records']:
                message = self.template_message_string_private(
                    message=record["message"],
                    source=record["source"],
                    date= record["date"],
                    sender=record["sender"],
                    receiver=record["receiver"]
                )
                documents.append(message)
                logging.info(f'Chroma Docs: {message}')
                
            
            add_documents = chroma_service.add_documents(documents=documents, ids=ids)
            logging.info(f"All documents have been added to chroma. {add_documents}")
            return 1
        except Exception as e:
            logging.error(f'Failed to add records to chroma. {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to add all records')

 
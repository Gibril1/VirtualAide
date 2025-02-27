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
        message = f"On {date}, {sender} sent  to his team via {source}, a message with content '{message}'"

        return message
    
    
    
    async def add_records_to_database_group_messages(self, model):
        try:
            records = await self.find(model)
            length_of_records = len(records["records"])
            ids = [str(uuid.uuid4()) for _ in range(length_of_records)]
            documents = []

            for record in records['records']:
                message_content = record["message"]
                source = record["source"]
                date = record["date"]
                sender = record["sender"]

                message = self.template_message_string(message_content, source, date, sender)
                documents.append(message)
                logging.info(f'Chroma Docs: {message}')
                
            
            add_documents = chroma_service.add_documents(documents=documents, ids=ids)
            logging.info(f"All documents have been added to chroma. {add_documents}")
            return 1
        except Exception as e:
            logging.error(f'Failed to add records to chroma. {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to add all records')
    
    def template_message_string_private(self, message, source, date, sender, receiver):
        if sender == 'user':
            sender = 'CEO'
        elif receiver == 'user':
            receiver = 'CEO'
        message = f"On {date}, {sender} sent a message with content '{message}' to {receiver} via {source}"

        return message
    
    async def add_records_to_database_private_messages(self, model):
        try:
            records = await self.find(model)
            length_of_records = len(records["records"])
            ids = [str(uuid.uuid4()) for _ in range(length_of_records)]

            for index, record in enumerate(records['records']):
                source = record["source"]
                message_content = record["message"]
                sender = record["sender"]
                date = record["date"]
                receiver = record["receiver"]

                
                message = self.template_message_string_private(message_content, source, date, sender, receiver)
                logging.info(f'Chroma Docs: {message}')
                
            
                add_documents = chroma_service.add_documents(documents=message, ids=ids[index])
                logging.info(f"All documents have been added to chroma. {add_documents}")
            return 1
        except Exception as e:
            print(e)
            logging.error(f'Failed to add records to chroma. {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to add all records')

 
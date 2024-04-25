import os
import logging
import chromadb
from dotenv import load_dotenv
from chromadb.utils import embedding_functions

load_dotenv()


class ChromaDb():
    def __init__(self, embedding_model="text-embedding-ada-002"):
        logging.info({"CHROMA_ENDPOINT_IP": 'localhost'})
        self.client = chromadb.HttpClient(host="localhost", port="8000")
        self.ef_function = self.get_openai_ef(model=embedding_model)
        self.heartbeat()

    def get_openai_ef(self, model):
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv('OPENAI_API_KEY'),
            model_name=model
        )
        return openai_ef
    
    def get_collection(self, collection_name):
        return self.client.get_or_create_collection(collection_name, embedding_function=self.ef_function)
    
    def heartbeat(self):
        try:
            self.client.heartbeat()
            logging.info("Connection to Chroma server successful!")
        except Exception as e:
            logging.error(f"Connection to Chroma server failed: {e}")
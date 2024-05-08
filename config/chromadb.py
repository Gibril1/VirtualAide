import os
import logging
import chromadb
from dotenv import load_dotenv
from chromadb.utils import embedding_functions

load_dotenv()

# Init logging
logging.basicConfig(level=logging.INFO)

class ChromaDb():
    def __init__(self):
        logging.info("########ChromaDB instantiating....😁😁######")
        self.client = chromadb.HttpClient(host="localhost", port="8000")
        self.ef_function = self.get_openai_ef()
        self.heartbeat()
        logging.info("####### ChromaDB has finished initialising 🥰🥰####")

    def get_openai_ef(self):
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv('OPENAI_API_KEY'),
            model_name="text-embedding-ada-002"
        )
        return openai_ef
    
    def get_hf_ef(self):
        hf_ef = embedding_functions.HuggingFaceEmbeddingFunction(
            api_key=os.getenv('HF_API_KEY'),
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        return hf_ef
    
    def get_collection(self, collection_name):
        return self.client.get_or_create_collection(collection_name, embedding_function=self.ef_function)
    
    def heartbeat(self):
        try:
            self.client.heartbeat()
            logging.info("Connection to Chroma server successful!😃😃😃")
        except Exception as e:
            logging.error(f"Connection to Chroma server failed: {e}🥲🥲🥲")
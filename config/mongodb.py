import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


load_dotenv()

# Load environment variables
DATABASE_URL = os.getenv('MONGODB_URL')
DATABASE_NAME = os.getenv('MONGO_INITDB_DATABASE')

# Initialize logging
logging.basicConfig(level=logging.INFO)

class MongoDBService:
    client: AsyncIOMotorClient = None # type: ignore

db = MongoDBService()

async def connect_to_database():
    """
    Connect to the MongoDB database and return the database object.
    """
    
    try:
        logging.info("########MongoDB instantiating....😁😁######")
        client = AsyncIOMotorClient(DATABASE_URL)
        await client.admin.command("ping")

        # Log successful connection
        logging.info("Connected to the mongo database.")

        # Return the database object
        return client[DATABASE_NAME]
    except Exception as e:
        # Log connection error
        logging.error(f"Error connecting to the database: {str(e)}🥲🥲🥲")
        return None

async def close_database_connection():
    if db.client is not None:
        db.client.close()
        logging.info('We are closing the database connection')

async def check_db_connection():
    """
    Check the database connection and log available collections.
    """
    # Connect to the database
    database = await connect_to_database()
    if database is not None:
        try:
            # Get the list of available collections in the database
            collection_names = await database.list_collection_names()

            # Log the available collections
            logging.info("Available collections:")
            for collection_name in collection_names:
                logging.info(collection_name)

            return True
        except Exception as e:
            # Log error while listing collections
            logging.error(f"Error listing collections: {str(e)}")
            return False
    else:
        return False




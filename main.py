import os
from fastapi import FastAPI
from config.chromadb import ChromaDb
from config.mongodb import connect_to_database, close_database_connection
from routes.chat_routes import chat_router
from routes.mongo_routes import mongo_router
from routes.chroma_routes import chroma_router
from slack_bolt.adapter.socket_mode import SocketModeHandler
from bot.slack_bot import slack_bot

from dotenv import load_dotenv
load_dotenv()

# app token
APP_TOKEN = os.getenv("APP_TOKEN")

# init app
# app = FastAPI()

# # init chroma
# chroma = ChromaDb()


# # register routes
# app.include_router(mongo_router)
# app.include_router(chroma_router)
# app.include_router(chat_router)



# # register events
# app.add_event_handler('startup', connect_to_database)
# app.add_event_handler('shutdown', close_database_connection)






# @app.get('/')
# def root():
#     return {
#         'message': 'Health check passed✅, server is running💯'
#     }

# start slack bot
SocketModeHandler(slack_bot, APP_TOKEN).start()




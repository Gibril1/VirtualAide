from fastapi import FastAPI
from config.chromadb import ChromaDb
from config.mongodb import connect_to_database, close_database_connection
from routes.chat_routes import router, chat_router
# init app
app = FastAPI()

# init chroma
chroma = ChromaDb()


# register routes
app.include_router(router)
app.include_router(chat_router)


# register events
app.add_event_handler('startup', connect_to_database)
app.add_event_handler('shutdown', close_database_connection)


@app.get('/')
def root():
    return {
        'message': 'Health check passed✅, server is running💯'
    }




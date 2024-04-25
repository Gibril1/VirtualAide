from fastapi import FastAPI
from config.chromadb import ChromaDb
from config.mongodb import connect_to_database, close_database_connection
# init app
app = FastAPI()

# init chroma
chroma = ChromaDb()

# register events
app.add_event_handler('startup', connect_to_database)
app.add_event_handler('shutdown', close_database_connection)


@app.get('/')
def root():
    return {
        'message': 'Health check passed✅, server is running💯'
    }




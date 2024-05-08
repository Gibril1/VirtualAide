import os
import logging
from dotenv import load_dotenv
load_dotenv()
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from services.langchain_service import LangChainService

chat_service = LangChainService()
BOT_TOKEN = os.getenv('BOT_TOKEN')
SIGNING_SECRET = os.getenv('SIGNING_SECRET')

slack_bot = App(token=BOT_TOKEN, signing_secret=SIGNING_SECRET)

@slack_bot.message(".*")
def message_handler(message, say, logger):
    
    logging.info(f"The user message is {message['text']}")
    
    output = chat_service.chat_with_bot(message['text'])   
    logging.info(f"The AI response is {output}")
    say(output)



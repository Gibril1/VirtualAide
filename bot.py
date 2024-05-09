import os
from dotenv import load_dotenv
load_dotenv()
from slack_bolt.adapter.socket_mode import SocketModeHandler
from bot.slack_bot import slack_bot

APP_TOKEN = os.getenv("APP_TOKEN")

SocketModeHandler(slack_bot, APP_TOKEN).start()

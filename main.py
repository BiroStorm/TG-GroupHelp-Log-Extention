import os
import logging
from dotenv import load_dotenv
from telethon.sync import TelegramClient


logging.basicConfig(
    filename='bot.log',
    filemode='a',
    format='[%(levelname)s %(asctime)s] %(name)s: %(message)s',
    level=logging.INFO,
    )

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# We have to manually call "start" if we want an explicit bot token
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# But then we can use the client instance as usual
with bot:
    logging.info("Bot started successfully.")
    # Now you can use the bot instance to interact with Telegram
    print("Bot is running...")
    # Example: Get the bot's own information
    me = bot.get_me()
    print(f"Bot name: {me.first_name}, ID: {me.id}")



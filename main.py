import os
import logging
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon import events

from commands.startcmd import start
from src.database import db, Database
from listener.onMessageInChannel import onMessageInChannel


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


client = TelegramClient('bot', api_id, api_hash)


############# Commands Registration #############
@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await start(event)
    
@client.on(events.NewMessage(pattern='/id'))
async def id_handler(event):
    await event.delete()
    chat = await event.get_chat()
    await event.reply(f"Chat ID: {chat.id}")


################################################################
############# Listener Handlers Registration #############

@client.on(events.NewMessage(chats=[2180748609]))  # Replace 123456789 with your channel/group ID
async def group_message_handler(event):
    await onMessageInChannel(event)
###############################################################


async def main():
    """Start the bot."""
    await client.start(bot_token=bot_token)
    logging.info("Bot started successfully.")
    
    me = await client.get_me()
    
    print(f"Bot name: {me.first_name}, ID: {me.id}")
    
    await client.run_until_disconnected()


if __name__ == '__main__':
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
    finally:
        Database.close_connection()




import logging
from src.database import db


async def onMessageInChannel(event):
    if db is not None:
        logging.info(f"Inserting message into DB: {event.message.text}")
        messages = db.messages
        
        messages.insert_one({'text': event.message.text, 'chat_id': event.chat_id})
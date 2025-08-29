from telethon import events

async def start(event):
    """Send a welcome message when the /start command is issued."""
    await event.respond('Hi! I am your friendly bot assistant.')

from telethon import TelegramClient, events
import asyncio
from fastapi import FastAPI
import uvicorn
import threading

# Telegram credentials
api_id = 26891026
api_hash = '11aacc9305f8896ea752df2eadba203626891026'

client = TelegramClient('session', api_id, api_hash)
replied_users = set()

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:
        user_id = event.sender_id
        if user_id not in replied_users:
            await event.reply("Admin is offline, please try again agle janam.")
            replied_users.add(user_id)

# Start Telegram bot
def start_bot():
    client.start()
    client.run_until_disconnected()

# Keep-alive web server
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bot is online."}

def start_web():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Run both
threading.Thread(target=start_bot).start()
threading.Thread(target=start_web).start()

import os
import asyncio
import requests
from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK")

client = TelegramClient("session", API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    message = event.message

    data = {
        "post_id": message.id,
        "text": message.text or "",
        "media": []
    }

    if message.photo:
        file = await message.download_media(file=bytes)
        data["media"].append({
            "type": "photo",
            "bytes": list(file)
        })

    if message.video:
        file = await message.download_media(file=bytes)
        data["media"].append({
            "type": "video",
            "bytes": list(file)
        })

    try:
        requests.post(N8N_WEBHOOK, json=data, timeout=10)
    except Exception as e:
        print("Webhook error:", e)

async def main():
    await client.start()
    print("Listening channel:", SOURCE_CHANNEL)
    await client.run_until_disconnected()

asyncio.run(main())

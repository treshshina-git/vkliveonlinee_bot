import os
from fastapi import FastAPI, Request

from telegram import Update
from telegram.ext import Application

from bot_logic import setup_bot

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "vkbot_secret")

app = FastAPI()

application = setup_bot(BOT_TOKEN)


@app.on_event("startup")
async def startup():
    await application.initialize()
    await application.bot.set_webhook(
        url=os.getenv("WEBHOOK_URL"),
        secret_token=WEBHOOK_SECRET
    )


@app.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    update = Update.de_json(data, application.bot)

    await application.process_update(update)

    return {"ok": True}
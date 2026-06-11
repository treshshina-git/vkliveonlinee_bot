from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from vk_api import get_online_streams
import os

BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)


async def online(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    streams = get_online_streams()

    streams.sort(
        key=lambda x: x["viewers"],
        reverse=True
    )

    if not streams:
        await update.message.reply_text(
            "Стримы не найдены."
        )
        return

    text = []

    for stream in streams[:20]:

        text.append(
            f"🔴 {stream['title']}\n"
            f"👤 {stream['owner']}\n"
            f"👁 {stream['viewers']}\n"
            f"{stream['url']}"
        )

    await update.message.reply_text(
        "\n\n".join(text)
    )


app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .build()
)

app.add_handler(
    CommandHandler(
        "online",
        online
    )
)

app.run_polling()
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from vk_api import get_online_streams


async def online(update: Update, context: ContextTypes.DEFAULT_TYPE):

    streams = get_online_streams()

    streams.sort(
        key=lambda x: x["viewers"],
        reverse=True
    )

    if not streams:
        await update.message.reply_text("Нет стримов")
        return

    text = []

    for s in streams[:20]:
        text.append(
            f"🔴 {s['title']}\n"
            f"👤 {s['owner']}\n"
            f"👁 {s['viewers']}\n"
            f"{s['url']}"
        )

    await update.message.reply_text("\n\n".join(text))


def setup_bot(token: str):

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("online", online))

    return app
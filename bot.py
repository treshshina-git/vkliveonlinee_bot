from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from vk_api import get_online_streams

TOKEN = "YOUR_TOKEN"


async def online(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    streams = get_online_streams()

    if not streams:
        await update.message.reply_text(
            "Онлайн стримов нет"
        )
        return

    lines = []

    for s in streams[:20]:
        lines.append(
            f"🔴 {s['title']}\n"
            f"👤 {s['author']}\n"
            f"👁 {s['viewers']}\n"
            f"{s['url']}"
        )

    await update.message.reply_text(
        "\n\n".join(lines)
    )


app = (
    ApplicationBuilder()
    .token(TOKEN)
    .build()
)

app.add_handler(
    CommandHandler(
        "online",
        online
    )
)

app.run_polling()
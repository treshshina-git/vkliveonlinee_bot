import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from vk_api import get_online_streams

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/online - онлайн стримы категории Чат Рулетка"
    )


async def online(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    try:
        streams = get_online_streams()

        if not streams:
            await update.message.reply_text(
                "Сейчас нет активных стримов."
            )
            return

        streams.sort(
            key=lambda x: x["viewers"],
            reverse=True
        )

        message_parts = []

        for stream in streams[:20]:
            message_parts.append(
                f"🔴 {stream['title']}\n"
                f"👤 {stream['owner']}\n"
                f"👁 {stream['viewers']}\n"
                f"🔗 {stream['url']}"
            )

        text = "\n\n".join(message_parts)

        if len(text) > 4000:
            text = text[:4000]

        await update.message.reply_text(
            text,
            disable_web_page_preview=True
        )

    except Exception as e:
        await update.message.reply_text(
            f"Ошибка: {str(e)}"
        )


def main():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "online",
            online
        )
    )

    print("Bot started")

    app.run_polling()


if __name__ == "__main__":
    main()

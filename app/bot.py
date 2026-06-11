from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from app.vk_api import get_online_streams
from app.config import TELEGRAM_BOT_TOKEN


def build_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Обновить", callback_data="refresh"),
            InlineKeyboardButton("🔝 ТОП-5", callback_data="top5"),
        ]
    ])


def format_streams(streams):
    return "\n\n".join(
        f"🔴 {s['title']}\n"
        f"👤 {s['owner']}\n"
        f"👁 {s['viewers']}\n"
        f"{s['url']}"
        for s in streams
    )


async def send(update, context, mode="all"):

    streams = get_online_streams()

    streams.sort(key=lambda x: x["viewers"], reverse=True)

    if mode == "top5":
        streams = streams[:5]

    text = format_streams(streams)

    if update.message:
        await update.message.reply_text(
            text,
            reply_markup=build_keyboard(),
            disable_web_page_preview=True
        )
    else:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=build_keyboard(),
            disable_web_page_preview=True
        )


async def online(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send(update, context)


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    if q.data == "refresh":
        await send(update, context)

    elif q.data == "top5":
        await send(update, context, mode="top5")


def setup_app():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("online", online))
    app.add_handler(CallbackQueryHandler(buttons))

    return app
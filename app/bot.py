import os

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
        ]
    ])

def format_streams(streams):
    return "🎹🎹🎹🎹❄❄❄❄🌕🌕🌕🌕\n\n".join(
        f"<a href='<b>{s['owner']}</b> 📢 «{s['title']}»\n"
        #f"◐ ◑\n"
        f"👓 {s['viewers']}</a>\n\n"
        for s in streams
    )
async def send(update, context, mode="all"):
    streams = get_online_streams()
    streams.sort(key=lambda x: x["viewers"], reverse=True)
    text = format_streams(streams)
    if update.message:
        await update.message.reply_text(
            text,
            reply_markup=build_keyboard(),
            disable_web_page_preview=True,
            parse_mode="HTML"
        )
    else:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=build_keyboard(),
            disable_web_page_preview=True,
            parse_mode="HTML"
        )

async def online(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send(update, context)

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "refresh":
        await send(update, context)

def setup_app():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("online", online))
    app.add_handler(CallbackQueryHandler(buttons))
    return app
from multiprocessing import context
import os
from fastapi import FastAPI, Request
from telegram import Update
from app.bot import setup_app
from app.config import (
    TELEGRAM_BOT_TOKEN,
    WEBHOOK_URL,
    WEBHOOK_SECRET, 
    validate_config
)
from app.main import startup


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
from app.vk_api import get_online_sections, get_online_streams
from app.config import TELEGRAM_BOT_TOKEN

def build_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("↪️ Обновить", callback_data="refresh"),
            InlineKeyboardButton("◀️ Назад", callback_data="back"),
        ]
    ])
def format_sections(sections):
    return "".join(
        f"{se['name']}"
        for se in sections
    )
def format_streams(streams):
    return "\n".join(
        f"<b>{s['owner']}</b>       🕶️ {s['viewers']}\n"
        f"📺 {s['title']}\n"
        f"🔗<a href='{s['url']}'>ссылка</a>🔗\n\n"
        for s in streams
    )
async def sendsec(update, context, mode="all"):
    #print("Sections for VK API - 1")    
    sections = get_online_sections()
    #print("Sections received from VK API - ", sections)
    sections.sort(key=lambda x: x["viewers"], reverse=True)
    text = format_sections(sections)
    #print(f"Text: {text}")
    keyboard = [
        [InlineKeyboardButton( f"{sec['name'][:30]}",
                              callback_data=f"section:{sec['id']}")]
        for sec in sections
    ]
    await update.message.reply_text(
        "Выберите раздел:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def send(update, context, mode="all"):
  
    section_id = context.user_data.get("section_id")
    #print(f"context.user_data: {section_id}")
    streams = get_online_streams(section_id)
    streams.sort(key=lambda x: x["viewers"], reverse=True)
    text = format_streams(streams)
    #print(f"Text: {text}")
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
    await sendsec(update, context)

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    #print(f"Callback query data: {q.data}")
    await q.answer()
    if q.data == "refresh":
        await send(update, context)
    if q.data == "back":
        await startup()
    if q.data.startswith("section:"):
        section_id = q.data.split(":")[1]
        #print(f"Selected section ID: {section_id}")
        context.user_data["section_id"] = section_id
        await send(update, context)
    return section_id

def setup_app():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("online", online))
    app.add_handler(CallbackQueryHandler(buttons))
    return app

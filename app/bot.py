from multiprocessing import context
import os
from turtle import update

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
            InlineKeyboardButton("🔄 Обновить", callback_data="refresh"),
        ]
    ])
def format_sections(sections):
    return "".join(
        f"{se['name']}"
        for se in sections
    )
def format_streams(streams):
    return "🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕\n\n".join(
        f"📺 <b>{s['owner']}</b> 📺 \n"
        f"{s['title']}\n"
        f"🕶️ {s['viewers']}              🔗<a href='{s['url']}'>ссылка</a>🔗\n\n"
        for s in streams
    )
async def sendsec(update, context, mode="all"):
    sections = get_online_sections()
    #print("Sections received from VK API - ", sections)
    sections.sort(key=lambda x: x["viewers"], reverse=True)
    text = format_sections(sections)
    print(text)
    for sec in sections:
        sec["name"] = sec["name"][:30] + "..."
    PAGE_SIZE = 20
    page = int(context.user_data.get("page", 0))
    items = sections[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]
    keyboard = [
        [InlineKeyboardButton( sec["name"],
                              callback_data=f"section:{sec['id']}")]
        for sec in sections
    ]
    keyboard.append([
        InlineKeyboardButton("◀", callback_data="page_prev"),
        InlineKeyboardButton("▶", callback_data="page_next"),
    ])
    await update.message.reply_text(
        "Выберите раздел:",
        reply_markup=InlineKeyboardMarkup(keyboard)
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
    await sendsec(update, context)

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "refresh":
        await sendsec(update, context)
    if q.data.startswith("section:"):
        section_id = q.data.split(":")[1]
        context.user_data["section_id"] = section_id
        await send(update, context)
def setup_app():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("online", online))
    app.add_handler(CallbackQueryHandler(buttons))
    return app

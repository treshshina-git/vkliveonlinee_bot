
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from app.vk_api import get_online_streams, get_categories
from app.config import TELEGRAM_BOT_TOKEN

selected_category = {}

def build_keyboard(categories):
    rows = [[InlineKeyboardButton("🔄 Обновить", callback_data="refresh")]]
    for cat in categories[:20]:
        rows.append([InlineKeyboardButton(cat["title"][:40], callback_data=f'cat:{cat["id"]}')])
    return InlineKeyboardMarkup(rows)

def format_streams(streams):
    if not streams:
        return "Стримы не найдены."
    return "\n\n".join(
        f"🔴 {s['title']}\n👤 {s['owner']} - {s['url']}\n👁 {s['viewers']}"
        for s in streams
    )

async def send(update, context):
    user_id = update.effective_user.id
    category_id = selected_category.get(user_id)

    streams = get_online_streams(category_id)
    streams.sort(key=lambda x: x["viewers"], reverse=True)

    text = format_streams(streams)
    kb = build_keyboard(get_categories())

    if update.message:
        await update.message.reply_text(text, reply_markup=kb, disable_web_page_preview=True)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=kb, disable_web_page_preview=True)

async def online(update, context):
    await send(update, context)

async def buttons(update, context):
    q = update.callback_query
    await q.answer()

    if q.data == "refresh":
        await send(update, context)
    elif q.data.startswith("cat:"):
        selected_category[q.from_user.id] = q.data.split(":",1)[1]
        await send(update, context)

def setup_app():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("online", online))
    app.add_handler(CallbackQueryHandler(buttons))
    return app

import os
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TOKEN_VK_URL = os.getenv("TOKEN_VK_URL")
VK_CLIENT_ID = os.getenv("VK_CLIENT_ID")
VK_CLIENT_SECRET = os.getenv("VK_CLIENT_SECRET")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "vk_live_bot")
API_default_section_ID = os.getenv("API_default_section_ID")
API_active_channels = os.getenv("API_active_channels")
API_online_categories = os.getenv("API_online_categories")
API_category_search = os.getenv("API_category_search")
API_online_channels = os.getenv("API_online_channels")

def validate_config():
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")

    if not VK_CLIENT_ID:
        missing.append("VK_CLIENT_ID")

    if not VK_CLIENT_SECRET:
        missing.append("VK_CLIENT_SECRET")

    if not WEBHOOK_URL:
        missing.append("WEBHOOK_URL")

    if missing:
        raise RuntimeError(
            f"Missing env vars: {', '.join(missing)}"
        )

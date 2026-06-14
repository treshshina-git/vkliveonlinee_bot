
import requests
from app.token_manager import get_access_token
from app.config import DEFAULT_CATEGORY_ID

API_URL = "https://apidev.live.vkvideo.ru/v1/catalog/online_channels"
CATEGORIES_URL = "https://apidev.live.vkvideo.ru/v1/catalog/categories"


def get_categories():
    token = get_access_token()
    r = requests.get(
        CATEGORIES_URL,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30
    )
    r.raise_for_status()
    data = r.json()

    categories = []
    for item in data.get("data", {}).get("categories", []):
        categories.append({
            "id": item.get("id"),
            "title": item.get("title", "Без названия")
        })
    return categories


def get_online_streams(category_id=None):
    token = get_access_token()

    category_id = category_id or DEFAULT_CATEGORY_ID

    params = {
        "limit": 200,
        "offset": 0,
        "all_streams": True,
        "has_vk_video": True
    }

    if category_id:
        params["category_id"] = category_id

    r = requests.get(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30
    )

    r.raise_for_status()

    data = r.json()
    streams = []

    for item in data.get("data", {}).get("channels", []):
        stream = item.get("stream", {})
        owner = item.get("owner", {})
        channel = item.get("channel", {})

        streams.append({
            "title": stream.get("title", "No title"),
            "viewers": stream.get("counters", {}).get("viewers", 0),
            "owner": owner.get("nick", "unknown"),
            "url": channel.get("url", "")
        })

    return streams

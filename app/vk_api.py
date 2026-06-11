import requests
from app.token_manager import get_access_token
from app.config import CHAT_RULETTE_CATEGORY_ID

API_URL = "https://apidev.live.vkvideo.ru/v1/catalog/online_channels"


def get_online_streams():

    token = get_access_token()

    r = requests.get(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        params={
            "limit": 200,
            "offset": 0,
            "category_id": CHAT_RULETTE_CATEGORY_ID,
            "all_streams": True,
            "has_vk_video": True
        },
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
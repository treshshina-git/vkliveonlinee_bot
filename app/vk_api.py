import requests
from app.token_manager import get_access_token
from app.config import CHAT_RULETTE_CATEGORY_ID, API_URL
API_URL1 = "https://apidev.live.vkvideo.ru/v1/catalog/online_categories"
def get_online_streams():
    token = get_access_token()
    r = requests.get(
        API_URL1,
        headers={"Authorization": f"Bearer {token}"},
        params={
            "limit": 200,
            "offset": 0,
            "category_type": ""
        },
        timeout=30
    )

    r.raise_for_status()
    data = r.json()
    print(data.get("id"), data.get("cover_url") )
    print(data)
    streams = []
    for item in data.get("data", {}).get("channels", []):
        stream = item.get("stream", {})
        owner = item.get("owner", {})
        channel = item.get("channel", {})
        uri = channel.get("url", "")
        urik = "https://live.vkvideo.ru/" + uri
        streams.append({
            "title": stream.get("title", "No title"),
            "viewers": stream.get("counters", {}).get("viewers", 0),
            "owner": owner.get("nick", "unknown"),
            "url": urik
        })
    return streams
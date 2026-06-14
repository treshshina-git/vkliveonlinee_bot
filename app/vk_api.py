
import requests
from app.token_manager import get_access_token
from app.config import DEFAULT_CATEGORY_ID, API_URL, CATEGORY_API_URL

def get_categories():

    token = get_access_token()

    r = requests.get(
        CATEGORY_API_URL,
        headers={"Authorization": f"Bearer {token}"},
        params={
            "query": "",
            "type": "chat",
            "limit": 100
        },
        timeout=30
    )
    print(r)
    r.raise_for_status()

    data = r.json()
    print(data)
    return [
        {
            "id": item["id"],
            "title": item["title"]
        }
        for item in data.get("data", {}).get("categories", [])
    ]

def get_online_streams(category_id):
    token = get_access_token()

    category_id = category_id or DEFAULT_CATEGORY_ID

    params={
        "limit": 200,
        "offset": 0,
        "category_id": category_id,
        "all_streams": True,
        "has_vk_video": True
    }

    if category_id:
        params["category_id"] = category_id

    r1 = requests.get(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30
    )

    r1.raise_for_status()

    data = r1.json()
    streams = []

    for item in data.get("data", {}).get("channels", []):
        print(item.keys())
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

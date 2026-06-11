import requests
from token_manager import get_access_token

API_URL = "https://apidev.live.vkvideo.ru/v1/catalog/online_channels"

CATEGORY_ID = "6abff723-68ea-4c47-8df1-55573d362749"


def get_online_streams():

    token = get_access_token()

    r = requests.get(
        API_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        params={
            "limit": 200,
            "offset": 0,
            "category_id": CATEGORY_ID,
            "all_streams": True,
            "has_vk_video": True
        },
        timeout=30
    )

    r.raise_for_status()

    data = r.json()

    result = []

    for item in data["data"]["channels"]:
        stream = item["stream"]

        result.append({
            "title": stream["title"],
            "viewers": stream["counters"]["viewers"],
            "owner": item["owner"]["nick"],
            "url": item["channel"]["url"]
        })

    return result

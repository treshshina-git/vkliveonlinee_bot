import requests

from token import get_access_token

API_URL = (
    "https://apidev.live.vkvideo.ru"
    "/v1/catalog/online_channels"
)

CHAT_RULETTE_CATEGORY = (
    "6abff723-68ea-4c47-8df1-55573d362749"
)


def get_online_streams():

    token = get_access_token()

    response = requests.get(
        API_URL,
        headers={
            "Authorization":
                f"Bearer {token}"
        },
        params={
            "limit": 200,
            "offset": 0,
            "category_id":
                CHAT_RULETTE_CATEGORY,
            "all_streams": True,
            "has_vk_video": True
        },
        timeout=30
    )

    response.raise_for_status()

    payload = response.json()

    streams = []

    for channel in payload["data"]["channels"]:

        stream = channel["stream"]

        streams.append({
            "title": stream["title"],
            "viewers":
                stream["counters"]["viewers"],
            "owner":
                channel["owner"]["nick"],
            "url":
                channel["channel"]["url"],
            "stream_id":
                stream["id"]
        })

    return streams
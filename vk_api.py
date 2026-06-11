import requests

from token_manager import get_access_token

API_URL = (
    "https://apidev.live.vkvideo.ru"
    "/v1/catalog/online_channels"
)

CATEGORY_ID = (
    "6abff723-68ea-4c47-8df1-55573d362749"
)


def get_online_streams(
    limit=200,
    offset=0
):
    token = get_access_token()

    response = requests.get(
        API_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        params={
            "limit": limit,
            "offset": offset,
            "category_id": CATEGORY_ID,
            "all_streams": True,
            "has_vk_video": True
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    streams = []

    for item in data["data"]["channels"]:
        stream = item["stream"]

        streams.append({
            "id": stream["id"],
            "title": stream["title"],
            "viewers": stream["counters"]["viewers"],
            "owner": item["owner"]["nick"],
            "url": item["channel"]["url"]
        })

    return streams

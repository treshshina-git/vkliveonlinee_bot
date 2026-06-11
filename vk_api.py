import requests

from vk_token_manager import (
    get_access_token,
    clear_token_cache
)

API_URL = (
    "https://apidev.live.vkvideo.ru"
    "/v1/catalog/online_channels"
)

CHAT_RULETTE_CATEGORY_ID = (
    "6abff723-68ea-4c47-8df1-55573d362749"
)


def _request_streams(token):
    return requests.get(
        API_URL,
        headers={
            "Authorization":
                f"Bearer {token}",
            "Accept":
                "application/json"
        },
        params={
            "limit": 200,
            "offset": 0,
            "category_id":
                CHAT_RULETTE_CATEGORY_ID,
            "all_streams": True,
            "has_vk_video": True
        },
        timeout=30
    )


def get_online_streams():
    token = get_access_token()

    response = _request_streams(token)

    if response.status_code == 401:
        clear_token_cache()

        token = get_access_token()

        response = _request_streams(token)

    response.raise_for_status()

    payload = response.json()

    result = []

    channels = (
        payload
        .get("data", {})
        .get("channels", [])
    )

    for item in channels:
        stream = item.get("stream", {})
        owner = item.get("owner", {})
        channel = item.get("channel", {})

        result.append({
            "id": stream.get("id"),
            "title": stream.get(
                "title",
                "Без названия"
            ),
            "viewers": (
                stream
                .get("counters", {})
                .get("viewers", 0)
            ),
            "owner": owner.get(
                "nick",
                "Unknown"
            ),
            "url": channel.get(
                "url",
                ""
            )
        })

    return result

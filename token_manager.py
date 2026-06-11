import os
import time
import base64
import requests

TOKEN_URL = (
    "https://api.live.vkvideo.ru/oauth/server/token"
)

CLIENT_ID = os.getenv("VK_CLIENT_ID")
CLIENT_SECRET = os.getenv("VK_CLIENT_SECRET")

_cached_token = None
_token_expires_at = 0


def _request_new_token():
    credentials = (
        f"{CLIENT_ID}:{CLIENT_SECRET}"
    )

    encoded = base64.b64encode(
        credentials.encode()
    ).decode()

    response = requests.post(
        TOKEN_URL,
        headers={
            "Authorization": f"Basic {encoded}",
            "Content-Type":
                "application/x-www-form-urlencoded"
        },
        data={
            "grant_type":
                "client_credentials"
        },
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def get_access_token():
    global _cached_token
    global _token_expires_at

    now = int(time.time())

    if (
        _cached_token
        and now < (_token_expires_at - 60)
    ):
        return _cached_token

    token_data = _request_new_token()

    _cached_token = token_data["access_token"]

    expire_time = token_data.get(
        "expire_time",
        3600
    )

    _token_expires_at = now + expire_time

    return _cached_token


def clear_token_cache():
    global _cached_token
    global _token_expires_at

    _cached_token = None
    _token_expires_at = 0

import os
import base64
import requests
import sys

if os.getenv("RAILWAY_ENVIRONMENT"):
    print("Running on Railway - single instance expected")
    
TOKEN_URL = (
    "https://api.live.vkvideo.ru/oauth/server/token"
)

CLIENT_ID = os.getenv("VK_CLIENT_ID")
CLIENT_SECRET = os.getenv("VK_CLIENT_SECRET")

if not CLIENT_ID:
    raise RuntimeError(
        "VK_CLIENT_ID not set"
    )

if not CLIENT_SECRET:
    raise RuntimeError(
        "VK_CLIENT_SECRET not set"
    )


def get_access_token():
    credentials = (
        f"{CLIENT_ID}:{CLIENT_SECRET}"
    )

    encoded = base64.b64encode(
        credentials.encode("utf-8")
    ).decode("utf-8")

    response = requests.post(
        TOKEN_URL,
        headers={
            "Authorization": f"Basic {encoded}",
            "Content-Type": (
                "application/x-www-form-urlencoded"
            )
        },
        data={
            "grant_type": "client_credentials"
        },
        timeout=30
    )

    response.raise_for_status()

    payload = response.json()

    return payload["access_token"]


def clear_token_cache():
    pass

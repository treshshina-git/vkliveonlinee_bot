import os
import base64
import requests

TOKEN_URL = (
    "https://api.live.vkvideo.ru/oauth/server/token"
)

CLIENT_ID = os.getenv("VK_CLIENT_ID")
CLIENT_SECRET = os.getenv("VK_CLIENT_SECRET")


def get_access_token():

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

    data = response.json()

    return data["access_token"]
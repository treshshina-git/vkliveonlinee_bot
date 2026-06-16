import requests
from app.token_manager import get_access_token
from app.config import CHAT_RULETTE_CATEGORY_ID, API_URL_STREAMS, API_URL_SECTIONS
def get_online_streams():
    token = get_access_token()
    section_id = user.data.get("section_id")
    if section_id 
    else CHAT_RULETTE_CATEGORY_ID
    print(f"Streams: {section_id}")
    r = requests.get(
        API_URL_STREAMS,
        headers={"Authorization": f"Bearer {token}"},
        params={
            "limit": 100,
            "offset": 0,
            "category_id": section_id,
            "all_streams": True,
            "has_vk_video": True
        },
        timeout=30
    )
    r.raise_for_status()
    data = r.json()
    #print("Data received from VK API - ", data)
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

def get_online_sections():
    token = get_access_token()
    r = requests.get(
        API_URL_SECTIONS,
        headers={"Authorization": f"Bearer {token}"},
        params={
            "limit": 50,
            "offset": 0,
            "category_type": ""
        },
        timeout=30
    )
    r.raise_for_status()
    data = r.json()
    dar = data.get("data", {}).get("categories", [])
    #print("Data received from VK API - ", data)
    sections = []
    for item in dar:
        sections.append({
            "id": item.get("id"),
            "name": item.get("title"),
            "viewers": item.get("counters", {}).get("viewers", 0)
        })
    return sections

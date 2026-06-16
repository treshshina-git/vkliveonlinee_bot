import requests
from app.token_manager import get_access_token
from app.config import API_default_section_ID, TOKEN_VK_URL, API_active_channels, API_online_categories, API_category_search, API_online_channels

def get_online_streams(section_id=None):
    token = get_access_token()
    #print(f"Fetching streams for section ID: {section_id}")
    r = requests.get(
        API_online_channels,
        headers={"Authorization": f"Bearer {token}"},
        params={
            "limit": 50,
            "offset": 0,
            "category_id": section_id,
            "all_streams": True,
            "has_vk_video": False,
            "category_type": "irl",
            "all_streams": True,
        },
        timeout=30
    )
    r.raise_for_status()
    data = r.json()
    streams = []
    for item in data.get("data", {}).get("channels", []):
        stream = item.get("stream", {})
        #owner = item.get("owner", {})
        owner = item.get("owner", {}).get("nick", "unknown")
        channel = item.get("channel", {})
        uri = channel.get("url", "")
        urik = "https://live.vkvideo.ru/" + uri
        streams.append({
            "title": stream.get("title", "No title")[:30],
            "viewers": stream.get("counters", {}).get("viewers", 0),
            "owner": owner.get("nick", "unknown")[:30],
            "url": urik
        })
    return streams

def get_online_sections():
    token = get_access_token()
    r = requests.get(
        API_online_categories,
        headers={"Authorization": f"Bearer {token}"},
        params={
            "limit": 30,
            #"query": "",
            #"type": ""
            "offset": 0,
            "category_type": "irl",
            #"has_vk_video": False,
            #"all_streams": True
        },
        timeout=30
    )
    r.raise_for_status()
    data = r.json()
    #print("Sections from VK API - ", data)
    dar = data.get("data", {}).get("categories", [])
    sections = []
    for item in dar:
        sections.append({
            "id": item.get("id"),
            "name": item.get("title")[:30],
            "viewers": item.get("counters", {}).get("viewers", 0)
        })
    #print("Parsed sections - ", sections)
    #if not sections: sections = [{"id": API_default_section_ID, "name": "Чат Рулетка", "viewers": 0}]
    return sections

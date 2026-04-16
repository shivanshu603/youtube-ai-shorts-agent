import requests
import os

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def fetch_video(query, output_path):
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1}

    res = requests.get(url, headers=headers, params=params).json()

    try:
        video_url = res["videos"][0]["video_files"][0]["link"]
    except:
        print("⚠️ No video found, using fallback image")
        return None

    video_data = requests.get(video_url).content

    with open(output_path, "wb") as f:
        f.write(video_data)

    return output_path

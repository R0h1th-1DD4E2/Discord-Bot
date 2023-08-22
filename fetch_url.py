import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('YOUTUBE_API')

def search_lofi_music():
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": token,
        "part": "snippet",
        "q": "high on life",
        "type": "video",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        videos = data["items"]
        if not videos:
            print("No videos found.")
            return None
        if videos:
            video_id = videos[0]['id']['videoId']
            open_url = "https://www.youtube.com/watch?v=" + video_id
            return open_url
        else:
            return 1
    else:
        print("Error:", response.status_code)
        return None
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google_auth_oauthlib

import json

### global constants
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# fetches the latest video uploaded by each channel id in "channels"
def poll(channels, devkey):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=devkey)

    for ch in channels:
        request = youtube.activities().list(
            part="snippet,contentDetails",
            channelId=ch,
            maxResults=1
        )

        response = request.execute()

        title = json.dumps(response["items"][0]["snippet"]["title"])
        id = json.dumps(response["items"][0]["contentDetails"]["upload"]["videoId"])

        print(title)
        print(id)
        print()

# main
with open("config.json") as config:
    data = json.load(config)
    devkey = data["youtubeAPIKey"]
    channels = data["channels"]
    poll(channels, devkey)
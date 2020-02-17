import json

# youtube
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google_auth_oauthlib

# TODO: Make a proper interface using metaclasses
class AbstrctAPIInterface:
    def poll(self):
        pass
    
    def createMessage(self):
        pass


class YouTubeAPI(AbstrctAPIInterface):
    def __init__(self):
        # constants
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
        
        # build api info from config file
        with open("config.json") as config:
            data = json.load(config)
            self.key = data["youtubeAPIKey"]
            self.channels = data["channels"]

        # build youtube api
        self.api = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self.key)

    def poll(self):
        for ch in self.channels:
            request = self.api.activities().list(
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

yt = YouTubeAPI()
yt.poll()
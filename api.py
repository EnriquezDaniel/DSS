import json

# youtube
import google_auth_oauthlib
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


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
        result = []

        for ch in self.channels:
            request = self.api.activities().list(
                part="snippet,contentDetails",
                channelId=ch,
                maxResults=1
            )

            response = request.execute()

            title = json.dumps(response["items"][0]["snippet"]["title"])
            title = title.strip("\"")

            videoID = json.dumps(response["items"][0]["contentDetails"]["upload"]["videoId"])
            videoID = videoID.strip("\"") #videoID initially has a pair of quotes surrounding it

            link = "https://www.youtube.com/watch?v=" + videoID
            result.append(dict([("title", title), ("link", link)])) #adds a new entry to the result

        return result
        
    def createMessage()

yt = YouTubeAPI()
temp = yt.poll()

for d in temp:
    print(d["title"])
    print(d["link"])
    print()
import json

# youtube
import google_auth_oauthlib
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# utility functions



# TODO: Make a proper interface using metaclasses
class AbstractAPIInterface:
    def poll(self):
        pass
    
    def createMessages(self):
        pass


class YouTubeAPI(AbstractAPIInterface):
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
        self.api = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=self.key
        )

        #should we store this info in program memory or a file?
        self.currResults = []
        self.prevResults = [] #should probably be stored in a file before shutdown

    def poll(self):
        #if len(self.currResults) == 0
        self.prevResults = self.currResults
        self.currResults = []

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
            self.currResults.append(
                dict([("title", title), ("link", link)]) #adds a new entry to the result
            )

        # check for changed results, add them to a new list,
        # create a list of messages, and return the messages
        newResults = []
        for d in self.currResults:
            if d in self.prevResults: #also try "not in"
                continue
            newResults.append(d)
        
        return self.createMessages(newResults)

    # in a perfect world this would be a private method,
    # (ie: don't call this from outside the class)
    # in an even better world this would be a global function b/c abstraction is nice
    def createMessages(self, results):
        if len(results) == 0:
            print("YOUTUBE: no messages to create")
            return []

        msgs = []
        for r in results:
            msg = r["title"] + "\n" + r["link"]
            msgs.append(msg)
        return msgs

    # debug function (maybe future "refresh" (?) command)
    # that returns a list of mesages for all entries in self.currResults
    def createAllMessages():
        msgs = []
        for r in self.currResults:
            msg = r["title"] + "\n" + r["link"]
            msgs.append(msg)
        return msgs

### main for testing
yt = YouTubeAPI()

for i in range(2):
    for m in yt.poll():
        print(m)
    print()
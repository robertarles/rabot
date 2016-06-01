import feedparser


class RaGatherer():

    def __init__(self, target_url):
        self.target_url = target_url

    def check(self):
        self.feed = feedparser.parse(self.target_url)
        return self.feed["items"]

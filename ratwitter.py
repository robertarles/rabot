import tweepy


class RaTwitter():

    # configuration for sending as rabot32
    def __init__(self):
        self.consumer_key = "YpKKXQkQZD2JPfbrFzpWhrGRG"
        self.consumer_secret = "fQLgWCzoLvUEpEdTybrQAGCku2ehOWOUOGZVgV7HVR00S062Tk"
        self.access_token = "726290531471380480-Au9KIC1TPmXdo5OlGrvejWL0PGZ4I8e"
        self.access_token_secret = "fSLBW4N3Ko0cvilbczUVp8bSLLLOQoXLvQqGz40zkWNxk"

    def direct_message(self, handle, message):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        api.send_direct_message(user=handle, text=message)
        # public_tweets = api.home_timeline()
        # for tweet in public_tweets:
        #     print(tweet.text)
        # for member in inspect.getmembers(api):
        #     print(member)  # direct_message("metabot32", "testing")


if __name__ == '__main__':
    RaTwitter.direct_message('metabot32', 'chimichangaless')

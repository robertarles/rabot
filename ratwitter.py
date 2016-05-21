import tweepy
import os
class RaTwitter():

    # configuration for sending as rabot32
    def __init__(self):
        self.secrets = None
        # read the twitter api secrets from ~/.twitter
        with open((os.path.expanduser('~') + '/.twitter'), 'r') as f:
            self.secrets = dict([line.strip().split('=') for line in f])

    def direct_message(self, handle, message):
        auth = tweepy.OAuthHandler(self.secrets["consumer_key"], self.secrets["consumer_secret"])
        auth.set_access_token(self.secrets["access_token"], self.secrets["access_token_secret"])
        api = tweepy.API(auth)
        api.send_direct_message(user=handle, text=message)
        # public_tweets = api.home_timeline()
        # for tweet in public_tweets:
        #     print(tweet.text)
        # for member in inspect.getmembers(api):
        #     print(member)  # direct_message("metabot32", "testing")


if __name__ == '__main__':
    rat = RaTwitter()
    rat.direct_message('metabot32', 'chimichangaless')

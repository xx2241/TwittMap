import json
import tweepy
from elasticsearch import Elasticsearch


class TweetStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print status.text

    def on_error(self, status_code):
        if status_code == 420:
            return False


def getCredentials():
    with open('../config.txt', 'rb') as configfile:
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET = configfile.read().splitlines()
        configfile.close()
    return CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET


def main():
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET = getCredentials()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    tweetStreamListener = TweetStreamListener()
    tweetStream = tweepy.Stream(auth=api.auth, listener=tweetStreamListener)
    tweetStream.filter(track=['Trump'], async=True)


if __name__ == '__main__':
    main()

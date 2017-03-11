import json
import tweepy
import requests
from elasticsearch import Elasticsearch
from datetime import datetime


FILTERED_KEYWORDS = ['Trump', 'China', 'Python']


class TweetStreamListener(tweepy.StreamListener):
    def __init__(self, es):
        self.es = es

    def on_data(self, data):
        # Load the json to a string
        cur_data = json.loads(data)
        location = cur_data['user']['location']
        if location:
            print location
            text = cur_data['text']

            for keyword in FILTERED_KEYWORDS:
                if keyword in text:
                    keyword = keyword
                    break
                else:
                    keyword = None

            api_key = "AIzaSyAWjWqvTQl4mrI1dUPJzdJO9O2HyG4Trkc"
            api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(location, api_key))
            api_response_dict = api_response.json()
            if api_response_dict['status'] == "OK":
                latitude = api_response_dict['results'][0]['geometry']['location']['lat']
                longitude = api_response_dict['results'][0]['geometry']['location']['lng']
                coordinates = [latitude, longitude]
            else:
                coordinates = None

            print keyword
            print coordinates
            mapping = {
                'keyword': keyword,
                'author': cur_data['user']['screen_name'],
                'text': text,
                'timestamp': datetime.now(),
                'location': location,
                'coordinates': coordinates
            }

            res = self.es.index(index="test-index", doc_type='tweet', id=cur_data['user']['id'], body=mapping)
            print(res['created'])

        return True


    def on_status(self, status):
        print ("Status: " + status.text)


    def on_error(self, status_code):
        print ("Tweepy Error: " + str(status_code))
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
    es = Elasticsearch()
    tweetStreamListener = TweetStreamListener(es)
    tweetStream = tweepy.Stream(auth=api.auth, listener=tweetStreamListener)
    tweetStream.filter(track=FILTERED_KEYWORDS, async=True)


if __name__ == '__main__':
    main()

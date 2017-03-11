import json
import tweepy
import requests
from elasticsearch import Elasticsearch
from dateutil import parser
from datetime import datetime


FILTERED_KEYWORDS = ['Trump', 'China', 'Python']


class TweetStreamListener(tweepy.StreamListener):
    def __init__(self, es):
        self.es = es

    def on_data(self, data):
        try:
            cur_data = json.loads(data)
            location = cur_data['user']['location']
            if location and cur_data['lang'] == 'en':
                text = cur_data['text']
                keyword = getKeyWord(text)
                api_key = getApiKey()
                coordinates = getCoordinates(api_key, location)
                timestamp = parser.parse(cur_data['created_at'])
                timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
                if keyword and coordinates:
                    mapping = {
                        'keyword': keyword,
                        'author': cur_data['user']['screen_name'],
                        'text': text,
                        'timestamp': timestamp,
                        'coordinates': coordinates,
                    }
                    try:
                        res = self.es.index(index="twittmap", doc_type='tweet', id=cur_data['user']['id'], body=mapping)
                        print ("Push Status: ", res['created'])
                    except:
                        print ("Error Here!")
        except Exception as e:
            print (str(e))

    def on_status(self, status):
        print ("Status: " + status.text)

    def on_error(self, status_code):
        print ("Tweepy Error: " + str(status_code))
        return False


def getCoordinates(api_key, location):
    api_key = api_key.decode('utf-8')
    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(location, api_key))
    api_response_dict = api_response.json()
    if api_response_dict['status'] == "OK":
        latitude = api_response_dict['results'][0]['geometry']['location']['lat']
        longitude = api_response_dict['results'][0]['geometry']['location']['lng']
        coordinates = [latitude, longitude]
    else:
        coordinates = None
    return coordinates


def getKeyWord(text):
    for keyword in FILTERED_KEYWORDS:
        if keyword in text:
            keyword = keyword
            break
        else:
            keyword = None
    return keyword


def getApiKey():
    with open('../config.txt', 'rb') as configfile:
        api_key = configfile.read().splitlines()[5]
        configfile.close()
    return api_key


def getCredentials():
    with open('../config.txt', 'rb') as configfile:
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, END_POINT = configfile.read().splitlines()[0:5]
        configfile.close()
    return CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, END_POINT


def main():
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, END_POINT = getCredentials()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    es = Elasticsearch(hosts=END_POINT, port=443, use_ssl=True)
    tweetStreamListener = TweetStreamListener(es)
    tweetStream = tweepy.Stream(auth=api.auth, listener=tweetStreamListener)
    tweetStream.filter(track=FILTERED_KEYWORDS, async=True)


if __name__ == '__main__':
    main()

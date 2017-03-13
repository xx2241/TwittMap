import sys
import json
import tweepy
import requests
import math
import time
from elasticsearch import Elasticsearch
from dateutil import parser
from datetime import datetime
import urllib3
urllib3.disable_warnings()

if sys.version_info[0] == 2:
    from httplib import IncompleteRead
else:
    from http.client import IncompleteRead


FILTERED_KEYWORDS = ['Trump', 'China', 'Amazon', 'Football', 'Dinner', 'Google', 'Love', 'Facebook', 'Apple', 'Chicken']


class TweetStreamListener(tweepy.StreamListener):
    def __init__(self, es):
        self.es = es
        self.rate = 0
        self.other = 0

    def on_data(self, data):
        try:
            cur_data = json.loads(data)
            location = cur_data['user']['location']
            if location:
                text = cur_data['text']
                keyword = getKeyWord(text)
                api_key = getApiKey()
                coordinates = getCoordinates(api_key, location)
                timestamp = parser.parse(cur_data['created_at'])
                timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
                author = cur_data['user']['screen_name']
                if (keyword and coordinates):
                    mapping = {
                        'keyword': keyword,
                        'author': author,
                        'text': text,
                        'timestamp': timestamp,
                        'coordinates': coordinates,
                    }
                    try:
                        res = self.es.index(index="twittmap", doc_type='tweet', id=cur_data['user']['id'], body=mapping)
                        print ("Push Status: ", res['created'])
                    except:
                        pass
                else:
                    print ("Unstructured data! Pass!")
            else:
                print ("No location information! Pass!")
        except Exception as e:
            print (e)

    def on_status(self, status):
        print ("Status: " + status.text)

    def on_error(self, status_code):
        print ('Error:', str(status_code))
        if status_code == 420:
            print ("Rate Limited!")
            sleepy = 60 * math.pow(2, self.rate)
            print (time.strftime("%Y%m%d_%H%M%S"))
            print ("A reconnection attempt will occur in " + \
            str(sleepy/60) + " minutes.")
            time.sleep(sleepy)
            self.rate += 1
        else:
            sleepy = 5 * math.pow(2, self.other)
            print (time.strftime("%Y%m%d_%H%M%S"))
            print ("A reconnection attempt will occur in " + \
            str(sleepy) + " seconds.")
            time.sleep(sleepy)
            self.other += 1
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
        if (keyword in text or keyword.lower() in text or keyword.upper() in text):
            keyword = keyword
            break
        else:
            keyword = None
    return keyword


def getApiKey():
    with open('./config.txt', 'rb') as configfile:
        api_key = configfile.read().splitlines()[5]
        configfile.close()
    return api_key


def getCredentials():
    with open('./config.txt', 'r') as configfile:
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, END_POINT = configfile.read().splitlines()[0:5]
        configfile.close()
    return CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, END_POINT


def main():
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, END_POINT = getCredentials()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    es = Elasticsearch(hosts=END_POINT, port=443, use_ssl=True)

    #while True:
    #    try:
    tweetStreamListener = TweetStreamListener(es)
    tweetStream = tweepy.Stream(auth=api.auth, listener=tweetStreamListener)
    tweetStream.filter(track=FILTERED_KEYWORDS, async=True)
    #    except IncompleteRead:
            # reconnect and keep trucking
    #        tweetStream.disconnect()
    #        continue
    #    except KeyboardInterrupt:
            # exit
    #        tweetStream.disconnect()
    #        break
    #    except:
    #        continue


if __name__ == '__main__':
    main()

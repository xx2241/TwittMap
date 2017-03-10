import json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream


CONSUMER_KEY = 'oic2Xa3hvk019kOX2Qj8aBZvH'
CONSUMER_SECRET = 'Mm5fUpJ4akUdGrDWRsc2dvZUufccwjBipSRCmRGkXO2Sp8IQhW'
ACCESS_TOKEN = '734766867538022404-jmLnLYov6P8nMkZW49Aih3e926d1qBx'
ACCESS_SECRET = 'EEPLwgVUTkW4uTPa13jHI5AuS4lgETmOqNnVIOqFo5VI6'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_stream = TwitterStream(auth=oauth)

iterator = twitter_stream.statuses.sample()

tweet_count = 1000
for tweet in iterator:
    tweet_count -= 1
    # Twitter Python Tool wraps the data returned by Twitter
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    print json.dumps(tweet)

    # The command below will do pretty printing for JSON data, try it out
    # print json.dumps(tweet, indent=4)

    if tweet_count <= 0:
        break

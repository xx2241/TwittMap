import json
from elasticsearch import Elasticsearch
import urllib3
urllib3.disable_warnings()


def getEndPoint():
    with open('./config.txt', 'r') as configfile:
        end_point = configfile.read().splitlines()[4]
        configfile.close()
    return end_point


def tweets_filter(keyword):
    END_POINT = getEndPoint()
    es = Elasticsearch(hosts=END_POINT, port=443, use_ssl=True)

    tweet_filter = json.dumps({
                       "from" : 0, "size" : 100,
                       "query": {
                           "match": {
                               'keyword': keyword
                           }
                       },
                       "sort": [
                           {
                               "timestamp": {
                                   "order": "desc"
                               }
                           }
                       ]
                   })

    tweets_res = es.search(index="twittmap", doc_type='tweet', body=tweet_filter)
    location_res = []
    for hit in tweets_res['hits']['hits']:
        coordinates = hit['_source']['coordinates']
        if coordinates:
            print ("Current coordinates", coordinates)
            location_res.append(coordinates)

    return location_res


if __name__ == "__main__":
    tweets_filter('Trump')

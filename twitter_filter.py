import json
from elasticsearch import Elasticsearch
import urllib3
urllib3.disable_warnings()


def getEndPoint():
    with open('./config.txt', 'r') as configfile:
        end_point = configfile.read().splitlines()[4]
        configfile.close()
    return end_point


def tweets_geo(coordinates):
    END_POINT = getEndPoint()
    es = Elasticsearch(hosts=END_POINT, port=443, use_ssl=True)

    tweet_geo = json.dumps({
                    "query" : {
                        "bool" : {
                            "must" : {
                                "match_all" : {}
                            },
                            "filter" : {
                                "geo_distance" : {
                                "distance" : "50km",
                                "coordinates" : coordinates
                                }
                            }
                        }
                    }
                })

    tweets_res = es.search(index="twittmap", doc_type='tweet', body=tweet_geo)
    geo_res = []
    for hit in tweets_res['hits']['hits']:
        geo = hit['_source']['coordinates']
        if geo:
            print ("Proximity Coordinates", geo)
            geo_res.append(geo)

    return geo_res


def tweets_filter(keyword):
    END_POINT = getEndPoint()
    es = Elasticsearch(hosts=END_POINT, port=443, use_ssl=True)

    tweet_filter = json.dumps({
                       "from" : 0, "size" : 500,
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
            print ("Current Coordinate", coordinates)
            location_res.append(coordinates)

    return location_res


if __name__ == "__main__":
    tweets_filter('Trump')

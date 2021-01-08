#!/usr/bin/env python3

from indexer import indexDocuments
from utils import *
from preprocessor import Preprocessor

from elasticsearch import Elasticsearch


def basicQueries():

    def search(index, query=None, n_res=10):
        es = Elasticsearch()
        res = es.search(index=index_name, body={
            "query" : query
        }, size=n_res)

        pprint(g("%d documents found, showing the first %d" % (res['hits']['total']['value'], n_res)))
        printRes(res)
        return res


    pprint(r("BASIC QUERIES DEMO"))

    ## User case 1 - Textual search on a specific field using keywords

    # Query 1 - ...
    search(index_name, query={
                "match" : {
                    "text" : "nolan"
                }})

    search(index_name, query={
                "match_phrase" : {
                    "text" : "Nolan film's"
                }})    


    ## User case 2 - Textual search on a combination of fields
    search(index_name, query={
                "bool": {
                    "must": [
                        {"match": {"screen_name" : "newscientist"}},
                        {"match": {"text" : "insect"}}
                    ]
                }})

    # Range query example midnight on New Year's Eve
    search(index_name, query={
            "range": {
                "date" : {
                    "gt" : "Thu Dec 31 23:45:00 +0000 2020",
                    "lte" : "Fri Jan 01 01:00:00 +0000 2021"                    
                }
            }})

    



def advancedQueries(profiles):

    def search(index, query=None, n_res=10):
        es = Elasticsearch()
        res = es.search(index=index_name, body={
            "query" : query
        }, size=n_res)

        pprint(g("%d documents found, showing the first %d" % (res['hits']['total']['value'], n_res)))
        return res


    pprint(r("ADVANCED QUERIES DEMO"))

    ## User case 3 - Rank the tweets taking into account the user profile
    query_res = search(index_name, query={
                    "match" : {
                        "text" : "nolan"
                    }})

    # If user list is empty personalize_query retrive the search personalized for each user in dataset, else it provides
    # personalization for only the user specified.
    user = []
    personalized_res = profiles.personalize_query(query_res, user)

    printResAdv(personalized_res)


    ## User case 4 - Expand the search adding synonyms of the words in the query




## UTILS FUNCTION
def printRes(res):
    for doc in res['hits']['hits']:
        print(y("Tweet ID: ") + doc['_id'] + 
                g("\nUser: ") + doc['_source']['user_name'] +
                g("\nCreated at: ") + doc['_source']['date'] +
                g("\nText: ") + doc['_source']['text'] + 
                r("\nScore: ") + str(doc['_score']) + "\n")

def printResAdv(res):
    for usr in res:
        pprint('Personalized results for user: ' + usr)
        for doc in res[usr]['news']:
            print(y("Tweet ID: ") + doc['_id'] + 
                    g("\nUser: ") + doc['_source']['user_name'] +
                    g("\nCreated at: ") + doc['_source']['date'] +
                    g("\nText: ") + doc['_source']['text'] + 
                    r("\nPersonalized score: ") + str(doc['new_score']) + "\n")


if __name__ == "__main__":

    ## ES parameters for indexing data
    index_name = 'twitter_index'
    data_path = './datasets/news_tweets.json'
    config_path = './index_config.json'

    ## Index document specified in ES server, only the first time
    #indexDocuments(data_path, config_path, index_name)

    ## Basic queries on Elasticsearch
    #basicQueries()

    ## Users profiles extraction providing set of tweets
    users_tweets_path = ["./datasets/test.json"]
    user_profiles = Preprocessor(users_tweets_path)

    ## Avanced queries using users profiles for personalization
    advancedQueries(user_profiles)
    
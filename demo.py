#!/usr/bin/env python3

from utils.utils import *
from indexer import indexDocuments
from preprocessor import Preprocessor

from elasticsearch import Elasticsearch


def basicQueries():
    '''
    Performs standard queries on the news twitter index
    '''

    def search(index, query=None, n_res=10):
        es = Elasticsearch()
        res = es.search(index=index_name, body={
            "query" : query
        }, size=n_res)

        pprint(g("%d documents found (showing first %d)" % (res['hits']['total']['value'], n_res)))
        printRes(res)
        return res


    pprint(r("BASIC QUERIES DEMO"))

    ## USER CASE 1 - Textual search on a specific field using keywords

    # Query 1 - ...
    search(index_name, query={
                "match" : {
                    "text" : "nolan"
                }})

    search(index_name, query={
                "match_phrase" : {
                    "text" : "Nolan film's"
                }})    


    ## USER CASE 2 - Textual search on a combination of fields
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

    

def advancedQueries(users_tweets):
    '''
    Performs advanced queries on the news twitter index, customizing the results based on the tweets of the users 
    considered.
    '''

    def search(index, query=None, n_res=10):
        es = Elasticsearch()
        res = es.search(index=index_name, body={
            "query" : query
        }, size=n_res)

        pprint(g("%d documents found (showing first %d)" % (res['hits']['total']['value'], n_res)))
        return res


    pprint(r("ADVANCED QUERIES DEMO"))

    ## USER CASE 3 - Rank the tweets taking into account the user profile

    # If user list is empty personalize_query retrive the search personalized for each user in dataset, else it provides
    # personalization for only the users specified.
    user = ['Barack Obama']

    # ES standard query
    query_res = search(index_name, query={
                    "match" : {
                        "text" : "nolan"
                    }})

    # Personalization re-rank process
    personalized_res = users_tweets.personalize_query(query_res, user)

    printResAdv(personalized_res)


    ## USER CASE 4 - Expand the search adding synonyms of the words in the query




## Utils functions
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
    config_path = './utils/index_config.json'

    ## Index document specified in ES server, only the first time
    #indexDocuments(data_path, config_path, index_name)

    ## Basic queries on Elasticsearch
    #basicQueries()

    ## User tweets-based personalization
    users_tweets_path = ["./datasets/group_one.json","./datasets/group_two.json"]
    users_tweets = Preprocessor(users_tweets_path)

    ## Avanced queries using users tweets for personalization
    advancedQueries(users_tweets)
    
from indexer import Indexer
from elasticsearch import Elasticsearch
from utils import *


## ELASTICSEARCH INDEX CREATION FOR NEWS TWEETS
def indexing(): 

    pprint(r("PHASE 1 - ES INDEX CREATION"))
    index = Indexer(dfile, cfile, index_name)
    index.indexCorpus()



## BASIC QUERIES
def basicQueries():

    pprint(r("PHASE 2 - BASIC QUERIES"))
    res = search(index_name, query={"user_name": "Tyson"})
    printRes(res)



## USER PROFILE EXTRACTION
def extractUserProfile():

    pprint(r("PHASE 3 - USER PROFILE EXTRACTION"))
    



## ADVANCED QUERIES WITH USER PROFILE
def advancedQueries():

    pprint(r("PHASE 4 - ADVANCED QUERIES"))

    # effettuo query
    res = search(index_name, query={"user_name": "Tyson"})

    import pdb; pdb.set_trace()

    # re-rank tramite calcolo similarità tra user profile e risultati query

    # stampa dei risultati




## UTILS FUNCTION
def search(index, query=None, n_res=10):
    es = Elasticsearch()
    res = es.search(index=index_name, body={
        "query" : {
            "match" : query
        }
    }, size=n_res)

    pprint(g("%d documents found" % res['hits']['total']['value']))
    return res

def printRes(res):
    for doc in res['hits']['hits']:
        print("Tweet ID: " + y(doc['_id']) + "\nUser: " + g(doc['_source']['user_name']) + "\nText: " 
                + doc['_source']['text'] + '\n')



if __name__ == "__main__":

    index_name = 'twitter_index'
    dfile = './datasets/test.json'
    cfile = './index_config.json'

    #indexing()

    #basicQueries()

    advancedQueries()

    
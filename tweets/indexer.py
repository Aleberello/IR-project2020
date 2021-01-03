import json
from elasticsearch import Elasticsearch

file = './index_config.json'
index_name = 'twitter_index'

class Indexer:

    def __init__(self):
        return  

    @staticmethod
    def getIndexConfig(self, file_path):
     """
     Loads a JSON configuration file for the elasticsearch indexing
     param file_path: the path of the file in JSON format;

     return: the configuration file for indexing
     """
     with open(file=file_path, encoding='utf-8', errors='ignore') as path:
         index_config = json.load(path)
     return index_config


    @staticmethod
    def getData(self, fd, sd):

        """
        Identifies all the available documents inside a dictionary and return them as a List.
        param fd: the first data file (document) object in JSON format.
        sd: the second data file (document) object in JSON format.

        return: a list of all documents
        """
        for file in [fd, sd]:
            data = json.load(open(file))
        return data
        
    
    @staticmethod
    def indexCorpus(self, index_name, index_config, corpus):
        """
        Indexes a document using ElasticSearch method. A matching query is used to retrieve 
        param index_name: name of the index,  index_config: the configured mapping, corpus: the corpus (document) object as a dictionary
        
        return: results from the query
        """
        RESET = "\033[0m"
        g = lambda s: "\033[32m" + str(s) + RESET  # green
        y = lambda s: "\033[33m" + str(s) + RESET  # yellow

        es = Elasticsearch()

        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
        else: es.indices.create(index=index_name, body=index_config)

        for tweet in corpus:
            es.index(index=index_name, body=corpus[tweet])
        
        results = es.search(index=index_name, body={
            "query" : { 
                "match" : {"user_name": "Obama"}
            }
        })

        print(g("%d documents found" % results['hits']['total']['value']))

        for doc in results['hits']['hits']:
            print("Tweet ID: " + y(doc['_id']) + "\nUser: " + g(doc['_source']['user_name']) + "\nText: " + doc['_source']['text'])
            print('\n')
        return results


if __name__ == "__main__":

    index_config = Indexer.getIndexConfig(None, file)

    data = Indexer.getData(None, 'group_one.json', 'group_two.json')
    res = Indexer.indexCorpus(None, index_name, index_config, data)
    print(res)
    
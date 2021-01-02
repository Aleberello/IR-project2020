import json
from elasticsearch import Elasticsearch

file = 'tweets/index_config.json'
index_name = "twitter_index"
#index_config = json.load(file)

class Corpus:

    def __init__(self):
        return  

    @staticmethod
    def getCorpus(self, file_path):

        """
        Identifies and returns all the metadata inside a given corpus (for example tweet):
        param file_path: the path of the file in JSON format (corpus);

        return: a dictionary containing all the metadata.
        """
        user_name = None
        date = None
        tweet_id = None
        text = None


        # Check for metadata inside the json file
        for metadata in file_path:
            if text == None:
                if "+0000" in metadata: 
                    date = metadata["date"] # assign the date  
                elif metadata.startswith("1", 0, 1): 
                    tweet_id = metadata["tweet_id"] # assignt the id 
                elif "@" in metadata:
                    user_name = metadata["user_name"] # assign the username
            else: text += metadata

            if user_name == None or date == None or tweet_id == None:
                return

        doc = {
            user_name,
            date,
            tweet_id,
            text 
            }
        return doc


    @staticmethod
    def getMultipleCorpus(self, corpus):

        """
        Identifies all the available documents inside a dictionary and return them as a List.
        param corpus: the corpus (document) object as a dictionary

        return: a list of all documents
        """
        docs = 0
        allDocs = []

        # if the corpus is empty
        with open(corpus) as input_doc:
            tweet = ""

            for line in input_doc:
                if '@' in line and len(tweet) > 0:
                    docs += 1
                    allDocs.append(Corpus.getCorpus(None, tweet))
                    tweet = ''
                else:
                    tweet += line

            # if the corpus is available (there's already content)
            if len(tweet)>0:
                allDocs.append(Corpus.getCorpus(None, tweet))

        return allDocs
    
    
    @staticmethod
    def indexCorpus(self, index_name, index_config, corpus):
        """
        Indexes a document using ElasticSearch method. A matching query is used to retrieve 
        param index_name: name of the index,  index_config: the configured mapping, corpus: the corpus (document) object as a dictionary
        
        return: results from the query
        """

        es = Elasticsearch()

        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
        else: es.indices.create(index=index_name, body=index_config)

        for doc in corpus:
            if doc != None:
                es.index(index=index_name, body=doc)
        
        results = es.search(index=index_name, body={
            "query" : {
                "bool" : {
                    "must" : [
                        { "match" : {"user_name": "Neil deGrasse Tyson"} }
                    ]
                }
            }
        })

        return results


if __name__ == "__main__":

    with open(file="tweets/index_config.json", mode='r') as path:
        index_config = json.load(path)    
    corpus = Corpus.getMultipleCorpus(None, 'tweets/group_one.json')
    res = Corpus.indexCorpus(None, index_name, index_config, corpus)

    for i in res:
        print(i.values)
    
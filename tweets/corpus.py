from elasticsearch import Elasticsearch


index_name = "twitter_index"
index_config = {
    "settings": {
        "number_of_shards" : 1,
        "number_of_replicas" : 1,
        "analysis" : {
            "analyzer" : {
                "tweet_1" : {
                "type" : "custom",
                "tokenizer" : "standard",
                "filter" : ["lowercase"]
                },
            "tweet_2" : {
                "type" : "custom",
                "tokenizer" : "standard",
                "filter" : ["lowercase", "english_stop", "porter_stem"],
                "char_filter" : ["html_strip"]
                }
            },
            "filter" : {
                "english_stop" : {"type": "stop", "Stopwords" : "_english_"}
            }
        }
    },
    "mappings": {
        "properties" : {
            "user_name" : {
                "type": "text",
                "analyzer" : "tweet_2",
                "search_analyzer" : "tweet_2",
                "similarity" : "boolean"
            },
            "date": {
                "type": "text",
                "analyzer" : "tweet_1",
                "search_analyzer" : "tweet_1",
                "similarity" : "boolean"
            },
            "tweet_id" : {
                "type": "text",
                "analyzer" : "tweet_1",
                "search_analyzer" : "tweet_1",
                "similarity" : "boolean"
            },
            "text" : {
                "type": "text",
                "analyzer" : "tweet_2",
                "search_analyzer" : "tweet_2",
                "similarity" : "boolean"
            }
        }
    }
}

class Corpus:

    def __init__(self):
        return

    @staticmethod
    def getTweet(self, tweet):
        """
        TODO(Add documentation)
        """
        user_name = None
        date = None
        tweet_id = None
        text = None

        # Check for metadata inside a tweet

        for metadata in tweet.split("\n"):
            if text == None:
                if metadata.startswith("+0000 "):
                    date = metadata[len("+0000 "):].strip() # assign the date of the tweet
                elif metadata.startswith("1341"):
                    tweet_id = metadata[len("1341"):].strip() # assign the tweet id
                elif metadata.startswith("@"):
                    user_name = metadata[len("@"):].strip() # assign the username
                else:
                    text = metadata.strip() # assign the containing text
            if user_name == None or date == None or tweet_id == None:
                return

        doc = {
            "user_name" : user_name,
            "date" : date,
            "tweet_id" : tweet_id,
            "text" : text 
        }

        return doc

    @staticmethod
    def getMultipleTweets(self, corpus):

        """
        TODO(Add Documentation)
        """
        docs = 0
        allDocs = []

        # if the tweet is empty
        with open(corpus) as input_doc:
            tweet = ""
            for line in input_doc:
                if '' in line and len(tweet) > 0:
                    docs += 1
                    allDocs.append(Corpus.getTweet(None, tweet))
                    tweet = ""
                else:
                    tweet += line

            # if the tweet is available (there's already content)

            if len(tweet)>0:
                allDocs.append(Corpus.getTweet(None, tweet))

        return allDocs
    
    @staticmethod
    def indexTweet(self, index_name, index_config, corpus):
        """
        TODO(Add documentation)
        hint: corpus = Corpus.getMultipleTweets()
        """

        es = Elasticsearch()

        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
        es.indices.create(index=index_name, body=inde])

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
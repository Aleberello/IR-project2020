import json
import tqdm
from os import path
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from utils import *

class Indexer:

    def __init__(self, datapath, configpath, index_name):
        self.index_name = index_name 
        self.config_path = configpath
        self.data_path = datapath


    def indexCorpus(self):
        """
        Indexes a document using ElasticSearch method. 
        param index_name: name of the index,  index_config: the configured mapping, corpus: the corpus (document) object as a dictionary
        
        return: results from the query
        """

        def genData():
            for tweet in tweets:
                yield tweets[tweet]


        # Load a JSON mapping file for elasticsearch indexing
        if path.exists(self.config_path):
            with open(file=self.config_path, encoding='utf-8') as p:
                index_config = json.load(p)

        # Load twitter dataset
        if path.exists(self.data_path):
            with open(self.data_path) as o:
                tweets = json.load(o)


        es = Elasticsearch()

        if es.indices.exists(index=self.index_name):
            es.indices.delete(index=self.index_name)
        es.indices.create(index=self.index_name, body=index_config)

        pprint("Indexing documents...")
        progress = tqdm.tqdm(unit="docs", total=len(tweets))
        successes = 0
        for ok, action in streaming_bulk(
            client=es, index=self.index_name, actions=genData(),
        ):
            progress.update(1)
            successes += ok
        pprint("Indexed %d/%d documents" % (successes, len(tweets)))
        
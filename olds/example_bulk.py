import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import tqdm

from TwitterScraper import scrape


#RESET = "\033[0m"
#g = lambda s: "\033[32m" + str(s) + RESET  # green
#y = lambda s: "\033[33m" + str(s) + RESET  # yellow


with open(file="tweets/index_config.json", mode='r') as path:
    index_config = json.load(path)    


for file in ["tweets/group_one.json"]:
    data = json.load(open(file))


index_name = "twitter_index"

es = Elasticsearch()

print("Creating an index...")
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
es.indices.create(index=index_name, body=index_config)



def gendata():
    for tweet in data:
        yield data[tweet]



print("Indexing documents...")
progress = tqdm.tqdm(unit="docs", total=len(data))
successes = 0
for ok, action in streaming_bulk(
    client=es, index="twitter_index", actions=gendata(),
):
    progress.update(1)
    successes += ok
print("Indexed %d/%d documents" % (successes, len(data)))



res = es.search(index=index_name, body={
    "query" : {
         "match" : {"user_name": "Obama"}
    }
}, size=20)

print(g("%d documents found" % res['hits']['total']['value']))

for doc in res['hits']['hits']:
    print("Tweet ID: " + y(doc['_id']) + "\nUser: " + g(doc['_source']['user_name']) + "\nText: " + doc['_source']['text'])
    print('\n')


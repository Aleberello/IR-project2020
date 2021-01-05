import json
from elasticsearch import Elasticsearch

RESET = "\033[0m"
g = lambda s: "\033[32m" + str(s) + RESET  # green
y = lambda s: "\033[33m" + str(s) + RESET  # yellow


with open(file="./index_config.json", mode='r') as path:
    index_config = json.load(path)    

for file in ["test.json"]:
    data = json.load(open(file))


index_name = "twitter_index"

es = Elasticsearch()

if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

es.indices.create(index=index_name, body=index_config)

import pdb; pdb.set_trace()
for tweet in data:
    print(es.index(index=index_name, body=data[tweet]))


res = es.search(index=index_name, body={
    "query" : {
         "match" : {"user_name": "Obama"}
    }
}, size=20)

print(g("%d documents found" % res['hits']['total']['value']))

for doc in res['hits']['hits']:
    print("Tweet ID: " + y(doc['_id']) + "\nUser: " + g(doc['_source']['user_name']) + "\nText: " + doc['_source']['text'])
    print('\n')







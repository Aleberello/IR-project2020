## SOME CURL COMMAND FOR TEST ELASTICSEARCH API's


# SIMPLE QUERY WITH SCORE CALCULATION EXPLITATION
curl -X GET "localhost:9200/twitter_index/_search/?pretty" -H 'Content-Type: application/json' -d'
{
    "explain": true,
    "query": {
        "bool": {
            "must" : {
                "match_phrase" : {"text" : "Anybody 52 light years away"}
            }
        }
    }
}'


# TESTING ANALYZER WITH PHRASES
curl -X POST "localhost:9200/twitter_index/_analyze?pretty" -H 'Content-Type: application/json' -d'
{
  "analyzer": "tweet_text",
  "text": "PA bakery claims cookie sales have predicted past presidential elections \u2014 and heres how it looks for 2020\n\nhttps://t.co/nuzkFp6c8Y https://t.co/Iumbj1JW3V"

}'

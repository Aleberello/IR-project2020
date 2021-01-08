# IR-project2020
## Project A - Personalized Search Engine for microblog
Team members:
- Alessandro Bertolo (808314) - a.bertolo2@campus.unimib.it
- Diego Bellini (816602) - d.bellini3@campus.unimib.it
- Mirko Lantieri (858278) - m.lantieri@campus.unimib.it

## Project summary
  
### Project structure
```bash
├── datasets                        # extracted tweets for users and news
│   ├── group_one.json
│   ├── group_two.json
│   ├── news_tweets.json
├── twitter-scrape                  # Twitter API implementation for tweets extraction
│   ├── api_key.example.py          # Twitter API credentials
│   ├── scrape.py                   # tweets scraper
│   ├── usernames.txt               # list of Twitter usernames from wich extract tweets
├── utils                           # utils folder
│   ├── user-profiles               # stores all already user tweets pre-processed for personalization in pickle files
│       └── ...
│   ├── index_config.json           # configuration file for ElasticSearch index creation
│   ├── utils.py                    # utils variables and methods
│   ├── wn_s.pl                     # WordNet synonyms dictionary used for synonyms queries in ElasticSearch
├── demo.py                         # demo script for the project
├── indexer.py                      # script used for indexing tweets in ElasticSearch
├── preprocessor.py                 # script used for manual pre-processing of tweets and query personalization phase
├── README.md
├── requiments.txt
└── .gitignore
```

## How to run
### Requiments
Libraries necessary for the project are contained in the file `requiments.txt`:
```
pip install requiments.txt
```

### Set-up
- Download and install [Elasticsearch 7.10.1](https://www.elastic.co/downloads/elasticsearch)
- For the synonym query section (inside `demo.py`):
    - move WordNet dictionary from `"utils/wn_s.pl"` to ElasticSearch source folder `"elasticsearch-*/config/"`
- For the preprocessing section (`processor.py`):
    - un-comment and download, only for the first execution, the following nltk packages
    ```python
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    ```


Notes:
- After the first execution the preprocessed tweets of given JSON are saved into JSON_filename.pickle file 
in /utils/user-profiles optimize the execution time
- After the first execution TfidfVectorized object for each user are saved into a .pickle file in 
utils/user-profile/user_name folder to optimize the execution time
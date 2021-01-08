# IR-project2020
## Project A - Personalized Search Engine for microblog
Team members:
- Alessandro Bertolo (808314) - a.bertolo2@campus.unimib.it
- Diego Bellini (816602) - d.bellini3@campus.unimib.it
- Mirko Lantieri (858278) - m.lantieri@campus.unimib.it

## Project summary
  
### Project structure
#### preprocessor.py:
  - Download only for the first execution the following nltk packages: stopword, wordnet, averaged_perceptron_tagger (these are commented on in the first rows of this file)
  - After the first execution the user profile for each user are saved into the test.pickle file to optimize the execution time
  - After the first execution TfidfVectorized object for each user are saved into a .pickle file to optimize the execution time

## How to run
### Requiments
- Python 3

### Set-up
- Download and install [Elasticsearch 7.10.1](https://www.elastic.co/downloads/elasticsearch)
- Install [Python Elasticsearch Client](https://elasticsearch-py.readthedocs.io/en/master/)

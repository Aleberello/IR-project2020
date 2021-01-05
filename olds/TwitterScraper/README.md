# TwitterScraper
Original project by @MatthewWolff ([Github repo](https://github.com/MatthewWolff/TwitterScraper)).
Modified for the IR project purposes.

## Description

This script allows the extraction of the tweets of one or more users in two ways:
* using directly Twitter API's with Tweepy library
* using Selenium as web scraper

The second way is necessary if you want to extract the entire tweets history as Twitter API's allow the extraction of only 3200 most recent 
tweets.

NOTE: This scraper will notice if a user has less than 3200 tweets. In this case, it will do a "quickscrape" to grab all available tweets at once (significantly faster). It will store them in the exact same manner as a manual scrape.

`utils/jsonToCsv.py` script allows you to convert the resulting json files, providing them as input, into csv files.


## Requirements (or rather, what I used)

* python3 (3.7.3)
* Modules (via `pip`):
  * selenium (3.141.0)
  * tweepy (3.8.0)
  * requests (2.21.0)
  * requests_oauthlib (1.3.0)
  * beautifulsoup4 (4.7.1)
* [Chrome webdriver](https://chromedriver.chromium.org/downloads)) - Provided version Version 87.0.4280.88 (Linux)
* [Twitter API developer credentials](https://dev.twitter.com)


## Using the Scraper

* run `python3 scrape.py` and add the arguments you desire. Try `./scrape.py --help` for all options.
  * `-u` followed by the username
  * `-us` followed by the path of txt file with one row for each username to extract
  * `--since` followed by a date string, e.g., (2017-01-01). Defaults to whenever the user created their twitter
  * `--until` followed by a date string, e.g., (2018-01-01). Defaults to the current day 
  * `--by` followed by the number of days to scrape at once (default: 7)
    * If someone tweets dozens of times a day, it might be better to use a lower number
  * `--delay` followed by an integer. This will be the number of seconds to wait on each page load before reading the page
    * if your internet is slow, put this higher (default: 3 seconds)

* when collection finishes, it will dump all the data to a `.json` file in `/out` folder that corresponds to the twitter handle
  * don't worry about running two scrapes that have a time overlap; it will only retrieve new tweets!

Note: if `-us` is provided, all the tweets will be stored in a single json file in  `out/all_usrs.json`.

## Troubleshooting

* do you get a driver error when you try and execute the script?
  * make sure your browser is up to date and that you have a driver version that matches your browser version 
  * you can also open `scrape.py` and change the driver to use `Chrome()` or `Firefox()`
* does the scraper seem like it's missing tweets that you know should be there?
  * try increasing the `--delay` parameter, it likely isn't waiting long enough for everything to load
  * try decreasing the `--by` parameter, it likely has too many tweets showing up on certain days

## Twitter API credentials

* sign up for a developer account here https://dev.twitter.com/
* get your key here: https://apps.twitter.com/
* once you have your key, open the file `utils/api_key.example.py` and fill in your info removing "example"

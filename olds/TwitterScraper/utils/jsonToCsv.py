#!/usr/bin/env python3

import argparse
import json, csv
import pandas as pd
from os import path

# OUTPUT COLORS
RESET = "\033[0m"
g = lambda s: "\033[32m" + str(s) + RESET  # green
y = lambda s: "\033[33m" + str(s) + RESET  # yellow

def retrieve_existing(filepath):
    tweets = dict()
    if path.exists(filepath):
        with open(filepath) as o:
            tweets = json.load(o)

    return tweets

def save_to_csv(json_tw, savepath=None):
    if savepath is None:
        savepath = 'out/out.csv'
    with open(savepath, 'w') as f:
        df = pd.DataFrame().from_dict(json_tw, orient='index', dtype='str')
        df.to_csv(f,index=False)
    print(g("JSON tweets converted in ") + y(savepath))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="jsonToCsv.py", usage="python3 %(prog)s [options]",
                                     description="jsonToCsv.py - Convert JSON twitter file to csv")
    parser.add_argument("-f", "--file", help="Convert user's Tweets in this txt file.", required=True)
    parser.add_argument("-sp", "--savepath", help="Choose a path for the csv file.")
    args = parser.parse_args()

    tweets = retrieve_existing(args.file)
    save_to_csv(tweets, args.savepath)

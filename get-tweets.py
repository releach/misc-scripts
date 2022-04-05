import csv
import json
import os

import pandas as pd
import requests

bearer_token = os.environ.get("BEARER_TOKEN")
search_url = "https://api.twitter.com/2/tweets/"
csvin = input('Enter input csv path: ')
csvout = input('Enter output csv filename: ')
# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
# query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}


def get_tweets(csvin):
    """
    Creates dicts of 100 tweet_ids and appends them to param_list.
    """
    df = pd.read_csv(csvin, chunksize=100)
    param_list = []
    for data in df:
        tweet_ids = []
        for row in data['tweet_id']:
            tweet_ids.append(row)
        tweet_ids_str = ','.join(map(str, tweet_ids))
        tweet_list = {'ids': tweet_ids_str}
        param_list.append(tweet_list)
    return param_list


def bearer_oauth(r):
    """
    Creates auth headers for bearer token.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    return r


def connect_to_endpoint(url, params):
    """
    Connects to API endpoint and returns tweets in JSON.
    """
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    json_response = response.json()
    return json_response


def write_csv(source_data):
    """
    Parses returned JSON and writes it to a CSV. For now, ignores errors.
    """
    tweetdata = []
    if source_data['data']:
        for tweet in source_data['data']:
            tweetrow = []
            tweetrow.append(tweet['id'])
            tweetrow.append(tweet['text'])
            tweetdata.append(tweetrow)
    with open(csvout, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(tweetdata)


def main():
    tweet_data = get_tweets(csvin)
    for query_params in tweet_data:
        json_response = connect_to_endpoint(search_url, query_params)
        write_csv(json_response)

if __name__ == "__main__":
    main()

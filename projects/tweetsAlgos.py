import os
import tweepy as tw
import pandas as pd
import re
from .rating_model import rate_review
from .sentimentsAlgo import sentiment_scores, generate_particular_sentiments

def clean_tweet(tweet): 
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

def getTweets(search_words, date_since, count):
    consumer_key = "JDErXhmGOnDeWZE6gQJ7ghpt3"
    consumer_secret = 'tt1bsCcDcqcOuvK77dP0NorYaMh1sSE03NeQGvUSbvOBc4ly1s'
    access_token = '933231091036569600-XDs6QN5NSOXriVp46d7LLyVx1Vigwq0'
    access_token_secret = 'vitrHtQpKCdC1Jq8svFMxtsl6HnSoKnm2whwFNXrtBQ61'
    tweets_on_topic = []

    #authenticate
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # search_words = "#indvsnz"
    # date_since = "2020-02-01"

    #get tweets
    tweets = tw.Cursor(api.search,
                q=search_words,
                lang="en",
                since=date_since).items(count)

    #print tweets
    for tweet in tweets:
        tweets_on_topic.append(clean_tweet(tweet.text))

    return tweets_on_topic

tweets = getTweets('#indvsnz', '2020-02-01', 10)
scores = sentiment_scores(tweets)
partitions, total = generate_particular_sentiments(scores, 10)
print(partitions)
print(total)



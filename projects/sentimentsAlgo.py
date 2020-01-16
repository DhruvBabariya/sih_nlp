import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import os

def reviews_preprocessing(filePathJson, key):
    fileContent = open(filePathJson)
    reviews = []
    corrected_reviews = []

    for review in fileContent:
        reviews.append(json.loads(review))

    counter = 0
    for review in reviews:
        try:
            reivew_text = review[key]
            # review_text = TextBlob(reivew_text).correct()
            corrected_reviews.append(reivew_text)
        except:
            continue
    return corrected_reviews


def sentiment_scores(reviews_list):
    sentiment_scores = []
    for review in reviews_list:
        sid_obj = SentimentIntensityAnalyzer()
        sentiment_dict = sid_obj.polarity_scores(review)
        sentiment_scores.append(sentiment_dict)
    return sentiment_scores


# positive sentiment: compound score >= 0.05
# neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
# negative sentiment: compound score <= -0.05

def generate_particular_sentiments(review_sentiment_scores):
    sentiments_dict = {'positive': [],
                       'negative': [], 'neutral': [], 'compound': []}
    num_of_tweets_for_sentiment = {'positive': 0, 'negative': 0, 'neutral': 0}

    for value in review_sentiment_scores:
        sentiments_dict['positive'].append(value['pos'])
        sentiments_dict['negative'].append(value['neg'])
        sentiments_dict['neutral'].append(value['neu'])
        sentiments_dict['compound'].append(value['compound'])

        if(value['compound'] >= 0.05):
            num_of_tweets_for_sentiment['positive'] += 1
        elif(value['compound'] > -0.05 and value['compound'] < 0.05):
            num_of_tweets_for_sentiment['neutral'] += 1
        elif(value['compound'] <= -0.05):
            num_of_tweets_for_sentiment['negative'] += 1
    return sentiments_dict, num_of_tweets_for_sentiment

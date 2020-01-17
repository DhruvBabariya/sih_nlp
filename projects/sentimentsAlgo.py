import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

filePathJson = '/Users/amanchaudhary/Documents/temp_dataset.json'


def reviews_preprocessing(filePathJson, key):
    fileContent = open(filePathJson)
    reviews = []
    corrected_reviews = []
    count = 0
    for review in fileContent:
        if(count < 10000):
            reviews.append(json.loads(review))
            count = count + 1
        else:
            break

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

def generate_particular_sentiments(review_sentiment_scores, parts):
    # sentiments_dict = {'positive': [],
    #                    'negative': [], 'neutral': [], 'compound': []}
    num_of_tweets_for_sentiment = {'positive': 0, 'negative': 0, 'neutral': 0}
    partitioned_sentiment_dict = {
        'positive': {}, 'negative': {}, 'neutral': {}}

    for i in range(0, int(100/parts) + 1):
        partitioned_sentiment_dict['positive'][i] = 0
        partitioned_sentiment_dict['negative'][i] = 0
        partitioned_sentiment_dict['neutral'][i] = 0

    for value in review_sentiment_scores:
        # sentiments_dict['positive'].append(value['pos'])
        # sentiments_dict['negative'].append(value['neg'])
        # sentiments_dict['neutral'].append(value['neu'])
        # sentiments_dict['compound'].append(value['compound'])

        pos_value = value['pos'] * 100
        neg_value = value['neg'] * 100
        neu_value = value['neu'] * 100



        pos_index = int(pos_value/parts)
        neg_index = int(neg_value/parts)
        neu_index = int(neu_value/parts)

        partitioned_sentiment_dict['positive'][pos_index] += 1
        partitioned_sentiment_dict['negative'][neg_index] += 1
        partitioned_sentiment_dict['neutral'][neu_index] += 1
        
        if(value['compound'] >= 0.05):
            num_of_tweets_for_sentiment['positive'] += 1
        elif(value['compound'] > -0.05 and value['compound'] < 0.05):
            num_of_tweets_for_sentiment['neutral'] += 1
        elif(value['compound'] <= -0.05):
            num_of_tweets_for_sentiment['negative'] += 1

    
    partitioned_sentiment_dict['positive'][int(100/parts) - 1] += partitioned_sentiment_dict['positive'][int(100/parts)]
    partitioned_sentiment_dict['negative'][int(100/parts) - 1] += partitioned_sentiment_dict['negative'][int(100/parts)]
    partitioned_sentiment_dict['neutral'][int(100/parts) - 1] += partitioned_sentiment_dict['neutral'][int(100/parts)]

    del partitioned_sentiment_dict['positive'][int(100/parts)]
    del partitioned_sentiment_dict['negative'][int(100/parts)]
    del partitioned_sentiment_dict['neutral'][int(100/parts)]

    return partitioned_sentiment_dict, num_of_tweets_for_sentiment


# reviews = reviews_preprocessing(filePathJson, 'reviewText')
# scores = sentiment_scores(reviews)
# partitions, total = generate_particular_sentiments(scores, 10)
# print(partitions)

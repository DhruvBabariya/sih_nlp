from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

def sentiment_score(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict

#msg = input("Enter the review: ")
#correct_msg = TextBlob(msg).correct()
#print(msg+ str(correct_msg))
# sentiment_scores(msg)

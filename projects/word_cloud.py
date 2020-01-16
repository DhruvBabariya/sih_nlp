import json
from django.conf import settings
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os

#{"overall": 5.0, "verified": true, "reviewTime": "07 14, 2014", "reviewerID": "A25MDGOMZ2GALN", "asin": "B00005N7P0", "reviewerName": "Alvey", "reviewText": "A great read every issue.", "summary": "Five Stars", "unixReviewTime": 1405296000}

def generate_word_cloud(filePathJson, key):
    fileContent = open(filePathJson)
    stopwords = set(STOPWORDS)
    processed_words = ''
    words_list = []
    reviews = []

    for review in fileContent:
        try:
            reviews.append(json.loads(review))
        except:
            continue

    for review in reviews:
        try:
            text = review[key].lower()
            processed_words = processed_words + text + ' '
        except:
            continue


    wordcloud = WordCloud(width=800, height=800,
                      background_color='white',
                      stopwords=stopwords,
                      min_font_size=10).generate(processed_words)

    plt.figure(figsize = (8, 8), facecolor = None) 
    # plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    
    plt.savefig(os.path.join(settings.MEDIA_ROOT, 'fig.png'))
    plt.close()

# filePathJson = os.path.join(settings.MEDIA_ROOT, 'temp.json')
# generate_word_cloud(filePathJson, 'reviewText')
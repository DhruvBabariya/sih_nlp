import json
import re
import nltk
import fasttext
import os
from .rating_model import rate_review

# filePathJson = '/Users/amanchaudhary/Documents/projects/sih_nlp/projects/temp.json'

def get_aspects_list(filePathJson, key, aspect):
    fileContent = open(filePathJson)
    reviews = []
    rating = 0
    tokenized_sentences = []
    count = 0
    reviewText = []
    aspect_list = aspect

    for review in fileContent:
        if(count<100000):
            try:
                reviews.append(json.loads(review))
                count = count + 1
            except:
                continue
        else:
            break

    for review in reviews:
        try:
            var = nltk.sent_tokenize(review[key])     
            for sentence in var:
                tokenized_sentences.append(sentence)
        except:
            continue
        
    for sentence in tokenized_sentences:
        for el in aspect.keys():
            if(el in sentence.lower()):
                aspect_list[el].append(sentence)

    return aspect_list

def give_aspect_rating(aspect_list):
    aspect_rating = {}
    for keys in aspect_list.keys():
        rating = 0
        for review in aspect_list[keys]:
            if('\n' in review):
                review = ''.join(review.split('\n'))
            rating += float(rate_review(review))

        if(len(aspect_list[keys]) == 0):
            continue
        aspect_rating[keys] = round(rating /len(aspect_list[keys]), 2)

    return aspect_rating

# result = get_aspects_list(filePathJson, 'reviewText', aspect={'battery': [], 'camera': []})
# rating_aspects = give_aspect_rating(result)
# print(rating_aspects)







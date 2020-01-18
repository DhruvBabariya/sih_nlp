from .rating_model import rate_review
import json

#{"overall": 5.0, "verified": true, "reviewTime": "07 14, 2014", "reviewerID": "A25MDGOMZ2GALN", "asin": "B00005N7P0", "reviewerName": "Alvey", "reviewText": "A great read every issue.", "summary": "Five Stars", "unixReviewTime": 1405296000}

def predict_rating_dataset(filePathJson, key):
    fileContent = open(filePathJson)
    reviews = []
    rating = 0

    for review in fileContent:
        try:
            reviews.append(json.loads(review))
        except:
            continue

    for review in reviews:
        try:
            sentence = ''.join(review[key].split('\n'))
            rating += float(rate_review(sentence))
            count = count + 1
        except:
            continue
    predicted_avg_rating_dataset = round(rating / len(reviews), 2)

    return predicted_avg_rating_dataset


def original_rating_dataset(filePathJson, key):
    fileContent = open(filePathJson)
    reviews = []
    rating = 0

    for review in fileContent:
        try:
            reviews.append(json.loads(review))
        except:
            continue

    for review in reviews:
        rating += review[key]
    
    reviews_length = len(reviews)
    average_rating_dataset = round(rating / len(reviews), 2)

    return average_rating_dataset, reviews_length
    
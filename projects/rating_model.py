import fasttext
import re
import os.path

BASE = os.path.dirname(os.path.abspath(__file__))

filename = os.path.join(BASE, "compressed_model_ratings.ftz")
model = fasttext.load_model(filename)

def rate_review(review):
    review = review.lower()
    review = re.sub(r"([.!?,'/()])", r" \1 ", review)
    result = model.predict(review,1)
    rating = result[0][0][9:]
    return rating

# print(rate_review("The restuarant is good but food quality is bad"))

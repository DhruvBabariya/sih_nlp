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

print(rate_review("Pros: \
1.Looks stunning high end category.\
2.Battery is also powerful.\
3. Fast charging.\
Cons:\
1.Camera is not upto mark as it says 48MP it's like 8 Mp \
2. Storage & Memory statistics are confusing. Showing 900 mb free though I am not accessing much resources. \
3. Earphone slot given at down side which makes difficult to handle phone."))

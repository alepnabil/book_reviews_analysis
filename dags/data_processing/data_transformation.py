from langdetect import detect, DetectorFactory
from nltk.corpus import stopwords
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from spacy.tokens import Doc

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# spacy.load('en_core_web_sm')

# stop = stopwords.words('english')


# @spacy.Language.component("custom_sentiment")
# def get_blob(doc):
#     # your custom component code here
#     return doc

# Doc.set_extension('blob', getter=get_blob)

# def custom_sentiment(doc):
#     # custom sentiment analysis logic here
#     return doc
    
def get_num_author_books(author):
    num_author_books = author.split('Author')[1].split('book')[0]
    return num_author_books


def get_num_author_followers(author):
    author = author.replace('followers', 'follower')

    if 'books' in author:
        num_author_followers = author.split('books')[-1].replace('follower', '')
    elif 'book':
        num_author_followers = author.split('book')[-1].replace('follower', '')

    return num_author_followers


def get_num_reviewer_reviews(reviewer):
    reviews = reviewer.lower()
    reviews = reviewer.replace('reviews', 'review')

    reviews = reviewer.split()[0]

    return reviews


def get_num_reviewer_followers(reviewer):
    if 'follower' in reviewer:
        followers = reviewer.split()[-2]
    elif 'followers' in reviewer:
        followers = reviewer.split()[-2]
    else:
        followers = None

    return followers


def multiply_followers(follower):
    if follower is None:
        pass
    elif 'k' in follower:
        follower = float(follower.strip('k'))
        follower = follower * 1000
    else:
        follower = follower
    return follower


def get_ratings(rating):
    rating = rating.split()[1]
    return rating


def get_num_review_likes(review):
    review = review.split()[0]

    return review


def get_num_review_comments(comment):
    comment = comment.split()
    comment_len = len(comment)
    if comment_len >= 4:
        comment = comment[-2]
    else:
        comment = None
    return comment


def get_review_likes(review):
    # Case 1:138 likes 4 comments
    # Case 2:165 likes
    # Case 3:3 comments

    # convert all reviews which has 'likes' to 'like'
    if 'likes' in review:
        review = review.replace('likes', 'like')
    else:
        pass

    review = review.split()
    if 'like' in review:
        review = review[0]
    else:
        review = None

    return review


def get_review_comments(comment):
    # Case 1:138 likes 4 comments
    # Case 2:3 comments
    # Case 3:1 likes

    # convert all reviews which have 'comments' to 'comment'
    if 'comments' in comment:
        comment = comment.replace('comments', 'comment')
    else:
        pass

    # to handle different kind of cases
    review_len = len(comment.split())
    if review_len == 4:
        comment = comment.split()[2]
    elif review_len == 2 and 'comment' in comment:
        comment = comment.split()[0]
    else:
        comment = None

    return comment


def classify_language(review):
    DetectorFactory.seed = 0
    try:
        return detect(review)
    except:
        return 'None'


# def calculate_sentiment_score(df):
#     language = df['language']
#     review = df['clean_review']

#     if language == 'es':
#         model = spacy.load('es_dep_news_trf')
#         spacy_text_blob = SpacyTextBlob('sentiment',model)
#     elif language == 'pt':
#         model = spacy.load('pt_core_news_lg')
#         spacy_text_blob = SpacyTextBlob('sentiment',model)
#     elif language == 'it':
#         model = spacy.load('it_core_news_lg')
#         spacy_text_blob = SpacyTextBlob('sentiment',model)
#     elif language == 'fr':
#         model = spacy.load('fr_dep_news_trf')
#         spacy_text_blob = SpacyTextBlob('sentiment',model)
#     else:
#         model = spacy.load('en_core_web_trf')
#         spacy_text_blob = SpacyTextBlob('sentiment',model)
    
#     model.add_pipe('spacytextblob',last=True)
#     # doc = model(review)
#     # sentiment = doc._.sentiment.polarity
#     # sentiment = round(sentiment, 2)
#     # return sentiment

#     @spacy.Language.component("get_sentiment")
#     def get_sentiment(review):
#         doc = model(review)
#         sentiment = doc._.sentiment.polarity
#         sentiment = round(sentiment, 2)
    
#         return sentiment


def calculate_sentiment_score(review):

    vader=SentimentIntensityAnalyzer()
    sentiment_score=vader.polarity_scores(str(review))

    
    return sentiment_score


def classify_sentiment(score):
    if score >= 0.05:
        sentiment = 'positive'
    elif -0.05< score <0.05:
        sentiment = 'neutral'
    else:
        sentiment = 'negative'
    return sentiment



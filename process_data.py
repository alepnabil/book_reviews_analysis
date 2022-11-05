from transformation import *
from data_validation import *

def preprocess_data(df):

    print('--preprocessing author columns---')
    # drop rows which have no reviews
    df = df[df['review'].notna()]
    # preprocess review stats columns
    df['author'] = df['reviewer_stats'].str.startswith('Author')
    df['num_author_books'] = df['reviewer_stats'].apply(
        lambda author: get_num_author_books(author) if author.lower().startswith('author') else None)

    df['num_author_followers'] = df['reviewer_stats'].apply(
        lambda author: get_num_author_followers(author) if author.lower().startswith('author') else None)

    df['reviewer_reviews'] = df['reviewer_stats'].apply(
        lambda reviewer: get_num_reviewer_reviews(reviewer) if not (reviewer.lower().startswith('author')) else None)

    df['reviewer_followers'] = df['reviewer_stats'].apply(
        lambda reviewer: get_num_reviewer_followers(reviewer) if not (reviewer.lower().startswith('author')) else None)

    df['reviewer_followers'] = df['reviewer_followers'].apply(lambda follower: multiply_followers(follower))

    df['ratings_given_out_of_5'] = df['ratings_given'].apply(
        lambda rating: get_ratings(rating) if rating.lower().startswith('rating') else None)

    df['review_likes'] = df['review_like'].apply(lambda review: get_review_likes(review))

    df['review_comments'] = df['review_like'].apply(lambda comment: get_review_comments(comment))

    df['language'] = df['review'].apply(classify_language)

    df['clean_review'] = df['review'].apply(lambda x: ' '.join(review for review in x.split() if review not in stop))

    df['sentiment_score'] = df.apply(lambda row: calculate_sentiment_score(row), axis=1)

    df['sentiment'] = df['sentiment_score'].apply(classify_sentiment)

    print(df)
    # df.to_csv('clean_data_spacy_sentiment_24102022.csv', index=False)
    return df


def data_conversion(df):

    df = df.drop(['reviewer_stats', 'ratings_given', 'review_like'], axis=1).copy()

    """
    columns reviewer reviews and followers will be in string 
    since some of them are in thousands (1,200)-->have commas
    """
    df['reviewer_reviews'] = df['reviewer_reviews'].str.replace(',', '')
    df['reviewer_reviews'] = df['reviewer_reviews'].astype(float).astype("Int32")

    df['reviewer_followers'] = df['reviewer_followers'].str.replace(',', '')
    df['reviewer_followers'] = df['reviewer_followers'].astype(float).astype("Int32")

    df['num_author_books'] = df['num_author_books'].astype(float).astype("Int32")

    df['num_author_followers'] = df['num_author_followers'].astype(float).astype("Int32")

    df['ratings_given_out_of_5'] = df['ratings_given_out_of_5'].astype(float).astype("Int8")

    df['review_likes'] = df['review_likes'].astype(float).astype("Int32")

    df['review_comments'] = df['review_comments'].astype(float).astype("Int32")

    return df

def data_validation(df):
    check_num_columns(df)
    column_type_validation(df)
    column_check_validation(df)
    return df



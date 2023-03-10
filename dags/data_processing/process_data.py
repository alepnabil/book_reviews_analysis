from data_processing.data_transformation import *
from data_processing.data_validation import *




def preprocess_data(curr_file_name,language,**kwargs):

    df=pd.read_csv(f'raw_data/{language}/{curr_file_name}.csv')
    print(df.head(5))
    print('--preprocessing author columns---')
    # drop rows which have no reviews
    df = df[df['review'].notna()]

    df.drop_duplicates(subset="review",
                     keep=False, inplace=True)

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
    print(df.head(5))

    sentiment=pd.json_normalize(df['review'].apply(calculate_sentiment_score))
    print(sentiment)
    df=pd.concat([df.reset_index(),sentiment.reset_index()],axis=1)
    print(df.shape)
    print(df.head(5))

    df['sentiment'] = df['compound'].apply(classify_sentiment)
    print('done classify sentiment')

    df.to_csv(f'raw_data/{language}/{curr_file_name}.csv', index=False)

def data_conversion(curr_file_name,language):

    df=pd.read_csv(f'raw_data/{language}/{curr_file_name}.csv',index_col=0)
    df.drop(['reviewer_stats', 'ratings_given', 'review_like'], axis=1,inplace=True)
    print(df.head(5))
    """
    columns reviewer reviews and followers will be in string 
    since some of them are in thousands (1,200)-->have commas
    """
   
    try:
        df['reviewer_reviews'] = df['reviewer_reviews'].str.replace(',', '')
        df['reviewer_reviews'] = df['reviewer_reviews'].str.replace('\n', '')
        df['reviewer_reviews'] = df['reviewer_reviews'].astype(float).astype("Int32")
    except:
        df['reviewer_reviews'] = df['reviewer_reviews'].astype(float).astype("Int32")

    try:
        df['reviewer_followers'] = df['reviewer_followers'].str.replace(',', '')
        df['reviewer_followers'] = df['reviewer_followers'].astype(float).astype("Int32")
    except:
        df['reviewer_followers'] = df['reviewer_followers'].astype(float).astype("Int32")


    try:
        df['num_author_followers'] = df['num_author_followers'].str.replace(',', '')
        df['num_author_followers'] = df['num_author_followers'].str.replace('\n', '')
        df['num_author_followers'] = df['num_author_followers'].astype(float).astype("Int32")
    except:
        df['num_author_followers'] = df['num_author_followers'].astype(float).astype("Int32")


    
    df['num_author_books'] = df['num_author_books'].astype(float).astype("Int32")

    df['ratings_given_out_of_5'] = df['ratings_given_out_of_5'].astype(float).astype("Int8")

    df['review_likes'] = df['review_likes'].astype(float).astype("Int32")

    df['review_comments'] = df['review_comments'].astype(float).astype("Int32")

    print(df.head(5))    
    df.to_csv(f'raw_data/{language}/{curr_file_name}.csv', index=False)
    # print(df.head(10))
    # print(df.shape)

def data_validation(curr_file_name,language):

    df=pd.read_csv(f'raw_data/{language}/{curr_file_name}.csv')
    print(df.head(5))
    check_num_columns(df)
    column_type_validation(df)
    column_check_validation(df)
    df.drop(['index.1'], axis=1,inplace=True)

    df.to_csv(f'clean_data/{language}/{curr_file_name}.csv', index=False)

#preprocess data(import transformation) ---> data conversion ---> data validation

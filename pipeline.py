import time

from scrape_data import Goodreadscraper
import boto3
import os
from botocore.exceptions import ClientError
import logging
from pathlib import Path
import configparser
import io
import pandas as pd
from pandera import Column, DataFrameSchema, Check, Index
import numpy as np
from transformation import *

config_file_path = 'config.ini'
config = configparser.ConfigParser()
config_file_path = config_file_path
config.read(config_file_path)

s3_access_key_id = config['s3']['access_key_id']
s3_secret_access_key = config['s3']['secret_access_key']


def upload_to_s3():
    logging.basicConfig(filename="s3_logs.txt",
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        filemode='a')
    logger = logging.getLogger()

    client = boto3.client('s3',
                          aws_access_key_id=s3_access_key_id,
                          aws_secret_access_key=s3_secret_access_key)

    src_dir = Path("raw_data")
    files_coll = src_dir.glob("*/*")

    try:
        for one_file in files_coll:
            folder = one_file.parent.name
            if folder == "malay":
                upload_file_bucket = 'book-reviews-analysis'
                upload_file_key = 'raw_data/malay/' + str(one_file.name)
                client.upload_file(str(one_file), upload_file_bucket, upload_file_key)
                logger.info('--DONE UPLOADING FILE TO BUCKET--')
            elif folder == 'english':
                upload_file_bucket = 'book-reviews-analysis'
                upload_file_key = 'raw_data/english/' + str(one_file.name)
                client.upload_file(str(one_file), upload_file_bucket, upload_file_key)
                logger.info('--DONE UPLOADING FILE TO BUCKET--')
    except ClientError as e:
        print(e)
        logger.info('--UNABLE TO USE S3--')
    except FileNotFoundError as e:
        logger.info('--FILE IS NOT FOUND--')


def check_files_in_s3():
    bucket_name = 'book-reviews-analysis'
    s3 = boto3.resource('s3',
                        aws_access_key_id=s3_access_key_id,
                        aws_secret_access_key=s3_secret_access_key)
    book_review_analysis_bucket = s3.Bucket(bucket_name)

    english_books_files = []
    malay_books_files = []

    for file in book_review_analysis_bucket.objects.filter(Prefix='raw_data/english'):
        file_name = file.key
        if file_name.endswith('.CSV'):
            english_books_files.append(file_name)
        else:
            pass

    for file in book_review_analysis_bucket.objects.filter(Prefix='raw_data/malay'):
        file_name = file.key
        if file_name.endswith('.CSV'):
            malay_books_files.append(file_name)
        else:
            pass

    english_books_files_num = len(english_books_files)
    malay_books_files_num = len(malay_books_files)

    return english_books_files_num, malay_books_files_num


def load_data_from_s3(language: str):
    df = []
    files_list = []

    bucket_name = 'book-reviews-analysis'
    s3 = boto3.resource('s3',
                        aws_access_key_id=s3_access_key_id,
                        aws_secret_access_key=s3_secret_access_key)
    book_review_analysis_bucket = s3.Bucket(bucket_name)

    for file in book_review_analysis_bucket.objects.filter(Prefix=f'raw_data/{language}'):
        file_name = file.key
        if file_name.endswith('.CSV'):
            files_list.append(file_name)
        else:
            pass

    for file in files_list:
        obj = s3.Object(bucket_name, file)
        data = obj.get()['Body'].read()
        df.append(pd.read_csv(io.BytesIO(data), header=0, delimiter=",", low_memory=False))

    new_df = pd.DataFrame(
        columns=['name', 'review', 'reviewer_stats', 'ratings_given', 'review_like']
    )

    for data in df:
        temp_df = pd.DataFrame(data=data)
        new_df = pd.DataFrame(np.concatenate([new_df.values, temp_df.values]),
                              columns=new_df.columns)

    return new_df


def preprocess_data():
    df = load_data_from_s3('english')

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

    df['ratings_given_out_of_5'] = df['ratings_given'].apply(
        lambda rating: get_ratings(rating) if rating.lower().startswith('rating') else None)

    df['review_likes'] = df['review_like'].apply(lambda review: get_review_likes(review))

    df['review_comments'] = df['review_like'].apply(lambda comment: get_review_comments(comment))

    print(df)
    df.to_csv('preprocess_stats_data.csv', index=False)


def main():
    # scraper = Goodreadscraper('https://www.goodreads.com/book/show/91953.Leviathan', 'bug_testing', 'malay')
    # scraper.scrape_first_page()
    # scraper.scrape_second_page()

    # upload_to_s3()
    # check_files_in_s3()
    # load_data_from_s3('english')
    preprocess_data()


if __name__ == '__main__':
    main()

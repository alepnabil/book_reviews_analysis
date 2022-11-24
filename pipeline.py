import time
from scrape_data import Goodreadscraper
import boto3
from botocore.exceptions import ClientError
import logging
from pathlib import Path
import configparser
import io
from io import StringIO

import numpy as np

from process_data import *
from redshift_functions import *

config_file_path = 'config.ini'
config = configparser.ConfigParser()
config_file_path = config_file_path
config.read(config_file_path)

s3_access_key_id = config['s3']['access_key_id']
s3_secret_access_key = config['s3']['secret_access_key']


def upload_to_s3(parent_folder: str):
    logging.basicConfig(filename="s3_logs.txt",
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        filemode='a')
    logger = logging.getLogger()

    client = boto3.client('s3',
                          aws_access_key_id=s3_access_key_id,
                          aws_secret_access_key=s3_secret_access_key)
    src_dir = Path(f'{parent_folder}')
    files_coll = src_dir.glob("*/*")

    try:
        for one_file in files_coll:
            folder = one_file.parent.name
            if folder == "malay":
                upload_file_bucket = 'book-reviews-analysis'
                upload_file_key = f'{parent_folder}/malay/' + str(one_file.name)
                client.upload_file(str(one_file), upload_file_bucket, upload_file_key)
                logger.info('--DONE UPLOADING FILE TO BUCKET--')
            elif folder == 'english':
                upload_file_bucket = 'book-reviews-analysis'
                upload_file_key = f'{parent_folder}/english/' + str(one_file.name)
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
    files_name = []

    bucket_name = 'book-reviews-analysis'
    s3 = boto3.resource('s3',
                        aws_access_key_id=s3_access_key_id,
                        aws_secret_access_key=s3_secret_access_key)
    book_review_analysis_bucket = s3.Bucket(bucket_name)

    # get all files in the raw data folder
    for file in book_review_analysis_bucket.objects.filter(Prefix=f'raw_data/{language}').all():
        curr_file_name = file.key
        curr_file_name = curr_file_name.split("/")[2]

        file_name = file.key
        if file_name.endswith('.CSV') and curr_file_name.endswith('.CSV'):
            files_list.append(file_name)
            files_name.append(curr_file_name)
        else:
            pass

    new_df = pd.DataFrame(
        columns=['name', 'review', 'reviewer_stats', 'ratings_given', 'review_like']
    )

    # for every file, preprocess the files
    for file, curr_file_name in zip(files_list, files_name):
        obj = s3.Object(bucket_name, file)
        data = obj.get()['Body'].read()
        df.append(pd.read_csv(io.BytesIO(data), header=0, delimiter=",", low_memory=False))
        for data in df:
            temp_df = pd.DataFrame(data=data)
            new_df = pd.DataFrame(np.concatenate([new_df.values, temp_df.values]),
                                  columns=new_df.columns)
            print(curr_file_name)
            process_data(new_df,curr_file_name,language)


def process_data(df,curr_file_name,language):

    df = preprocess_data(df)
    converted_df = data_conversion(df)
    validated_data = data_validation(converted_df)
    validated_data.to_csv(f'clean_data/{language}/{curr_file_name}',index=False)


def main():
    scraper = Goodreadscraper('https://www.goodreads.com/book/show/448836.Second_Treatise_of_Government?ref=nav_sb_ss_1_13', 'second_treatise_of_goverment', 'english')
    scraper.scrape_first_page()
    scraper.scrape_second_page()


    load_data_from_s3('malay')
    upload_to_s3('clean_data')
    load_data_rds('malay')


if __name__ == '__main__':
    main()

import boto3
from data_processing.process_data import *
from data_processing.data_transformation import *
from data_processing.data_validation import *
import pandas as pd
import configparser
import io
import numpy as np

import logging
from pathlib import Path
from botocore.exceptions import ClientError



config_file_path = 'dags/config.ini'
config = configparser.ConfigParser()
config_file_path = config_file_path
config.read(config_file_path)

s3_access_key_id = config['s3']['access_key_id']
s3_secret_access_key = config['s3']['secret_access_key']

def load_data_from_s3(language: str, book_name: str, **kwargs):
    """

    Used only to load raw data file from S3.
    Load specific file to pull from and S3 for data processing.

    :param language: specific language
    :param book_name: specific book name to avoid pulling all files in the folder

    """

    print('----LOADING DATA FROM S3----')
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

        # for saving file name convention
        curr_file_name = file.key
        curr_file_name = curr_file_name.split("/")[2]
        # for reading from S3 to a dataframe convention
        file_name = file.key

        if file_name.endswith('.csv') and curr_file_name.endswith('.csv') and book_name in file_name:
            files_list.append(file_name)
            files_name.append(curr_file_name)
        else:
            pass

    new_df = pd.DataFrame(
        columns=['book_author','book_name','name', 'review', 'reviewer_stats', 'ratings_given', 'review_like']
    )

    # for every file, preprocess the files
    for file, curr_file_name in zip(files_list, files_name):
        obj = s3.Object(bucket_name, file)
        data = obj.get()['Body'].read()
        df.append(pd.read_csv(io.BytesIO(data), header=0, delimiter=",", low_memory=False, encoding='latin-1'))
        for data in df:
            temp_df = pd.DataFrame(data=data)
            new_df = pd.DataFrame(np.concatenate([new_df.values, temp_df.values]),
                                  columns=new_df.columns)
            print(curr_file_name)
            new_df.to_csv(f'raw_data/{language}/{curr_file_name}', index=False)

    print(new_df)


def upload_to_s3(parent_folder: str, **kwargs):
    """
    Upload only a specific file in local directory to S3 bucket. Local directory should contain only 1 specific book file.

    :param parent_folder: raw_data or clean_data
    """

    config_file_path = 'dags/config.ini'
    config = configparser.ConfigParser()
    config_file_path = config_file_path
    config.read(config_file_path)

    s3_access_key_id = config['s3']['access_key_id']
    s3_secret_access_key = config['s3']['secret_access_key']
    
    logging.basicConfig(filename="s3_logs.txt",
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        filemode='a')
    logger = logging.getLogger()

    print('------UPLOADING FILES TO S3------')
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
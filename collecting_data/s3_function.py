import configparser
import logging
import boto3
from pathlib import Path
from botocore.exceptions import ClientError
import pandas as pd


config_file_path = 'dags/config.ini'
config = configparser.ConfigParser()
config_file_path = config_file_path
config.read(config_file_path)

s3_access_key_id = config['s3']['access_key_id']
s3_secret_access_key = config['s3']['secret_access_key']


#USE THIS FILE TO JUST CONFIGURE PIPELINE. NOT TO BE USED INSIDE THE CONTAINER

def upload_to_s3(parent_folder: str):
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


def check_files_in_s3():
    """
    :return: number of files in S3 bucket.
    """
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





if __name__ == '__main__':
    upload_to_s3()

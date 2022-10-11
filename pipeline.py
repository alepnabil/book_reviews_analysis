from scrape_data import Goodreadscraper
import boto3
import os
from botocore.exceptions import ClientError
import logging
from secrets import access_key_id,secret_access_key
from pathlib import Path
import glob




def upload_to_s3():


    logging.basicConfig(filename="s3_logs.txt",
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        filemode='a')
    logger = logging.getLogger()

    client=boto3.client('s3',
                        aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key)




    src_dir = Path("raw_data")
    files_coll = src_dir.glob("*/*")


    try:
        for one_file in files_coll:
            folder = one_file.parent.name
            if folder == "malay":
                upload_file_bucket = 'book-reviews-analysis'
                upload_file_key = 'malay/' + str(one_file.name)
                client.upload_file(str(one_file), upload_file_bucket, upload_file_key)
                logger.info('--DONE UPLOADING FILE TO BUCKET--')
            elif folder == 'english':
                upload_file_bucket = 'book-reviews-analysis'
                upload_file_key = 'english/' + str(one_file.name)
                client.upload_file(str(one_file), upload_file_bucket, upload_file_key)
                logger.info('--DONE UPLOADING FILE TO BUCKET--')
    except ClientError as e:
        print(e)
        logger.info('--UNABLE TO USE S3--')
    except FileNotFoundError as e:
        logger.info('--FILE IS NOT FOUND--')





def main():
    # scraper = Goodreadscraper('https://www.goodreads.com/book/show/50535410-seni-berfikir-yang-hilang', 'bug_testing', 'malay')
    # scraper.scrape_first_page()
    # scraper.scrape_second_page()

    upload_to_s3()

if __name__ == '__main__':
    main()
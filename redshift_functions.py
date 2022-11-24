import redshift_connector
import configparser
import boto3

config_file_path = 'config.ini'
config = configparser.ConfigParser()
config_file_path = config_file_path
config.read(config_file_path)

dwh_endpoint = config['redshift']['dwh_endpoint']
db_name = config['redshift']['db_name']
username = config['redshift']['username']
rds_password = config['redshift']['rds_password']
port = int(config['redshift']['port'])
iam_role = config['redshift']['iam_role']

s3_access_key_id = config['s3']['access_key_id']
s3_secret_access_key = config['s3']['secret_access_key']


def load_data_rds(language):

    print('loading into rds')
    clean_data_files = []
    # get all the clean files in 'malay' folder

    bucket_name = 'book-reviews-analysis'
    s3 = boto3.resource('s3',
                        aws_access_key_id=s3_access_key_id,
                        aws_secret_access_key=s3_secret_access_key)
    book_review_analysis_bucket = s3.Bucket(bucket_name)

    for file in book_review_analysis_bucket.objects.filter(Prefix=f'clean_data/{language}'):
        file_name = file.key
        if file_name.endswith('.CSV'):
            clean_data_files.append(file_name)
        else:
            pass

    conn = redshift_connector.connect(
        host=dwh_endpoint,
        database=db_name,
        user=username,
        password=rds_password,
        port=port
    )

    cursor = conn.cursor()
    # for every of those file in the folder, we want to append to our table
    
    for file in clean_data_files:
        cursor.execute(f"""
            
            copy book_testing5 
            from 's3://book-reviews-analysis/{file}'
            iam_role '{iam_role}'
            
            FORMAT AS CSV
            IGNOREHEADER 1
            
            """)

    conn.commit()


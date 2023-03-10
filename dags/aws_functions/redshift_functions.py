import configparser
import boto3
import psycopg2

# from airflow import settings
# from airflow.models import Connection

config_file_path = 'dags/config.ini'
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




def load_data_main_table_rds(book_name:str,language:str):

    
    print('-----LOADING DATA INTO RDS-----')
    clean_data_files = []
    # get all the clean files in 'malay' folder

    bucket_name = 'book-reviews-analysis'
    s3 = boto3.resource('s3',
                        aws_access_key_id=s3_access_key_id,
                        aws_secret_access_key=s3_secret_access_key)
    book_review_analysis_bucket = s3.Bucket(bucket_name)

    conn = psycopg2.connect(host=dwh_endpoint, port=port, dbname=db_name, user=username, password=rds_password)

    cursor = conn.cursor()

    for file in book_review_analysis_bucket.objects.filter(Prefix=f'clean_data/{language}/{book_name}'):

        if file.key.endswith('csv'):

            file_name = file.key

            cursor.execute(f"""

                copy main_table
                from 's3://book-reviews-analysis/{file_name}'
                iam_role '{iam_role}'

                FORMAT AS CSV
                IGNOREHEADER 1

                """)

        conn.commit()
        cursor.close()
        conn.close()
        # print(f'----LOADING {file_name} INTO RDS----')
        # if file_name.endswith('.csv'):
        #     clean_data_files.append(file_name)
        # else:
        #     pass



    # conn = redshift_connector.connect(
    #     host=dwh_endpoint,
    #     database=db_name,
    #     user=username,
    #     password=rds_password,
    #     port=port
    # )

    # cursor = conn.cursor()
    # # for every of those file in the folder, we want to append to our table

    # for file in clean_data_files:
    #     cursor.execute(f"""

    #         copy book
    #         from 's3://book-reviews-analysis/{file}'
    #         iam_role '{iam_role}'

    #         FORMAT AS CSV
    #         IGNOREHEADER 1

    #         """)

    # conn.commit()

    # for obj in s3.Bucket('YOUR_S3_BUCKET_NAME').objects.filter(Prefix='YOUR_S3_PREFIX'):

    # # check if object is a CSV file
    # if obj.key.endswith('.csv'):
        
    #     # get the S3 file path
    #     s3_path = f's3://{obj.bucket_name}/{obj.key}'
        
    #     # execute a Redshift COPY command to load data from S3 to Redshift
    #     cur.execute(f"""
    #         COPY YOUR_REDSHIFT_TABLE
    #         FROM '{s3_path}'
    #         IAM_ROLE '{iam_role}'
    #         FORMAT AS CSV
    #         IGNOREHEADER 1
    #     """)
        
    # # commit the changes and close the cursor and connection
    # conn.commit()
    # cur.close()
    # conn.close()

# load_data_main_table_rds('politik_untuk_pemula','malay')
def insert_data_into_tables():
    
    conn = psycopg2.connect(
        host=dwh_endpoint, 
        port=port, 
        dbname=db_name, 
        user=username, 
        password=rds_password)

    print('--inserrting data--')
    # Open the SQL file and read the contents
    with open('dags/aws_functions/insert_data.sql', 'r') as file:
        sql = file.read()
    
    # Execute the SQL statement
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()
    print('--done uploading data--')



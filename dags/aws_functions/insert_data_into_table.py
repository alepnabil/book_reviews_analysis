import psycopg2
import configparser




def insert_data_into_tables():
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



    conn = psycopg2.connect(
        host=dwh_endpoint, 
        port=port, 
        dbname=db_name, 
        user=username, 
        password=rds_password)


    # Open the SQL file and read the contents
    with open('insert_data_into_table', 'r') as file:
        sql = file.read()

    # Execute the SQL statement
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

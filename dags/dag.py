from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.models import Variable

from aws_functions.s3_functions import *
from data_processing.process_data import *
from aws_functions.redshift_functions import *


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(5)
}


dag_variable=Variable.get("dag_variable",deserialize_json=True)
language=dag_variable["language"]
book_name=dag_variable["book_name"]
clean_data_folder=dag_variable["clean_data_folder"]


process_data_dag = DAG(
    'process_data',
    default_args=default_args,
    description='Aggregates booking records for data analysis',
    schedule_interval=timedelta(days=1),
    catchup=False
)



task_1=PythonOperator(
        task_id='load_data',
        python_callable=load_data_from_s3,
        op_kwargs={'language':language,'book_name':book_name},
        dag=process_data_dag
)

task_2=PythonOperator(
        task_id='preprocessing_data',
        python_callable=preprocess_data,
        op_kwargs={'curr_file_name':book_name,'language':language},
        dag=process_data_dag
)

task_3=PythonOperator(
        task_id='convert_data',
        python_callable=data_conversion,
        op_kwargs={'curr_file_name':book_name,'language':language},
        dag=process_data_dag
)

task_4=PythonOperator(
        task_id='data_validation',
        python_callable=data_validation,
        op_kwargs={'curr_file_name':book_name,'language':language},
        dag=process_data_dag
)

task_5=PythonOperator(
        task_id='load_data_to_s3',
        python_callable=upload_to_s3,
        op_kwargs={'parent_folder': clean_data_folder},
        dag=process_data_dag
)

# task_6=PythonOperator(
#         task_id='load_data_to_main_table_rds',
#         python_callable=load_data_main_table_rds,
#         op_kwargs={'book_name':book_name,'language':language},
#         dag=process_data_dag
# )

# task_7=PythonOperator(
#         task_id='insert_data_into_tables',
#         python_callable=insert_data_into_tables,
#         dag=process_data_dag
# )



task_1 >> task_2 >> task_3 >> task_4 >> task_5 
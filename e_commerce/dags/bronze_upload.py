from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import PythonOperator
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")
LOCAL_FILE_PATH = "/opt/airflow/data"

def upload():
    s3_hook = S3Hook(aws_conn_id='aws_default')

    files = os.listdir(LOCAL_FILE_PATH)

    for file_name in files:
        local_file_path = os.path.join(LOCAL_FILE_PATH, file_name)

        s3_hook.load_file(
            filename=local_file_path,
            key=f"bronze/{file_name}",
            bucket_name=BUCKET_NAME,
            replace=True
        )

with DAG(
    dag_id = "upload_to_s3",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",   
    catchup=False
) as dag:

    upload_to_s3 =PythonOperator(
        task_id = "upload_to_s3",
        python_callable=upload
    )


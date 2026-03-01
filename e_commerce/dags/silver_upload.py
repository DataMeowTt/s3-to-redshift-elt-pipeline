from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

default_args = {
    "owner": "me",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
    dag_id="spark_partition_list_order",
    default_args=default_args,
    schedule=None,
    catchup=False,
) as dag:

    spark_partition_task = SparkSubmitOperator(
        task_id="partition_list_order",
        application="/opt/airflow/dags/spark_jobs/partition.py",
        conn_id="spark_default",
        verbose=True,
        conf={
            "spark.master": "spark://spark-master:7077",
            "spark.hadoop.fs.s3a.endpoint": "s3.amazonaws.com",
        },
        packages="org.apache.hadoop:hadoop-aws:3.3.4",
    )

    # Other transformation for silver layer can be added here, and set spark_partition_task as downstream of those tasks

    spark_partition_task
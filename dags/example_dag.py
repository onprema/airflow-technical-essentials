"""
This is an example of a DAG
"""
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator


default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(seconds=30),
    'do_xcom_push': False
}

dag = DAG(
    dag_id='example_dag',
    description='Just an example DAG',
    start_date=datetime(2021, 1, 1),
    schedule_interval='0 0 * * *',
    catchup=False,
    default_args=default_args
)

# Operators: https://airflow.apache.org/docs/stable/_api/airflow/operators/index.html
task_1 = BashOperator(
    task_id='hello_task',
    bash_command='echo "Hello"',
    dag=dag
)

task_2 = BashOperator(
    task_id='curl_task',
    bash_command='curl http://example.com',
    dag=dag
)

# task_2 depends on task_1
task_1 >> task_2

"""
This is an example of a DAG.
Things to explore:
    - DAG: https://github.com/apache/airflow/blob/main/airflow/models/dag.py
    - Operators: https://github.com/apache/airflow/tree/main/airflow/operators
    - Provider Operators: https://pypi.org/search/?q=apache-airflow-providers&o=-created&c=Framework+::+Apache+Airflow+::+Provider
    - Tasks: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html
"""
import textwrap
from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="example_dag",
    description="This is an example DAG",
    default_args={
        "owner": "airflow",
        "retries": 3,
        "retry_delay": timedelta(seconds=30),
        "do_xcom_push": False,
    },
    start_date=datetime(2024, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
) as dag:
    hello_task = BashOperator(task_id="hello_task", bash_command='echo "Hello"')
    curl_task = BashOperator(task_id="curl_task", bash_command="curl http://example.com")

    @task()
    def goodbye():
        print('goodbye!')

    # curl_task and goodbye depend on hello_task
    hello_task >> [curl_task, goodbye()]

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
from airflow.models.dag import DAG
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
    task_1 = BashOperator(task_id="hello_task", bash_command='echo "Hello"')
    task_2 = BashOperator(task_id="curl_task", bash_command="curl http://example.com")
    task_2.doc_md = textwrap.dedent(
        """
        ## Task 2 documentation
        This task uses `curl` to **send a GET request** to _example.com_
        ![img](https://www.booleanworld.com/wp-content/uploads/2018/12/curl-cover-picture.png)
        """
    )

    dag.doc_md = __doc__

    # https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html
    templated_command = textwrap.dedent(
        """
        {% for n in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds, 7) }}"
        {% endfor %}
        """
    )
    task_3 = BashOperator(task_id="templated_task", bash_command=templated_command)

    # task_2 depends on task_1
    task_1 >> [task_2, task_3]

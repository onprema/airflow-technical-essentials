"""
This is an example of a DAG using the taskflow API
- Uses task decorators
- Automatically xcom pushes the return value
"""
from datetime import datetime
import subprocess
from airflow.decorators import dag, task


@dag(start_date=datetime(2022, 1, 1), schedule_interval='@hourly', tags=['examples'])
def taskflow_example():

    @task
    def hello():
        return str(subprocess.check_output(['echo', 'hello']))
    
    @task(task_id='curl_task', retries=3)
    def curl():
        return str(subprocess.check_output(['curl', 'http://example.com']))
    
    hello() >> curl()

dag = taskflow_example()
"""
Try to query the airflow metastore in our DAG
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(seconds=30),
    'do_xcom_push': False
}

dag = DAG(
    dag_id='query_dag',
    start_date=datetime(2020, 1, 1),
    schedule_interval='0 0 * * *', # midnight everyday
    default_args=default_args,
    catchup=False
)

def get_query_results():
    sql = 'select * from dag'
    pg_hook = PostgresHook(postgres_conn_id='airflow_conn')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        print(result)

with dag:
    run_query = PythonOperator(
        task_id='run_query',
        python_callable=get_query_results 
    )
    run_query

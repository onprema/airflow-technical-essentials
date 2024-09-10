from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.models import Variable
import requests
import json
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(default_args=default_args, schedule_interval=timedelta(days=1), start_date=days_ago(1), catchup=False)
def open_library_book_info_taskflow():
    
    @task()
    def fetch_book_info():
        """
        Fetches information about a book from the Open Library API
        """
        book_isbn = Variable.get("ISBN_NUMBER", default_var="0451526538")
        url = f"https://openlibrary.org/isbn/{book_isbn}.json"
        response = requests.get(url)
        return response.json()

    @task()
    def fetch_author_info(book_info: dict):
        author_key = book_info['authors'][0]['key']
        url = f"https://openlibrary.org{author_key}.json"
        response = requests.get(url)
        return response.json()

    @task()
    def analyze_info(book_info: dict, author_info: dict):
        analysis = {
            'book_title': book_info['title'],
            'publish_date': book_info.get('publish_date', 'Unknown'),
            'author_name': author_info['name'],
            'author_birth_date': author_info.get('birth_date', 'Unknown'),
        }
        print(json.dumps(analysis, indent=2))
        return analysis

    # Define the flow of tasks
    book_info = fetch_book_info()
    author_info = fetch_author_info(book_info)
    analyze_info(book_info, author_info)

# Create the DAG
open_library_dag = open_library_book_info_taskflow()
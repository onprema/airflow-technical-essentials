"""
This DAG uses the weather.gov API to generate a weather report for a pair of lat/long coordinates
Info: https://weather-gov.github.io/api/general-faqs
TODO:
    - Make connection from Web UI (http_conn_id='http_weather_api')
        - Host: https://api.weather.gov/points/
    - Add weather_coordinates variable to Variables from Web UI
        - Format: 39.7456,-97.0892
"""
import json
from datetime import datetime
import requests
from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.operators.python import PythonOperator


default_args = {
    "owner": "airflow",
    "retries": 0,
    "start_date": datetime(2021, 1, 1),
    "queue": "weather_queue",
}

dag = DAG(
    dag_id="weather_checker",
    description="Check the weather",
    schedule_interval="0 0 * * 1",  # midnight on Mondays
    default_args=default_args,
    catchup=False,
)


def parse_response(**context):
    """
    Parses the forecast endpoint from the weather metadata response.
    Located at properties.forecast
    """

    # For learning purposes, let's see what is in the context
    print("========== START CONTEXT ==========")
    for key, val in context.items():
        print(str(key) + " => " + str(val))
    print("========== END CONTEXT ==========")

    # pull metadata response from xcom
    response_string = context.get("task_instance").xcom_pull(
        task_ids="get_location_metadata"
    )

    json_response = json.loads(response_string)
    forecast_url = json_response.get("properties").get("forecast")

    # push the forecast url for the next task
    context.get("task_instance").xcom_push(key="forecast_url", value=forecast_url)


def print_forecast(**context):
    """
    Prints the detailed weather forecast
    """
    # pull the forecase url using xcom
    forecast_url = context.get("task_instance").xcom_pull(key="forecast_url")

    # make the request and transform to a dictionary
    response = requests.get(forecast_url).json()
    assert "properties" in response.keys()

    # print out the forecast for the week
    periods = response.get("properties").get("periods")
    for period in periods:
        period_name = period.get("name")
        forecast = period.get("detailedForecast")
        print(period_name + ": " + forecast)


with dag:  # new syntax, automatically associates all tasks to the above DAG
    get_location_metadata = HttpOperator(
        task_id="get_location_metadata",
        http_conn_id="http_weather_api",
        method="GET",
        response_check=lambda response: "forecast" in response.text,
        endpoint="{{ var.value.weather_coordinates }}",
        do_xcom_push=True,  # pushes response.text
    )

    parse_metadata_response = PythonOperator(
        task_id="parse_metadata_response",
        python_callable=parse_response,
        provide_context=True,
        do_xcom_push=True,
    )

    print_weekly_forecast = PythonOperator(
        task_id="print_weekly_forecast",
        python_callable=print_forecast,
        provide_context=True,
    )

    get_location_metadata >> parse_metadata_response >> print_weekly_forecast

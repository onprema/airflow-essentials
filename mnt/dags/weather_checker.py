"""
This DAG uses the weather.gov API to generate a weather report for 
a pair of lat/long coordinates

Info: https://weather-gov.github.io/api/general-faqs
"""
import json
import requests
from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'start_date': datetime(2020, 1, 1),
    'queue': 'weather_queue'
}

dag = DAG(
    dag_id='weather_checker',
    description='Check the weather',
    schedule_interval='0 0 * * 1', # midnight on Mondays
)

def parse_response(**context):
    """
    Parses the forecast endpoint from the weather metadata response.
    Located at properties.forecast
    """

    # For learning purposes, let's see what is in the context
    print('========== START CONTEXT ==========')
    for key, val in context.items():
        print(f'{key} => {val}')
    print('========== END CONTEXT ==========')

    # pull metadata response from xcom
    response_string = context.get('task_instance').xcom_pull(task_ids='get_location_metadata')

    json_response = json.loads(response_string)
    forecast_url = json_response.get('properties').get('forecast')

    # push the forecast url for the next task
    context.get('task_instance').xcom_push(key='forecast_url', value=forecast_url)


with dag: # new syntax, automatically associates all tasks to the above DAG

    get_location_metadata = SimpleHttpOperator(
        task_id='get_location_metadata',
        http_conn_id='http_weather_api',
        method='GET',
        response_check=lambda response: 'forecast' in response.text,
        endpoint='{{ var.value.weather_coordinates }}',
        xcom_push=True # pushes response.text
    )

    parse_metadata_response = PythonOperator(
        task_id='parse_metadata_response',
        python_callable=parse_response,
        provide_context=True,
        do_xcom_push=True
    )

    get_forecast = PythonOperator(
        task_id='get_location_metadata',
        python_callable=print_forecast
    )

def print_forecast(**context):
    """
    Prints the detailed weather forecast
    """

    # pull the forecase url using xcom
    forecast_url = context.get('task_instance').xcom_pull(key='forecast_url')

    # make the request and transform to a dictionary
    response = requests.get(forecast_url).json
    assert 'detailedForecast' in response

    # print out the forecast for the week
    periods = response.get('properties').get('periods')
    for period in periods:
        print(f'{period.get("name")}: {period.get("detailedForecast")}')
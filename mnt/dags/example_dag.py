"""
This is an example of a very basic DAG
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(seconds=30)
}

dag = DAG(
    dag_id='example_dag',
    description='Just an example DAG',
    schedule_interval='0 0 * * *',
    catchup=False,
    default_args=default_args
)

# Operators: https://airflow.apache.org/docs/stable/_api/airflow/operators/index.html
task_1 = BashOperator(
    task_id='task_1',
    bash_command='echo "Hello from task_1"',
    dag=dag
)

task_2 = BashOperator(
    task_id='task_2',
    bash_command='cat /etc/hosts',
    dag=dag
)

# task_2 depends on task_1
task_1 >> task_2

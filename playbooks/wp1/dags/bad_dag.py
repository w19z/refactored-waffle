from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',


dag = DAG(
    'simple_dag',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval='0 12 * * *',
    start_date=days_ago(2),
    tags=['example'],
)

start = DummyOperator(
    task_id='run_this_first',
    dag=dag,
)

middle = DummyOperator(
    task_id='run_this_second',
    dag=dag,
)

end = DummyOperator(
    task_id='run_this_last',
    dag=dag,
)

start >> middle >> end

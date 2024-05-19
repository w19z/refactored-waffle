import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import PythonVirtualenvOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from random import random, randint

dag = DAG(
   "prediction_pipeline",
   start_date=datetime(2024, 4, 3, 20, 0),
   schedule_interval='0 20 * * MON,TUE,WED,THU,FRI',
)


POSTGRES_CONN_ID = "postgres_new"
SQL_QUERY = """
    INSERT INTO second_table (id, col1, col2)
    VALUES (%s, %s, %s)
"""

def insert_func():
    """Inserts data into the stock_prices table."""
    postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(SQL_QUERY, (
        randint(1, 100),
        round(random()*100, 2),
        round(random()*100, 2),
    ))
    connection.commit()
    cursor.close()
    connection.close()



insert_data_task = PythonOperator(
    task_id="insert_data",
    python_callable=insert_func,
    provide_context=True,
    dag=dag,
)


insert_data_task

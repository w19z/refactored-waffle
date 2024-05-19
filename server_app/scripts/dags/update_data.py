from random import random
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime


dag = DAG(
   "update_data",
   start_date=datetime(2024, 4, 3, 9, 0),
   schedule_interval='*/15 * * * MON,TUE,WED,THU,FRI',
)


current_date = datetime.now().strftime('%Y-%m-%d')


data = {
    "date"  : current_date,
    "col1"  : round(random()*100, 2),
    "col2"  : round(random()*100, 2),
    "col3"  : round(random()*100, 2),
}


POSTGRES_CONN_ID = "postgres_new"
SQL_QUERY = """
    INSERT INTO first_table (date, col1, col2, col3)
    VALUES (%s, %s, %s, %s)
"""


def insert_func():
    """Inserts data into the first_table table."""
    postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(SQL_QUERY, (
        data.get("date"),
        data.get("col1"),
        data.get("col2"),
        data.get("col3"),
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

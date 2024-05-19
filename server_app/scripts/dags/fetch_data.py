import pandas as pd
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.utils.dates import datetime


dag = DAG(
   "fetch_data",
   start_date=datetime(2024, 4, 3, 23, 0),
   schedule_interval='0 23 * * FRI',
)

POSTGRES_CONN_ID = "postgres_new"
SQL_QUERY = "SELECT * FROM first_table;"

def fetch_data_from_postgres():
    """Fetch data from Postgres and return it as a list of tuples."""
    postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(SQL_QUERY)
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    return result

fetch_data_task = PythonOperator(
    task_id="fetch_data",
    python_callable=fetch_data_from_postgres,
    provide_context=True,
    dag=dag,
)

def save_as_csv(**kwargs):
    """Save the fetched data as a CSV file."""
    ti = kwargs["ti"]
    result = ti.xcom_pull(task_ids="fetch_data")
    if result:
        df = pd.DataFrame(result)
        df.to_csv("/opt/airflow/data/new_data.csv", index=False)

save_as_csv_task = PythonOperator(
    task_id="save_as_csv",
    python_callable=save_as_csv,
    provide_context=True,
    dag=dag,
)

fetch_data_task >> save_as_csv_task

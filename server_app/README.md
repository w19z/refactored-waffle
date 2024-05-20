# mlops_xflow

Сервисы:
- app
- apache airflow
- jupyterhub
- postgres


Запуск:
1. `docker compose up`
2. Запустить в airflow контейнере команды:
    - `airflow db init`
    - `airflow scheduler`
    - настроить postgres connection в airflow settings (all postgres, host: db)
3. DAGs поместить в папку data/dags
4. 'enable_xcom_pickling' in airflow.cfg

Credentials:
- jupyterhub ('admin' - 'password)
- airflow ('admin' - 'password)

Вариант использования:

- Загрузка и оркестрирование данных через airflow.
- Выгрузка предсказанный значений в таблицу

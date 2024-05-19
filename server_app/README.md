# HW_3_mlops_xflow

Домашнее задание № 3 "Автоматизация администрирования MLOps II"

Описание:

Инфраструктура для проекта машинного обучения на примере обработки временного ряда.

Сервисы:
- app
- apache airflow
- mlflow
- jupyterhub
- postgres

Перед запуском:

- добавить в переменную для airflow ваш api ключ для tiingo (tiingo.com)

Запуск:
1. `docker compose up`
2. Запустить в airflow контейнере команды:
    - `airflow db init`
    - `airflow scheduler`
    - настроить postgres connection в airflow settings (all postgres, host: db)
3. DAGs поместить в папку data/dags
4. 'chmod 777 /home/admin/project_1' in jupyter app
5. 'enable_xcom_pickling' in airflow.cfg

Credentials:
- jupyterhub ('admin' - 'password)
- airflow ('admin' - 'password)

Вариант использования:

- Загрузка и оркестрирование данных через airflow.
- Выгрузка предсказанный значений в таблицу

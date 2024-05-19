#!/bin/sh

docker exec -it airflow airflow db init
docker exec -d airflow airflow scheduler
docker exec -it airflow airflow connections add "postgres_new" \
    --conn-type "postgres" \
    --conn-login "postgres" \
    --conn-password "postgres" \
    --conn-host "db" \
    --conn-port "5432" \
    --conn-schema "postgres"
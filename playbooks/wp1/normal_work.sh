#!/bin/bash

while true; do
    if (( RANDOM % 2)); then
        curl -X GET http://192.168.56.25:5005/endpoint1
    else
	random_number=$(( RANDOM % 100 + 1 ))
        curl -X POST http://192.168.56.25:5005/endpoint2 \
             -H 'accept: application/json' \
             -H 'Content-Type: application/json' \
             -d "{\"id\": $random_number}"
    fi
    sleep $(( RANDOM % 245 + 45 ))
    echo "\n"
done

#!/bin/bash


curl -X 'POST' \
  'http://192.168.56.25:5005/endpoint3' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@dags/bad_dag.py'

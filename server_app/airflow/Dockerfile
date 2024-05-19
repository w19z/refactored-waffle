FROM apache/airflow:2.2.0
EXPOSE 8080
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["airflow", "webserver", "--port", "8080", "--host", "0.0.0.0", "--daemon"]

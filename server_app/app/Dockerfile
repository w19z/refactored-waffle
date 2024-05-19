FROM python:3.10
WORKDIR /app
RUN mkdir -p /app/data
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
EXPOSE 5005
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5005"]

FROM python:3.8-alpine

RUN mkdir -p /code/data
WORKDIR /code

ENV FLASK_CONFIG=production

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app app
COPY make_celery.py make_celery.py

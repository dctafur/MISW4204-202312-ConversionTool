FROM python:3.11.3-alpine

RUN apk add build-base linux-headers
WORKDIR /code

ENV FLASK_CONFIG=production

RUN mkdir -p data

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app app
COPY make_celery.py make_celery.py

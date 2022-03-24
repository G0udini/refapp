FROM python:3.9-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY entrypoint.sh entrypoint.sh

RUN chmod +x entrypoint.sh

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get -y install postgresql-client 

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
    
COPY . .
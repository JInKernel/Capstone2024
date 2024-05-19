# Dockerfile
FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirement.txt /code/
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config
RUN pip install --upgrade pip
RUN pip install -r requirement.txt
RUN pip install mysqlclient

COPY . /code/


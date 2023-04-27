FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .
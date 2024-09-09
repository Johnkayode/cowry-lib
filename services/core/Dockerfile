FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /core_app

WORKDIR /core_app

COPY . .

RUN chmod +x entrypoint.sh

RUN pip install --upgrade pip && pip install -r requirements.txt

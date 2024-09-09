FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /admin_app

WORKDIR /admin_app

COPY . .

RUN chmod +x entrypoint.sh

RUN pip install --upgrade pip && pip install -r requirements.txt
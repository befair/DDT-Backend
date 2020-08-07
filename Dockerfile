FROM python:3-slim-buster
MAINTAINER beFair "sysadmin@befair.it"
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install gcc -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app/

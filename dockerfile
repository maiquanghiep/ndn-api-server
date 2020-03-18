 FROM python:3.7.3-alpine3.9

RUN mkdir -p /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt





COPY ./ /app/

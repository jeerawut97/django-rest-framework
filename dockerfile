FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /django-rest-framework

WORKDIR /django-rest-framework

COPY . .

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

# RUN adduser -D user
# USER user
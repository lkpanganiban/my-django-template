FROM python:3.9.10-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LIBRARY_PATH=/lib:/usr/lib

RUN apk update \
    && apk add libpq postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev curl build-base libressl-dev libffi-dev geos-dev nodejs npm

# set work directory
WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app

RUN mkdir -p /var/log/django-app

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

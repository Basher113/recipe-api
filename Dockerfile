FROM python:3.12.9-alpine3.21
LABEL org.opencontainers.image.authors="akalimonde@gmail.com"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITECODE=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

WORKDIR /app

COPY ./app .

EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # Required deps to install psycopg2 inside alpine linux 
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # delete the .tmp-build-deps directory since psycopg2 is installed already on line 23
    apk del .tmp-build-deps && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/py/bin:$PATH"

USER django-user
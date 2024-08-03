FROM python:3.11.4-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    libpq-dev gcc

RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

CMD exec gunicorn flix.wsgi -b 0.0.0.0:${PORT} --log-level debug

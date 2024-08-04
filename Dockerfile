FROM python:3.11.4-slim-bullseye
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "gunicorn", "flix.wsgi", "-b", "0.0.0.0:80"]

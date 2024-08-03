FROM python:3.11.4-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Environment variables to prevent Python from buffering and writing bytecode
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app

# Entry point for Gunicorn, using the PORT environment variable
CMD ["gunicorn", "flix.wsgi", "-b", "0.0.0.0:${PORT}"]

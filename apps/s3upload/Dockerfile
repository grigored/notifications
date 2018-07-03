# Use an official Python runtime as a base image
FROM python:3.6.1

RUN apt-get update && apt-get install -y \
locales \
locales-all

# Set the working directory to /app
RUN mkdir -p /app
WORKDIR /app

# Define environment variable
ENV PYTHONPATH=/app/ \
LC_ALL=en_US.UTF-8 \
LANG=en_US.UTF-8 \
LANGUAGE=en_US.UTF-8

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./src /app/src

CMD gunicorn -c src/configs/gunicorn_conf.py src.wsgi.wsgi:app

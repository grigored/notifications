# Use an official Python runtime as a base image
FROM python:3.6.1

# Install wkhtmltopdf (and clean after)
RUN wget https://s3.amazonaws.com/instacarshare/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
unxz wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
tar -xvf wkhtmltox-0.12.4_linux-generic-amd64.tar && \
mv wkhtmltox/bin/wkhtmltopdf /usr/bin/wkhtmltopdf && \
rm -rf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz \
    wkhtmltox-0.12.4_linux-generic-amd64.tar \
    wkhtmltox

RUN apt-get update && apt-get install -y \
wget \
locales \
locales-all

# Set the working directory to /app
WORKDIR /app

# Make port 8000 available to the world outside this container
EXPOSE 8001 8002

# Define environment variable
ENV AWS_ACCESS_KEY_ID="" \
AWS_SECRET_ACCESS_KEY="" \
AWS_DEFAULT_REGION="" \
PYTHONPATH=/app/app/ \
LC_ALL=en_US.UTF-8 \
LANG=en_US.UTF-8 \
LANGUAGE=en_US.UTF-8

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

CMD gunicorn -c app/src/configs/gunicorn_conf.py app.src.wsgi.wsgi:app

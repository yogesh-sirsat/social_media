# Python and Alpine version can be found here: https://hub.docker.com/_/python 
FROM python:3.11.0a5-alpine3.14

# Define environment variable
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN  set -ex \
    && pip install --upgrade pip \
    && pip install -r requirements_docker.txt 

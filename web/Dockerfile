# pull official base image
FROM python:3.9-bullseye

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app
RUN --mount=type=cache,target=/root/.cache/pip \
  pip3 install -r requirements.txt

# copy project
COPY . /usr/src/app

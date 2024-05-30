FROM python:3.12-alpine as base 

# setting up env 
ENV LANG C.UTF-8 
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1 

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apk add --no-cache make build-base
RUN apk add --no-cache bash mariadb-dev mariadb-client mariadb-connector-c-dev python3-dev build-base

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt
RUN pip install mysqlclient

# Install application into container
COPY . /app
# CMD python /app/manage.py runserver 0.0.0.0:8000

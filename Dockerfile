FROM python:3.8

RUN apt-get update &&\
    apt-get install liblapack-dev libblas-dev gfortran -y
RUN pip install poetry

ENV POETRY_VIRTUALENVS_PATH=/root/.cache/pypoetry/virtualenvs/

WORKDIR /cs-insights-prediction-endpoint
COPY . /cs-insights-prediction-endpoint
COPY test.env /cs-insights-prediction-endpoint/.env

RUN poetry install --no-dev
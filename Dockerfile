FROM python:3.8

RUN apt-get update &&\
    apt-get install liblapack-dev libblas-dev gfortran -y
RUN pip install poetry

WORKDIR /cs-insights-prediction-endpoint
COPY test.env /cs-insights-prediction-endpoint/.env
COPY . /cs-insights-prediction-endpoint

RUN poetry install --no-dev

FROM python:3.8

RUN apt-get update &&\
    apt-get install liblapack-dev libblas-dev gfortran -y
RUN pip install poetry

WORKDIR /cs-insights-prediction-endpoint
COPY test.env /cs-insights-prediction-endpoint/.env
COPY pyproject.toml /cs-insights-prediction-endpoint/pyproject.toml
COPY poetry.lock /cs-insights-prediction-endpoint/poetry.lock

RUN poetry install --no-dev

COPY . /cs-insights-prediction-endpoint

FROM python:3.8

WORKDIR /cs-insights-prediction-endpoint

RUN apt-get update &&\
    apt-get install liblapack-dev libblas-dev gfortran -y
RUN pip install poetry
RUN poetry config virtualenvs.path --unset
RUN poetry config virtualenvs.in-project true

COPY . /cs-insights-prediction-endpoint
COPY test.env /cs-insights-prediction-endpoint/.env

RUN poetry install --no-dev

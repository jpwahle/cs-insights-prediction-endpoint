FROM python:3.10

WORKDIR /cs-insights-prediction-endpoint

RUN apt-get update &&\
    apt-get install liblapack-dev libblas-dev gfortran python3-venv -y
RUN pip install poetry
RUN poetry config virtualenvs.in-project false

COPY . /cs-insights-prediction-endpoint

RUN poetry install --no-dev
RUN rm -rf .venv # Remove broken env that is created althouth `virtualenvs.in-project` is set to false
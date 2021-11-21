FROM python:3.7

WORKDIR /app
ADD pyproject.toml /app/pyproject.toml

RUN pip install poetry
RUN poetry install

COPY . /app
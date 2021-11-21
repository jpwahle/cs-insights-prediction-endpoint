FROM python:3.9

WORKDIR /app
ADD pyproject.toml /app/pyproject.toml

RUN pip install poetry
RUN poetry install

COPY . /app
FROM python:3.9

RUN apt-get update &&\
    apt-get install liblapack-dev libblas-dev gfortran -y

WORKDIR /app
ADD pyproject.toml /app/pyproject.toml

COPY . /app

RUN pip install poetry
RUN poetry install

COPY test.env /app/.env

ENTRYPOINT ["poetry", "run", "python", "prod.py", "--port", "8000"]

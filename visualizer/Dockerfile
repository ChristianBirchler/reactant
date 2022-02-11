FROM python:3.10-slim

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip
RUN apt update && apt install -y gcc
RUN pip install poetry

COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry install

COPY . .

EXPOSE 8050
EXPOSE 50000

ENV HOST=0.0.0.0

ENTRYPOINT ["poetry", "run", "python", "src/visualizer/main.py"]
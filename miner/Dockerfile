FROM python:3.10-slim

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip
RUN apt update && apt install -y gcc git
RUN pip install poetry

COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry install

COPY . .

ENV VISUALIZER=visualizer

CMD ["poetry", "run", "python", "src/miner/main.py"]
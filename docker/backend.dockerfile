FROM python:3.8-slim AS base

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY requirements /app/requirements

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements/backend.txt --no-deps --default-timeout=100

CMD ["python", "-m", "hack"]

FROM base AS dev

ENV BACKEND_CONFIG_PATH "config/dev.yaml"


FROM base AS real

COPY config /app/config
COPY build /app/build
COPY hack /app/hack


FROM real AS stg

ENV BACKEND_CONFIG_PATH "config/stg.yaml"


FROM real AS prd

ENV BACKEND_CONFIG_PATH "config/prd.yaml"
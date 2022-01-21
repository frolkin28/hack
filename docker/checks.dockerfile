FROM python:3.8-slim

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV MYPYPATH "${MYPYPATH}:/app"
ENV BACKEND_CONFIG_PATH "config/pytest.yaml"

COPY requirements /app/requirements

RUN pip3 install --upgrade pip && \
  pip3 install -r requirements/backend.txt --no-deps --no-cache-dir && \
  pip3 install -r requirements/checks.txt --no-deps --no-cache-dir
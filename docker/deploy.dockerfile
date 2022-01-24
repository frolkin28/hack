FROM node:13.8-slim AS frontend

WORKDIR /app

COPY package.json /app
COPY package-lock.json /app

RUN npm install --loglevel=error

COPY .babelrc /app
COPY webpack /app/webpack
COPY static /app/static

RUN npm run build-dev

FROM python:3.8-slim AS backend

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY requirements /app/requirements

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements/backend.txt --no-deps --default-timeout=100

ENV BACKEND_CONFIG_PATH "config/dev.yaml"

COPY config /app/config
COPY --from=frontend /app/build /app/build
COPY hack /app/hack


CMD ["python", "-m", "hack"]
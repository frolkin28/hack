FROM node:13.8-slim AS frontend

WORKDIR /app

COPY package.json /app
COPY package-lock.json /app

RUN npm install --loglevel=error

COPY . /app

RUN npm run build-dev

FROM python:3.8-slim AS backend

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY requirements /app/requirements

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements/backend.txt --no-deps --default-timeout=100

ENV BACKEND_CONFIG_PATH "config/dev.yaml"



RUN mkdir -p build

COPY --from=frontend /app/build /app/build/

COPY . /app

CMD ["python", "-m", "hack"]
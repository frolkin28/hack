FROM node:13.8-slim AS dev

WORKDIR /app

COPY package.json /app
COPY package-lock.json /app

RUN npm install --loglevel=error


FROM dev AS stg

COPY .babelrc /app
COPY tsconfig.frontend.json /app
COPY webpack /app/webpack
COPY static /app/static


FROM stg AS prd
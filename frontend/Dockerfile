FROM node:14-alpine

WORKDIR /src

COPY package.json package.json
COPY package-lock.json package-lock.json

RUN npm install

COPY . /src

RUN npm run build

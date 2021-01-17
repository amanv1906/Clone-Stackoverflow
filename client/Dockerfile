FROM node:12.18.3


WORKDIR /app

COPY ["package.json", "./"]

RUN npm install --silent

COPY . .

EXPOSE 3000

FROM node:12-alpine

WORKDIR /usr/src/frontend
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm" ,"run", "dev"]

FROM node:14-alpine

WORKDIR /usr/src/frontend
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build
CMD ["node", "build/index.js"]

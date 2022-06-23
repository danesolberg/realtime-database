FROM node:16-alpine

WORKDIR .

ENV PATH /node_modules/.bin:$PATH

COPY package.json ./
COPY yarn.lock ./
RUN yarn install

COPY . ./

CMD ["yarn", "dev"]
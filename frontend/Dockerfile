FROM node:18

RUN mkdir /frontend

COPY tsconfig.json /frontend/tsconfig.json

WORKDIR /frontend

RUN npm install -g typescript@5.8.3

RUN npm install d3@7.9.0 @types/d3@7.4.3

CMD ["npx", "tsc", "-w"]
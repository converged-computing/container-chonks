# Build step #1: build the React front end
FROM node:16-alpine as build-step
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json index.html style.css ./
COPY ./src ./src
COPY ./fonts ./fonts
COPY ./img ./img
RUN npm install --production=true
RUN npm run build


# Build step #2: build an nginx container
FROM nginx:stable-alpine
RUN mkdir /static
COPY --from=build-step /app/gims/static/* /static
RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./docker/40-copy-static-files.sh /docker-entrypoint.d/

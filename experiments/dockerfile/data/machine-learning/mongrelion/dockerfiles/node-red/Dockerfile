FROM docker.io/node:18-alpine

MAINTAINER Carlos León <mail@carlosleon.info>

ARG VERSION

RUN deluser --remove-home node

RUN npm install -g --unsafe-perm node-red@${VERSION}

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

EXPOSE 1880

VOLUME /data

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

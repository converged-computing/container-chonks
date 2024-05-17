FROM alpine:3.4
MAINTAINER Doug Stanley <doug@douglasstanley.com>

RUN apk add --update build-base git python3 python3-dev ;\
    /usr/bin/python3 -mensurepip ; \
    /usr/bin/pip3 install --upgrade pip ;\
    rm -rf /var/cache/apk/*

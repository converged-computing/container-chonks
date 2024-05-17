FROM ruby:2.4.2-alpine3.6

RUN apk add --no-cache curl \
    && gem install redis \
    && curl -sSL -o /usr/local/bin/redis-trib.rb http://download.redis.io/redis-stable/src/redis-trib.rb \
    && curl -sSL -o /usr/local/bin/rcm https://github.com/maiha/rcm.cr/releases/download/v0.7.6/rcm \
    && chmod +x /usr/local/bin/*

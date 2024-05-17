FROM fluent/fluentd:v0.14.8

USER root

RUN apk --no-cache --update add sudo build-base ruby-dev \
    && sudo -u fluent gem install fluent-plugin-elasticsearch fluent-plugin-record-reformer \
    && rm -rf /home/fluent/.gem/ruby/2.3.0/cache/*.gem \
    && sudo -u fluent gem sources -c \
    && apk del sudo build-base ruby-dev \
    && rm -rf /var/cache/apk/*

EXPOSE 24284

USER fluent

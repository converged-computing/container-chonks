FROM alpine:3.8
MAINTAINER Doug Stanley <doug@douglasstanley.com>

ADD run.sh /run.sh
RUN apk add --update postgresql postgresql-client ;\
    chmod a+rx /run.sh ;\
    rm -rf /var/cache/apk/*

ENTRYPOINT ["/run.sh"]
CMD [ "postgres" ]
VOLUME [ "/var/lib/postgresql", "/var/log/postgresql" ]
EXPOSE 5432

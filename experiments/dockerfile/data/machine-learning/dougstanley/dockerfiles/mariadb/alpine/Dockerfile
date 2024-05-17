FROM alpine:3.3
MAINTAINER Doug Stanley <doug@douglasstanley.com>

ADD run.sh /run.sh
RUN apk add --update mariadb mariadb-common mariadb-client ;\
    chmod a+rx /run.sh ;\
    rm -rf /var/cache/apk/*

ENTRYPOINT ["/run.sh"]
CMD [ "mysqld" ]
VOLUME [ "/var/lib/mysql", "/var/log/mysql" ]

FROM alpine:3.6

RUN apk add --no-cache keepalived

COPY keepalived.conf /etc/keepalived/keepalived.conf
COPY keepalived.sh /usr/bin/keepalived.sh

CMD ["keepalived.sh"]

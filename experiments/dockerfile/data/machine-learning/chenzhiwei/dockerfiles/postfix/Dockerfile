FROM docker.io/library/golang:latest AS builder
RUN git clone https://github.com/ochinchina/supervisord.git
RUN cd supervisord && go mod tidy && CGO_ENABLED=0 go build -o /tmp/supervisord && strip /tmp/supervisord

FROM docker.io/library/alpine:3.15

LABEL org.opencontainers.image.authors="zhiwei@youya.org"
LABEL org.opencontainers.image.documentation="https://github.com/chenzhiwei/dockerfiles"

RUN apk add --no-cache postfix opendkim opendkim-utils ca-certificates cyrus-sasl

COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY --from=builder /tmp/supervisord /usr/bin/supervisord

COPY postfix/* /etc/postfix/
COPY opendkim/* /etc/opendkim/
COPY sasl2/smtpd.conf /etc/sasl2/smtpd.conf
COPY mail-docker-config.sh /usr/libexec/mail-docker-config.sh

CMD ["supervisord"]

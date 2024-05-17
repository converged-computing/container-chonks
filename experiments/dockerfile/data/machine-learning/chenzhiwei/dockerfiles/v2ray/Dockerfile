FROM docker.io/library/alpine:latest AS builder

RUN apk add --no-cache ca-certificates curl
RUN curl -sLO https://github.com/v2fly/v2ray-core/releases/latest/download/v2ray-linux-64.zip
RUN unzip -o -d / v2ray-linux-64.zip

FROM docker.io/library/alpine:latest

LABEL org.opencontainers.image.authors="zhiwei@youya.org"
LABEL org.opencontainers.image.documentation="https://github.com/chenzhiwei/dockerfiles"

RUN apk add --no-cache ca-certificates curl

COPY --from=builder /v2ray /usr/bin/
COPY --from=builder /config.json /etc/v2ray/config.json

COPY v2ray.sh /v2ray.sh

CMD ["/v2ray.sh"]

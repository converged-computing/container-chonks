# podman build --platform linux/amd64,linux/arm64 --manifest docker.io/siji/privoxy:latest .

FROM docker.io/library/alpine:latest

LABEL org.opencontainers.image.authors="zhiwei@youya.org"
LABEL org.opencontainers.image.documentation="https://github.com/chenzhiwei/dockerfiles"

RUN apk add --no-cache privoxy
RUN echo 'listen-address 0.0.0.0:8118' > /etc/privoxy/config

CMD ["privoxy", "--no-daemon", "--user", "privoxy", "/etc/privoxy/config"]

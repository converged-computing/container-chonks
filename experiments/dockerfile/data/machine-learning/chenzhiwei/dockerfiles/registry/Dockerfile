FROM docker.io/library/registry:2

LABEL org.opencontainers.image.authors="zhiwei@youya.org"
LABEL org.opencontainers.image.documentation="https://github.com/chenzhiwei/dockerfiles"

COPY cr.crt cr.key /certs

ENV REGISTRY_HTTP_ADDR=0.0.0.0:443 \
    REGISTRY_HTTP_TLS_CERTIFICATE=/certs/cr.crt \
    REGISTRY_HTTP_TLS_KEY=/certs/cr.key \

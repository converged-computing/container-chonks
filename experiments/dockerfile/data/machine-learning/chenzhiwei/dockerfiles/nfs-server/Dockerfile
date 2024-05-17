FROM docker.io/library/ubuntu:latest

LABEL org.opencontainers.image.authors="zhiwei@youya.org"
LABEL org.opencontainers.image.documentation="https://github.com/chenzhiwei/dockerfiles/tree/master/nfs-server"

RUN apt update \
    && apt -y install nfs-kernel-server --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY exports /etc/exports
COPY nfs-server.sh /nfs-server.sh

VOLUME /var/nfs

CMD ["/nfs-server.sh"]

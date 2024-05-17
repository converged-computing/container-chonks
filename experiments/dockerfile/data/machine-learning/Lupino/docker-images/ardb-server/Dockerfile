FROM ubuntu:18.04
MAINTAINER Li Meng Jun "lmjubuntu@gmail.com"

# Build stage:

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y git make gcc g++ automake autoconf libbz2-dev libz-dev wget

RUN git clone https://github.com/yinqiwen/ardb.git && \
    make -C ardb && \
    sed -e 's@home.*@home /var/lib/ardb@' \
        -e 's/loglevel.*/loglevel info/' \
        -i ardb/ardb.conf && \
    echo 'trusted-ip *.*.*.*' >> ardb/ardb.conf

# Production stage:

FROM ubuntu:18.04

COPY --from=0 ardb/ardb.conf       /etc/
COPY --from=0 ardb/src/ardb-server /usr/bin

WORKDIR /var/lib/ardb

EXPOSE 16379
ENTRYPOINT ["/usr/bin/ardb-server", "/etc/ardb.conf"]

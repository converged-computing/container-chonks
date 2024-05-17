# NodeJS v0.10.29

# Version 0.1

FROM mongrelion/debian

MAINTAINER Carlos León, mongrelion@dev-co.org

RUN cd /tmp && \
    wget http://nodejs.org/dist/v0.10.29/node-v0.10.29-linux-x64.tar.gz && \
    tar xf node-v0.10.29-linux-x64.tar.gz && \
    mv node-v0.10.29-linux-x64 /opt/nodejs && \
    rm node-v0.10.29-linux-x64.tar.gz

ENTRYPOINT ["/opt/nodejs/bin/node"]

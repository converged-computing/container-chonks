FROM          node:8
MAINTAINER    Robert Krahn <robert.krahn@gmail.com>

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update; \
    apt-get upgrade -y; \
    apt-get -y install curl git bzip2 unzip zip \
                       lsof sysstat dnsutils \
                       sudo

# lively user, password: lively
# openssl passwd -1 lively
RUN /usr/sbin/useradd \
    --create-home --home-dir /home/lively \
     --shell /bin/bash \
     --groups sudo \
     --password "$1$AvxnsNsn$jUwLZCqF3uxnKgXLUqyX41" \
     lively

# git
ADD gitconfig /home/lively/.gitconfig

# nodejs tooling
RUN npm install -g \
  nodemon forever

# For the Lively spell checker:
RUN apt-get install -y aspell

# lively
ENV WORKSPACE_LK=/home/lively/LivelyKernel \
    HOME=/home/lively \
    livelyport=9001

USER lively

WORKDIR /home/lively/LivelyKernel

EXPOSE 9001-9004

CMD rm "*.pid" >/dev/null 2>&1; \
    sudo chown -R lively .; \
    test ! -d PartsBin && echo "downloading PartsBin" && \
      curl https://lively-web.org/nodejs/PartsBinCopy/ > PartsBin.zip && \
      unzip PartsBin.zip && rm PartsBin.zip; \
    test ! -d users && echo "downloading users dir" && \
      curl https://lively-web.org/nodejs/PartsBinCopy/users.zip > users.zip && \
      unzip users.zip && rm users.zip; \
    forever bin/lk-server.js \
      --port 9001 --host 0.0.0.0 --behind-proxy \
      --db-config '{"enableRewriting":false,"enableVersioning":false}'

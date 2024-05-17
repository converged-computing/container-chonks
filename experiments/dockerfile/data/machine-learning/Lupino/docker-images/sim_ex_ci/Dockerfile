FROM ubuntu:18.04

ENV NODE_VERSION 10.16.3
ENV ARCH x64

RUN apt update \
  && apt install -y python3.7-dev python3.7 curl python3.7-distutils build-essential git unzip unrar-free \
  && update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1 \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python3.7 get-pip.py --force-reinstall \
  && rm get-pip.py \
  && pip install cython pymysql pymysql-pooling requests aio_periodic \
  && curl -fsSLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-$ARCH.tar.xz" \
  && tar -xJf "node-v$NODE_VERSION-linux-$ARCH.tar.xz" -C /usr/local --strip-components=1 --no-same-owner \
  && rm "node-v$NODE_VERSION-linux-$ARCH.tar.xz" \
  && ln -s /usr/local/bin/node /usr/local/bin/nodejs

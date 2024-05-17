FROM ubuntu:14.04

# Replace the Ubuntu sources
RUN sed -i 's/archive.ubuntu.com/mirrors.163.com/g' /etc/apt/sources.list

# Install enssential packages
RUN apt-get update && apt-get -y install \
    autoconf \
    build-essential \
    git \
    libapr1-dev \
    libcurl4-nss-dev \
    libsasl2-dev \
    libsvn-dev \
    libtool \
    maven \
    openjdk-7-jdk \
    python-boto \
    python-dev

# Clone Mesos code
RUN git clone https://github.com/apache/mesos /mesos

# Build Mesos binary
RUN mkdir -p /mesos/build \
    && cd /mesos \
    && ./bootstrap \
    && cd /mesos/build \
    && ../configure --prefix=/usr/local/mesos \
    && make \
    && make install

# Build tar package
RUN cd /usr/local \
    && tar zcf mesos.tar.gz mesos

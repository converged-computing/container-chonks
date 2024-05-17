FROM centos:7.2.1511

MAINTAINER 10sr <8slashes+docker@gmail.com>

RUN yum install -y tar \
    bzip2-devel ncurses-devel sqlite-devel readline-devel tk-devel openssl-devel zlib-devel "@Development Tools"

RUN cd /tmp && \
    curl -sSL -O https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz && \
    tar -xf Python-2.7.13.tgz && \
    cd Python-2.7.13 && ./configure --prefix=/usr/local && make && make install && \
    cd /tmp && rm -fr Python-2.7.13 && rm -f Python-2.7.13.tgz

RUN /usr/local/bin/python2.7 -m ensurepip

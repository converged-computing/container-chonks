FROM ubuntu:16.04

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN apt-get update && \
    apt-get install -y locales && \
    locale-gen en_US.UTF-8 && \
    update-locale en_US.UTF-8

RUN apt-get install -y curl gawk wget jq && \
    apt-get install -y python python-yaml python-pip && \
    apt-get clean && \
    pip install awscli
#      easy_install --upgrade pip && \

# Include `https://github.com/krallin/tini`.
# Newer versions of Docker (v1.13+) include `tini` out of the box using the
# `--init` flag for `docker run` command
# (https://docs.docker.com/engine/reference/commandline/run/#options).
ARG TINI_VERSION=v0.18.0
RUN gpg --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 595E85A6B1B4779EA4DAAEC70B588DFF0527A9B7 && \
    curl -o /usr/bin/tini -sSL "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini" && \
    curl -o /usr/bin/tini.asc -sSL "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini.asc" && \
    gpg --verify /usr/bin/tini.asc && \
    rm /usr/bin/tini.asc && \
    chmod +x /usr/bin/tini

RUN gpg --keyserver pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 && \
    curl -o /usr/local/bin/gosu -sSL "https://github.com/tianon/gosu/releases/download/1.10/gosu-$(dpkg --print-architecture)" && \
    curl -o /usr/local/bin/gosu.asc -sSL "https://github.com/tianon/gosu/releases/download/1.10/gosu-$(dpkg --print-architecture).asc" && \
    gpg --verify /usr/local/bin/gosu.asc && \
    rm /usr/local/bin/gosu.asc && \
    chmod +sx /usr/local/bin/gosu

# Use tini by default
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/bin/bash"]

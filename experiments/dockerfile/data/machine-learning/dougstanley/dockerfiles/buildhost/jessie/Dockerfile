FROM debian:8
MAINTAINER Doug Stanley <doug@technologixllc.com>

ENV DEBIAN_FRONTEND noninteractive

RUN echo deb-src http://httpredir.debian.org/debian jessie main >> /etc/apt/sources.list ; \
    echo deb-src http://httpredir.debian.org/debian jessie-updates main >> /etc/apt/sources.list ; \
    echo deb-src http://security.debian.org jessie/updates main >> /etc/apt/sources.list ; \
    apt-get -y -q update; \
    apt-get -y -q dist-upgrade; \
    apt-get -y -q install --no-install-recommends \
		ca-certificates \
		curl \
		wget ;\
    apt-get -y -q install --no-install-recommends \
        git \
        mercurial \
        bzr \
        subversion \
        openssh-client ; \
    apt-get -y -q install --no-install-recommends \
        build-essential \
        debhelper \
        dpkg-dev \
        autoconf \
		automake \
		bzip2 \
		file \
		g++ \
		gcc \
        libbz2-dev \
		libc6-dev \
		libcurl4-openssl-dev \
		libevent-dev \
		libffi-dev \
		libglib2.0-dev \
        liblzma-dev \
        libncurses-dev \
        libreadline-dev \
		libsqlite3-dev \
		libssl-dev \
		libtool \
		libxml2-dev \
		libxslt-dev \
		libyaml-dev \
		make \
		patch \
		xz-utils \
		zlib1g-dev ;\
    apt-get clean; \
    apt-get autoclean; \
    rm -rf /var/lib/apt/lists/*; \
    rm -rf /tmp/*

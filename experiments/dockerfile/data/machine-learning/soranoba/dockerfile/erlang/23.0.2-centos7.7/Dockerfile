FROM centos:7.7.1908

LABEL maintainer="contact@soranoba.net"

ENV OTP_VERSION 23.0.2
ENV OPENSSL_VERSION 1.1.1g

RUN yum -y update \
  && yum clean all \
  && yum -y install \
         git \
         gcc \
         autoconf \
         glibc-devel \
	 openssl-devel \
         make \
         ncurses-devel \
         perl \
         tar \
  && yum clean all

RUN curl -sSL "https://www.openssl.org/source/openssl-${OPENSSL_VERSION}.tar.gz" \
    | tar -v -C /tmp -xz \
  && cd /tmp/openssl-${OPENSSL_VERSION} \
  && ./config --prefix=/opt/openssl-${OPENSSL_VERSION} \
  && make \
  && make install \
  && cd .. \
  && rm -rf /tmp/openssl-${OPENSSL_VERSION}

RUN cd /tmp \
  && git clone -b OTP-${OTP_VERSION} https://github.com/erlang/otp.git \
  && cd /tmp/otp \
  && ./otp_build autoconf \
  && ./configure --prefix=/usr/local \
                 --build="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
                 --enable-kernel-poll \
                 --enable-dirty-schedulers \
                 --enable-smp-support \
                 --enable-hipe \
                 --with-ssl=/opt/openssl-${OPENSSL_VERSION} \
                 --without-javac \
                 --without-odbc \
                 --disable-sctp \
                 --disable-dynamic-ssl-lib \
                 --disable-vm-probes \
  && make \
  && make install \
  && cd .. \
  && rm -rf otp

WORKDIR /

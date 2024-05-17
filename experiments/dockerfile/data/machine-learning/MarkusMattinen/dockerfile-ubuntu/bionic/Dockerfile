# Ubuntu Bionic base image with updates, fixes and useful packages installed.
FROM ubuntu:bionic

ENV HOME=/root \
    DEBIAN_FRONTEND=noninteractive \
    LOCALE=en_US.UTF-8 \
    TERM=xterm

RUN echo '#!/bin/sh' > /usr/sbin/policy-rc.d \
 && echo 'exit 101' >> /usr/sbin/policy-rc.d \
 && chmod +x /usr/sbin/policy-rc.d \
 && dpkg-divert --local --rename --add /sbin/initctl \
 && cp -a /usr/sbin/policy-rc.d /sbin/initctl \
 && sed -i 's/^exit.*/exit 0/' /sbin/initctl \
 && echo 'force-unsafe-io' > /etc/dpkg/dpkg.cfg.d/docker-apt-speedup \
 && echo 'DPkg::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' > /etc/apt/apt.conf.d/docker-clean \
 && echo 'APT::Update::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' >> /etc/apt/apt.conf.d/docker-clean \
 && echo 'Dir::Cache::pkgcache ""; Dir::Cache::srcpkgcache "";' >> /etc/apt/apt.conf.d/docker-clean \
 && echo 'Acquire::Languages "none";' > /etc/apt/apt.conf.d/docker-no-languages \
 && echo 'Acquire::GzipIndexes "true"; Acquire::CompressionTypes::Order:: "gz";' > /etc/apt/apt.conf.d/docker-gzip-indexes \
 && echo 'Apt::AutoRemove::SuggestsImportant "false";' > /etc/apt/apt.conf.d/docker-autoremove-suggests \
 && mkdir -p /run/systemd \
 && echo 'docker' > /run/systemd/container \
 && echo "deb mirror://mirrors.ubuntu.com/mirrors.txt bionic main restricted universe multiverse" > /etc/apt/sources.list \
 && echo "deb mirror://mirrors.ubuntu.com/mirrors.txt bionic-updates main restricted universe multiverse" >> /etc/apt/sources.list \
 && echo "deb mirror://mirrors.ubuntu.com/mirrors.txt bionic-security main restricted universe multiverse" >> /etc/apt/sources.list \
 && echo "deb-src mirror://mirrors.ubuntu.com/mirrors.txt bionic main restricted universe multiverse" >> /etc/apt/sources.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends apt-transport-https \
 && apt-get install -y --no-install-recommends apt-utils ca-certificates locales tzdata \
 && locale-gen ${LOCALE} \
 && export LANG=${LOCALE} LC_ALL=${LOCALE} \
 && apt-get install -y --no-install-recommends curl wget vim-tiny iproute2 \
 && apt-get dist-upgrade -y --no-install-recommends \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* $HOME/.cache \
 && echo "LANG=${LOCALE}" > /etc/default/locales \
 && echo "LC_COLLATE=${LOCALE}" >> /etc/default/locales \
 && echo "LC_CTYPE=${LOCALE}" >> /etc/default/locales \
 && echo "LC_MESSAGES=${LOCALE}" >> /etc/default/locales \
 && echo "LC_MONETARY=${LOCALE}" >> /etc/default/locales \
 && echo "LC_NUMERIC=${LOCALE}" >> /etc/default/locales \
 && echo "LC_PAPER=${LOCALE}" >> /etc/default/locales \
 && echo "LC_NAME=${LOCALE}" >> /etc/default/locales \
 && echo "LC_ADDRESS=${LOCALE}" >> /etc/default/locales \
 && echo "LC_TELEPHONE=${LOCALE}" >> /etc/default/locales \
 && echo "LC_MEASUREMENT=${LOCALE}" >> /etc/default/locales \
 && echo "LC_IDENTIFICATION=${LOCALE}" >> /etc/default/locales \
 && echo "LC_TIME=${LOCALE}" >> /etc/default/locales

ENV LANG=${LOCALE} \
    LC_ALL=${LOCALE}

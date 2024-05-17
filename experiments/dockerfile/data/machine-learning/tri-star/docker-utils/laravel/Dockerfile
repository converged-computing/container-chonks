FROM ubuntu:18.04

ARG UID=1000
ARG GID=1000

RUN apt-get update && \
    apt-get install -y tzdata locales && \
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    echo "ja_JP UTF-8" > /etc/locale.gen && \
    locale-gen && \
    apt-get clean

ENV LANG=ja_JP.utf8

RUN apt-get update && \
    apt-get install -y less vim curl git python \
            php php-fpm php-mbstring php-xml php-zip php-json php-mysql \
            php-xdebug \
            nginx && \
    apt-get clean

RUN curl -L https://bootstrap.pypa.io/ez_setup.py | python && \
    easy_install supervisor

RUN cd /usr/local && \
    curl -LO https://nodejs.org/dist/v8.11.3/node-v8.11.3-linux-x64.tar.xz && \
    tar -Jxf node-v8.11.3-linux-x64.tar.xz && \
    mv node-v8.11.3-linux-x64 node && \
    echo "export PATH=${PATH}:/usr/local/node/bin" > /etc/profile.d/node.sh && \
    rm node-v8.11.3-linux-x64.tar.xz

RUN mkdir -p /opt/demo && \
    groupadd -g $GID demo && \
    useradd -u $UID -g $GID --create-home --shell=/bin/bash demo

RUN su - demo -c "curl -o- -L https://yarnpkg.com/install.sh | bash"

RUN cd /usr/local/src && \
    curl -L https://getcomposer.org/installer | php && \
    chmod 755 composer.phar && \
    mv composer.phar /usr/local/bin/composer

RUN rm -f /etc/php/7.2/fpm/pool.d/* && \
    rm -f /etc/nginx/sites-enabled/*

COPY docker/nginx /etc/nginx
COPY docker/supervisord.conf /etc/supervisord.conf
COPY docker/supervisord.d /etc/supervisord.d
COPY docker/php-fpm /etc/php/7.2/fpm
COPY docker/entrypoint.sh /

VOLUME ["/opt/demo", "/data"]

WORKDIR /opt/project

ENTRYPOINT [ "bash", "/entrypoint.sh" ]

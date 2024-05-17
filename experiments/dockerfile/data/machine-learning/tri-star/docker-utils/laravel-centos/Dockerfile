FROM centos:7.5.1804

ARG UID=1000
ARG GID=1000
ARG HTTP_PROXY=""
ARG NO_PROXY=127.0.0.1

ENV LANG=ja_JP.UTF-8 \
    TERM=xterm \
    HTTP_PROXY=$HTTP_PROXY \
    HTTPS_PROXY=$HTTP_PROXY \
    http_proxy=$HTTP_PROXY \
    https_proxy=$HTTP_PROXY \
    no_proxy=$NO_PROXY

RUN yum reinstall -y glibc-common && \
    yum clean all

RUN rm -f /etc/localtime && \
    ln -fs /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN yum install -y epel-release && \
    curl -LO http://rpms.famillecollet.com/enterprise/remi-release-7.rpm && \
    rpm -ivh remi-release-7.rpm && \
    yum install -y --enablerepo=remi,remi-php72 less vim curl git python \
            php php-fpm php-mbstring php-xml php-pecl-yaml php-json php-zip php-mysql php-pdo-sqlite \
            php-xdebug php-opcache php-process \
            nginx && \
    yum clean all

RUN curl -L https://bootstrap.pypa.io/ez_setup.py | python && \
    easy_install supervisor

RUN cd /usr/local && \
    curl -LO https://nodejs.org/dist/v8.11.3/node-v8.11.3-linux-x64.tar.xz && \
    tar -Jxf node-v8.11.3-linux-x64.tar.xz && \
    mv node-v8.11.3-linux-x64 node && \
    echo "export PATH=${PATH}:/usr/local/node/bin" > /etc/profile.d/node.sh && \
    rm node-v8.11.3-linux-x64.tar.xz

RUN mkdir -p /opt/project && \
    groupadd -g $GID develop && \
    useradd -u $UID -g $GID --create-home --shell=/bin/bash develop && \
    chown develop:develop /opt/project
    
RUN su - develop -c "curl -o- -L https://yarnpkg.com/install.sh | bash"

RUN echo 'export PATH="$HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH"' > /etc/profile.d/yarn.sh

RUN cd /usr/local/src && \
    curl -L https://getcomposer.org/installer | php && \
    chmod 755 composer.phar && \
    mv composer.phar /usr/local/bin/composer

RUN rm -f /etc/php-fpm.conf && \
    rm -rf /etc/php-fpm.d && \
    rm -f /etc/nginx/sites-enabled/*

COPY docker/nginx /etc/nginx
COPY docker/supervisord.conf /etc/supervisord.conf
COPY docker/supervisord.d /etc/supervisord.d
COPY docker/php-fpm /etc/php-fpm
COPY docker/entrypoint.sh /

VOLUME ["/data"]

WORKDIR /opt/project

ENTRYPOINT [ "bash", "/entrypoint.sh" ]

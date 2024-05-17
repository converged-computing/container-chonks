FROM debian:wheezy
MAINTAINER hello@andreimanea.com

RUN apt-get update && apt-get install -y curl \ 
    && echo "deb http://packages.dotdeb.org wheezy all" >> /etc/apt/sources.list \
    && echo "deb-src http://packages.dotdeb.org wheezy all" >> /etc/apt/sources.list \
    && curl http://www.dotdeb.org/dotdeb.gpg | apt-key add -

RUN apt-get update && apt-get install -y \
			php5-fpm \
                        php5-exactimage \
			php5-ffmpeg \
			php5-gdcm \
			php5-vtkgdcm \
			php5-mapscript \
			php5-ming \
			php5-adodb \
			php5-geoip \
			php5-imagick \
			php5-memcache \
			php5-memcached \
			php5-ps \
			php5-rrd \
			php5-sasl \
			php5-cli \
			php5-common \
			php5-curl \
			php5-dbg \
			php5-dev \
			php5-enchant \
			php5-fpm \
			php5-gd \
			php5-gmp \
			php5-imap \
			php5-interbase \
			php5-intl \
			php5-mcrypt \
			php5-mysqlnd \
			php5-odbc \
			php5-pgsql \
			php5-pspell \
			php5-recode \
			php5-sqlite \
			php5-tidy \
			php5-xmlrpc \
			php5-xsl \
			php5-librdf \
			php5-remctl \
			php5-xcache \
			php5-mongo \
			&& sed 's/;daemonize = yes/daemonize = no/' -i /etc/php5/fpm/php-fpm.conf

VOLUME /etc/php5

WORKDIR /root

ADD docker-entrypoint.sh /entrypoint.sh
RUN chmod u+x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 9000

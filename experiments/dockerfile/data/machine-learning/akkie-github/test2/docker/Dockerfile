FROM php:7.3-fpm
RUN apt-get update && apt-get install -y --no-install-recommends libicu-dev libzip-dev git unzip zlib1g-dev
WORKDIR /usr/src/php/ext
RUN docker-php-ext-install pdo_mysql mysqli mbstring zip opcache
RUN pecl install apcu-5.1.17 \
    && pecl install msgpack-2.0.3 \
    && pecl install redis-5.0.2 \
    && docker-php-ext-enable apcu msgpack redis
WORKDIR /var/www

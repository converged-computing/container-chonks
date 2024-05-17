FROM alpine:3.6

RUN apk add --no-cache php7 php7-fpm php7-mcrypt php7-mbstring php7-gd php7-xml php7-mysqli php7-pdo php7-pdo_mysql php7-json php7-curl php7-tokenizer \
    && echo '[global]' > /etc/php7/php-fpm.d/zz-docker.conf \
    && echo 'daemonize = no' >> /etc/php7/php-fpm.d/zz-docker.conf \
    && echo 'error_log = /proc/self/fd/2' >> /etc/php7/php-fpm.d/zz-docker.conf \
    && echo '[www]' >> /etc/php7/php-fpm.d/zz-docker.conf \
    && echo 'access.log = /proc/self/fd/2' >> /etc/php7/php-fpm.d/zz-docker.conf \
    && echo 'listen = [::]:9000' >> /etc/php7/php-fpm.d/zz-docker.conf

CMD ["php-fpm7"]

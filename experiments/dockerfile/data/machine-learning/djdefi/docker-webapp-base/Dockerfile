#
# Howto build: docker build -t djdefi/docker-webapp-base .
# VERSION 0.0.1

FROM ubuntu:precise
MAINTAINER DJ DeFi <djdefi@gmail.com>

# Set the env variable DEBIAN_FRONTEND to noninteractive
ENV DEBIAN_FRONTEND noninteractive

# Install apache php
RUN apt-get update
RUN apt-get install -y git apache2 libapache2-mod-php5 php5-mysql vim php5-ldap

# enable .htaccess
ADD apache_default /etc/apache2/conf.d/000-default.conf

# Enable mod_rewrite
RUN a2enmod rewrite

# Enable mod_ldap
RUN a2enmod ldap

# Fix Environment variables
RUN sed -i 's/variables_order = "GPCS"/variables_order = "EGPCS"/g' /etc/php5/apache2/php.ini 

# apache env vars
ENV APACHE_LOCK_DIR /var/lock
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2/
ENV APACHE_PID_FILE /var/apache.pid

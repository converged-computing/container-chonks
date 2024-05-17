FROM ubuntu:14.04
MAINTAINER kkeo

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install supervisor git subversion apache2 libapache2-mod-php5 php5-sqlite

EXPOSE 80

#RUN echo "source /etc/apache2/envvars" >> ~/.bashrc
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

CMD /bin/sh -c ". /etc/apache2/envvars && /usr/sbin/apache2 -D FOREGROUND"

# DOCKER-VERSION 0.8.1

FROM    ubuntu:12.04
RUN     echo "deb http://archive.ubuntu.com/ubuntu quantal main universe" >> /etc/apt/sources.list
RUN     apt-get -y update

RUN     apt-get -y install wget git python supervisor
RUN     wget -O /tmp/node-v0.11.0.tar.gz http://nodejs.org/dist/v0.11.0/node-v0.11.0-linux-x64.tar.gz
RUN     tar -C /usr/local/ --strip-components=1 -zxvf /tmp/node-v0.11.0.tar.gz
RUN     rm /tmp/node-v0.11.0.tar.gz
RUN     git clone git://github.com/etsy/statsd.git statsd
RUN     mkdir -p /var/log/supervisor

ADD     ./config.js ./statsd/config.js
ADD     ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE  8125/udp
EXPOSE  8126/tcp

CMD ["/usr/bin/supervisord"]

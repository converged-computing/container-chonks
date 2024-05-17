FROM ubuntu:latest
# BUILD:
# docker build . -t thesheff17/apt-cacher-ng

# RUN: 
# mkdir /tmp/cache
# docker run -d -p 3142:3142 -v /tmp/cache:/var/cache/apt-cacher-ng thesheff17/apt-cacher-ng

# USE:
# docker run -t -t --rm -e http_proxy http://dockerhost:3142 debian bash
# RUN  echo 'Acquire::http { Proxy "http://172.17.0.2:3142"; };' >> /etc/apt/apt.conf.d/01proxy
# RUN rm /etc/apt/apt.conf.d/01proxy

# MAINTAINER Dan@Sheffner.com

VOLUME	["/var/cache/apt-cacher-ng"]

RUN \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-cacher-ng && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /root/
EXPOSE 	3142
CMD chmod 777 /var/cache/apt-cacher-ng && service apt-cacher-ng start && tail -f /var/log/apt-cacher-ng/*

FROM gliderlabs/alpine

MAINTAINER Carlos León <mail@carlosleon.info>

RUN apk-install tinyproxy && \
    sed -i -E "s/^#Syslog On/Syslog on/" /etc/tinyproxy/tinyproxy.conf

EXPOSE 8888

ENTRYPOINT ["/usr/sbin/tinyproxy"]

CMD ["-d"]

# supervisord on Ubuntu Bionic
FROM markusma/ubuntu:bionic

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-pkg-resources  python3-pip python3-setuptools git \
 && git clone https://github.com/MarkusMattinen/supervisor.git -b prepend-timestamp /tmp/supervisor \
 && cd /tmp/supervisor \
 && pip3 install . \
 && ln -sf /usr/local/bin/supervisord /usr/bin/supervisord \
 && ln -sf /usr/local/bin/pidproxy /usr/bin/pidproxy \
 && cd / \
 && rm -rf /tmp/supervisor \
 && apt-get purge -y --autoremove -o APT::AutoRemove::RecommendsImportant=false python3-pip python3-setuptools git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* $HOME/.cache \
 && mkdir -p /var/log/supervisor

ADD config/etc/supervisor/supervisord.conf /etc/supervisor/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]

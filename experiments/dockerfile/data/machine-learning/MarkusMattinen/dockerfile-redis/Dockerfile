# Redis on Ubuntu Bionic

FROM markusma/ubuntu:bionic

RUN add-apt-repository ppa:chris-lea/redis-server \
 && apt-get update \
 && apt-get install -y --no-install-recommends redis-server \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* $HOME/.cache

RUN curl -L https://github.com/tianon/gosu/releases/download/1.10/gosu-amd64 -o /usr/local/bin/gosu \
 && chmod +x /usr/local/bin/gosu

COPY etc/ /etc/
COPY bin/ /usr/local/bin/

EXPOSE 6379
VOLUME ["/var/lib/redis"]
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["redis-server", "/etc/redis/redis.conf"]

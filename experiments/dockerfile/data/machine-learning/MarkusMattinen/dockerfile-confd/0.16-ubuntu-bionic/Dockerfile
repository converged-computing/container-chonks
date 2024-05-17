# confd and supervisord on Ubuntu Bionic
FROM markusma/supervisord:ubuntu-bionic

RUN apt-get update \
 && apt-get install -y --no-install-recommends golang make \
 && export GOPATH=/go \
 && git clone https://github.com/kelseyhightower/confd -b v0.16.0 $GOPATH/src/github.com/kelseyhightower/confd \
 && cd $GOPATH/src/github.com/kelseyhightower/confd \
 && make \
 && mv bin/confd /usr/local/bin/confd \
 && chmod +x /usr/local/bin/confd \
 && cd / \
 && rm -r $GOPATH \
 && apt-get purge -y --autoremove -o APT::AutoRemove::RecommendsImportant=false golang make \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* $HOME/.cache

ADD config/etc/confd /etc/confd
ADD config/init /init

CMD ["/init"]

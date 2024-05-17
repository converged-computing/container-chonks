FROM ubuntu:18.04
MAINTAINER Doug Stanley <doug@douglasstanley.com>

ENV DEBIAN_FRONTEND noninteractive

ARG UID=1000
ARG GID=1000

RUN apt-get -y -q update \
    && apt-get install -y -q --no-install-recommends dumb-init apt-cacher-ng \
    && sed -i -e \
    '/^# Default:$/{N;/\n# PassThroug.*$/{s//&\nPassThroughPattern: \^\.\*:443\$/;P;D}}' \
      /etc/apt-cacher-ng/acng.conf \
    && chgrp -R $GID /etc/apt-cacher-ng/* \
    && chown -R $UID:$GID /var/cache/apt-cacher-ng \
    && chown -R $UID:$GID /var/log/apt-cacher-ng \
    && apt-get clean && apt-get autoclean

VOLUME ["/var/cache/apt-cacher-ng"]
EXPOSE 3142
USER $UID:$GID
CMD /usr/bin/dumb-init -- /bin/sh -c '/usr/sbin/apt-cacher-ng -c /etc/apt-cacher-ng/ foreground=1'

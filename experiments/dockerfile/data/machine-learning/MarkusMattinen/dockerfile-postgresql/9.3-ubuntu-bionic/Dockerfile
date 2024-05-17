# PostgreSQL 9.3 with PostGIS 2.4 on Ubuntu Bionic
#
# Included plugins:
# pgextwlist
FROM markusma/ubuntu:bionic

RUN apt-get update \
 && apt-get install -y --no-install-recommends software-properties-common gnupg \
 &&  echo 'deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main' > /etc/apt/sources.list.d/pgdg.list \
 && apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 7FCC7D46ACCC4CF8 \
 && apt-get update \
 && apt-get install -y --no-install-recommends postgresql-9.3 postgresql-contrib-9.3 postgresql-server-dev-9.3 postgresql-9.3-postgis-2.4 git build-essential language-pack-fi \
 && dpkg-reconfigure locales \
 && cd /tmp \
 && git clone https://github.com/dimitri/pgextwlist.git \
 && cd pgextwlist \
 && make \
 && make install \
 && mkdir -p /usr/lib/postgresql/9.3/lib/plugins \
 && cp pgextwlist.so /usr/lib/postgresql/9.3/lib/plugins \
 && cd / \
 && rm -rf /tmp/pgextwlist \
 && apt-get purge -y postgresql-server-dev-9.3 software-properties-common gnupg git build-essential \
 && apt-get autoremove -y \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* $HOME/.cache

RUN curl -L https://github.com/tianon/gosu/releases/download/1.10/gosu-amd64 -o /usr/local/bin/gosu \
 && chmod +x /usr/local/bin/gosu

COPY etc/ /etc/
COPY bin/ /usr/local/bin/

EXPOSE 5432
VOLUME ["/var/lib/postgresql/9.3/main"]
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/usr/lib/postgresql/9.3/bin/postgres", "-D", "/var/lib/postgresql/9.3/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]

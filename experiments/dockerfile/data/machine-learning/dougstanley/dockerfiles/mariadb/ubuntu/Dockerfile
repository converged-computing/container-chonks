FROM ubuntu:14.04
MAINTAINER Doug Stanley <doug@douglasstanley.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-mark hold initscripts udev plymouth mountall upstart; \
    apt-get -y -q update; \
    apt-get -y -q dist-upgrade; \
    { echo "mariadb-server-5.5	mysql-server/root_password	password	''"; \
      echo "mariadb-server-5.5	mysql-server/root_password_again	password	''"; \
      echo "mariadb-server-5.5	mariadb-server/oneway_migration	boolean	true"; \	
      echo "mariadb-server-5.5	mariadb-server-5.5/really_downgrade	boolean	false"; \
      echo "mariadb-server-5.5	mysql-server-5.5/postrm_remove_databases	boolean	false"; \
    } | debconf-set-selections; \
    apt-get install -y -q mariadb-server mariadb-client; \
    apt-get clean; \
    apt-get autoclean; \
    rm -rf /var/lib/apt/lists/*; \
    rm -rf /tmp/*

RUN locale-gen en_US en_US.UTF-8; \
    dpkg-reconfigure locales; \
    sed -i -e"s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/my.cnf ; \
    rm -rf /var/lib/mysql && mkdir -p /var/lib/mysql && rm -rf /var/log/mysql/*

ADD ./run.sh /run.sh
RUN chmod a+rx /run.sh

VOLUME [ "/var/lib/mysql", "/var/log/mysql" ]

#where command or entrypoint is run
ENTRYPOINT ["/run.sh"]
EXPOSE 3306
CMD ["mysqld"]

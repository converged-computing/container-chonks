FROM centos:6.6

MAINTAINER erickbrower

RUN sed -i.bak '/^\[base\]/a exclude=postgresql\*' /etc/yum.repos.d/CentOS-Base.repo
RUN sed -i.bak '/^\[updates\]/a exclude=postgresql\*' /etc/yum.repos.d/CentOS-Base.repo 
RUN rpm -Uvh http://yum.postgresql.org/9.2/redhat/rhel-6-x86_64/pgdg-centos92-9.2-7.noarch.rpm
RUN yum install -y postgresql92 postgresql92-server postgresql92-contrib
RUN su - postgres -c /usr/pgsql-9.2/bin/initdb
RUN rpm -Uvh http://elgis.argeo.org/repos/6/elgis-release-6-6_0.noarch.rpm
RUN rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
RUN yum install -y libspatialite.x86_64 postgis2_92
RUN sed -i.bak -e '53d' /etc/init.d/postgresql-9.2
RUN echo "host    all             all             0.0.0.0/0               md5" >> /var/lib/pgsql/9.2/data/pg_hba.conf
RUN echo "host    all             docker          0.0.0.0/0               trust" >> /var/lib/pgsql/9.2/data/pg_hba.conf
RUN echo "listen_addresses = '*'" >> /var/lib/pgsql/9.2/data/postgresql.conf
RUN echo "port = 5432" >> /var/lib/pgsql/9.2/data/postgresql.conf
RUN touch /etc/sysconfig/network
RUN service postgresql-9.2 start && runuser -l postgres -c 'createuser -d -s -r -l docker' && runuser -l postgres -c "psql postgres -c \"ALTER USER docker WITH ENCRYPTED PASSWORD 'docker'\"" && service postgresql-9.2 stop
RUN echo 'HOSTNAME=database' >> /etc/sysconfig/network

EXPOSE 5432

CMD ["/bin/su", "postgres", "-c", "/usr/pgsql-9.2/bin/postgres -D /var/lib/pgsql/9.2/data -c config_file=/var/lib/pgsql/9.2/data/postgresql.conf"]

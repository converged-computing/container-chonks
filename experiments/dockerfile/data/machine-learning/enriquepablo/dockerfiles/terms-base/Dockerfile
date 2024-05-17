FROM enriquepablo/python3:0.1

MAINTAINER Enrique Perez Arnaud <enrique@cazalla.net>

RUN apt-get update && apt-get install -y \
  sed \
  git \
  postgresql \
  postgresql-client \
  postgresql-server-dev-9.1

RUN sed 's/^\(\(local\|host\).*\)\(md5\|peer\)$/\1trust/' </etc/postgresql/9.1/main/pg_hba.conf >pg_hba.conf.new \
  && mv -f pg_hba.conf.new /etc/postgresql/9.1/main/pg_hba.conf

RUN service postgresql start \
  && update-rc.d postgresql enable \
  && su postgres -c "createuser -s terms" \
  && su postgres -c "createdb --owner=terms terms"

RUN cd /root \
  && git clone https://github.com/enriquepablo/terms-project.git \
  && cd terms-project \
  && sed -e 's/test_terms$/terms/' -e 's/normal$/real/' <config.cfg.in >config.cfg \
  && python3 bootstrap.py \
  && service postgresql start \
  && bin/buildout \
  && ln -s /root/terms-project/bin/terms /usr/bin \
  && ln -s /root/terms-project/bin/kbdaemon /usr/bin

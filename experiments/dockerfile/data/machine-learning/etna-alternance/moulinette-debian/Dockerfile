FROM debian:latest

ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV TZ Europe/Paris

# Common
RUN apt-get -qq update \
	&& apt-get install -y --no-install-recommends -y locales \
	&& sed -i '$ a\en_US.UTF-8 UTF-8' /etc/locale.gen \
	&& sed -i '$ a\fr_FR.UTF-8 UTF-8' /etc/locale.gen \
	&& locale-gen en_US.UTF-8 fr_FR.UTF-8 \
	&& apt-get install -y --no-install-recommends wget curl build-essential php ruby ssh host tree bc git

# Java
RUN apt-get install -y default-jre default-jdk

# mysql
RUN apt-get install -y mysql-server

# Python
RUN sed -i -e "\$adeb http://http.us.debian.org/debian testing main non-free contrib" /etc/apt/sources.list && \
    sed -i -e "\$adeb-src http://http.us.debian.org/debian testing main non-free contrib" /etc/apt/sources.list
RUN apt-get -qq update && apt install -y python3 python3-pip sqlite3 && ln -s /usr/bin/python3 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip

RUN pip install pycodestyle flask flask-sqlalchemy paramiko pyyaml pytest
# Pour les moulinette de web
RUN pip3 install bs4 cssutils validators

# Cleanup
RUN rm -rf /var/lib/apt/lists/*

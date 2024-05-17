FROM debian:wheezy
MAINTAINER Allard Hoeve <allard@byte.nl>

ADD etc/apt/apt.conf.d/99assumeyes /etc/apt/apt.conf.d/99assumeyes
ADD etc/apt/sources.list /etc/apt/sources.list
ADD etc/apt/preferences /etc/apt/preferences
ADD http://debian.byte.nl/repository/dists/Release.key /tmp/debian-release.key
RUN apt-key add /tmp/debian-release.key

RUN apt-get update
RUN apt-get install aptitude
RUN aptitude -y install vim-nox git ack-grep procps net-tools curl devscripts && apt-get clean


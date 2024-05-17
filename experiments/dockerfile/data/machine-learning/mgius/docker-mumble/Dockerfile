FROM ubuntu
MAINTAINER docker-mumble@markgius.com

ADD mumbleapt.key /
ADD mumble-release-precise.list /etc/apt/sources.list.d/
ADD ubuntu-universe.list /etc/apt/sources.list.d/
RUN cat mumbleapt.key | apt-key add -
RUN apt-get update
RUN apt-get install mumble-server -y
ADD mumble-server.ini /etc/mumble-server.ini

EXPOSE 64738

CMD ["/usr/sbin/murmurd", "-fg"]

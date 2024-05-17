FROM ubuntu:14.04
MAINTAINER kkeo

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install supervisor git subversion apache2 libapache2-mod-php5 php5-sqlite

RUN apt-get install -y openssh-server 

RUN mkdir -p /var/run/sshd
RUN mkdir -p /var/log/supervisor

RUN echo 'root:letmein' | chpasswd

ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN sed -ri 's/^UsePAM yes/#UsePAM yes/' /etc/ssh/sshd_config
RUN sed -ri 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/^RhostsRSAAuthentication no/#RhostsRSAAuthentication yes' /etc/ssh/sshd_config

EXPOSE 22 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]


FROM ubuntu:12.04

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get -y install mysql-server

EXPOSE 3306

CMD ["/usr/bin/mysqld_safe"]

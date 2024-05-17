# ubuntu-jp
#
# $ docker build -t soranoba/ubuntu-ja:14.04

FROM ubuntu:14.04
MAINTAINER Hinagiku Soranoba <soranoba@gmail.com>

# ja
RUN unlink /etc/localtime
RUN ln -s /usr/share/zoneinfo/Japan /etc/localtime
RUN echo "export LANG=ja_JP.UTF-8" >> /.bashrc
RUN locale-gen ja_JP.UTF-8

FROM debian:latest
MAINTAINER Javier Domingo Cansino <javierdo1@gmail.com>

# Install oracle's java (been told to have better performance)
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886
RUN echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu/ precise main" > /etc/apt/sources.list.d/java.list
RUN apt-get update
RUN apt-get dist-upgrade -y
RUN echo "debconf shared/accepted-oracle-license-v1-1 select true" | debconf-set-selections
RUN echo "debconf shared/accepted-oracle-license-v1-1 seen true" | debconf-set-selections
RUN apt-get install -y oracle-java8-installer ca-certificates wget

VOLUME ['/java-runner']
WORKDIR /java-runner

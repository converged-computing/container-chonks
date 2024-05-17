FROM centos:7

MAINTAINER Michael Bornholdt Nielsen, jarry.dk

RUN yum update -y \
  && mkdir /usr/lib/jvm/ \
  && yum -y install unzip \
  && curl -o openjdk-11.0.2_linux-x64_bin.tar.gz https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz \
  && tar xvf openjdk-11.0.2_linux-x64_bin.tar.gz -C /usr/lib/jvm/ \
  && yum clean all \
  && rm openjdk-11.0.2_linux-x64_bin.tar.gz \
  && rm -rf /var/cache/yum

ENV JAVA_HOME /usr/lib/jvm/jdk-11.0.2

ENV PATH "$PATH":/${JAVA_HOME}/bin:.:

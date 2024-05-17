FROM centos:7

MAINTAINER Michael Bornholdt Nielsen, jarry.dk

RUN yum update -y \
  && mkdir /usr/lib/jvm/ \
  && yum -y install unzip \
  && curl -o openjdk-12_linux-x64_bin.tar.gz https://download.java.net/java/GA/jdk12/33/GPL/openjdk-12_linux-x64_bin.tar.gz \
  && tar xvf openjdk-12_linux-x64_bin.tar.gz -C /usr/lib/jvm/ \
  && yum clean all \
  && rm openjdk-12_linux-x64_bin.tar.gz \
  && rm -rf /var/cache/yum

ENV JAVA_HOME /usr/lib/jvm/jdk-12

ENV PATH "$PATH":/${JAVA_HOME}/bin:.:

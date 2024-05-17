FROM centos:7

MAINTAINER Michael Bornholdt Nielsen, jarry.dk

RUN yum update -y \
  && yum -y install unzip \
  && yum -y install java-1.8.0-openjdk-devel \
  && yum clean all \
  && rm -rf /var/cache/yum

ENV JAVA_HOME /usr/lib/jvm/java-1.8.0

ENV PATH "$PATH":/${JAVA_HOME}/bin:.:

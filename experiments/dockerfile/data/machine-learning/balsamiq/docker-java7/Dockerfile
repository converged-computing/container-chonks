FROM stackbrew/ubuntu:saucy
MAINTAINER Luis Arias <luis@balsamiq.com>

RUN apt-get update && apt-get -y upgrade

# Add oracle java 7 ppa @ webupd8
RUN apt-get -y install software-properties-common
RUN add-apt-repository ppa:webupd8team/java
RUN apt-get -y update

# Tell the oracle-java7-installer that we have already accepted the oracle java license
RUN echo "oracle-java7-installer shared/accepted-oracle-license-v1-1 boolean true" | debconf-set-selections

# Install oracle java 7
RUN apt-get -y install oracle-java7-installer

# Fix java-7-oracle cacerts
RUN apt-get -y install ca-certificates-java
RUN rm /usr/lib/jvm/java-7-oracle/jre/lib/security/cacerts ; ln -s /etc/ssl/certs/java/cacerts /usr/lib/jvm/java-7-oracle/jre/lib/security/cacerts

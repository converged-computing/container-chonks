# Dockerizing Mule EE
# Version: 0.1
# Based on: openjdk
FROM openjdk:8
MAINTAINER Pablo Sagarna <pablo.sagarna@mulesoft.com>
# MuleEE installation:
ENV MULE_FILE_NAME=mule-enterprise-standalone-4.2.1
ENV MULE_VERSION=4.2.1
COPY ./$MULE_FILE_NAME.zip /opt/
WORKDIR /opt
RUN unzip /opt/$MULE_FILE_NAME.zip
RUN rm -f /opt/$MULE_FILE_NAME.zip
RUN mv $MULE_FILE_NAME mule
WORKDIR /opt/mule
# Configure external access:
# HTTPS Port for Anypoint Platform communication
EXPOSE  443
# Mule remote debugger
EXPOSE  5000
# Mule JMX port (must match Mule config file)
EXPOSE  1098
# Mule Cluster ports
EXPOSE 5701
EXPOSE 54327
# HTTP Service Port
EXPOSE 8081
# HTTP Service Port
EXPOSE 8082
# HTTP Service Port
EXPOSE 8083
# HTTP Service Port
EXPOSE 8084
# HTTP Service Port
EXPOSE 8085
# HTTP Service Port
EXPOSE 8086
# HTTPS Service Port
EXPOSE 8091
CMD ["/opt/mule/bin/mule", "-M-Dmule.agent.enabled=false"]
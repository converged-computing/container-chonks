FROM jbking/ubuntu-dev:20191019-1420

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
 openjdk-8-jdk maven gradle\
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java

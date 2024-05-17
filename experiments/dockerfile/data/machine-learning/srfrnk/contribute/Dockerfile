# Dockerfile for interactive access to other servers. May be used from within a K8S cluster.
FROM ubuntu

# Use bash shell
SHELL ["bash","-c"]
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Allow comfortable access via ssh terminal
ENV COLUMNS=200
ENV DEBIAN_FRONTEND=noninteractive

# Install some nice apt packages (incl. python, Java 8 etc...)
RUN apt-get update &&\
    apt-get install -yy apt-utils &&\
    apt-get upgrade -yy &&\
    apt-get install -yy \
        software-properties-common \
        python-pip bash-completion curl git nano wget make net-tools netcat dnsutils \
        openjdk-8-jdk-headless maven build-essential librdkafka-dev libyajl-dev kafkacat tmux unzip

# Enable bash completion
RUN echo ". /usr/share/bash-completion/bash_completion" >> ~/.bashrc

# Install Cassandra (for cmd-line utils)
RUN echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | tee -a /etc/apt/sources.list.d/cassandra.sources.list &&\
    curl https://www.apache.org/dist/cassandra/KEYS | apt-key add - && \
    apt-get update && \
    apt-get install -yy cassandra && \
    update-rc.d cassandra disable

# Install Kafka (for cmd-line utils)
RUN cd /opt && curl http://apache.mivzakim.net/kafka/2.0.0/kafka_2.11-2.0.0.tgz | tar -xz

# Install NVM and NodeJS v10
ENV NVM_VERSION v0.33.11
ENV NODE_VERSION v10
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/${NVM_VERSION}/install.sh | bash
RUN source ~/.nvm/nvm.sh; \
    nvm install $NODE_VERSION; \
    nvm use --delete-prefix $NODE_VERSION;

# Install gradle
RUN cd /opt; \
    curl -L https://services.gradle.org/distributions/gradle-4.10.3-bin.zip -o gradle-4.10.3-bin.zip; \
    unzip gradle-4.10.3-bin.zip; \
    mv gradle-4.10.3 gradle; \
    rm gradle-4.10.3-bin.zip; \
    mkdir -p /usr/share/bash_completion.d; \
    curl -LA gradle-completion https://edub.me/gradle-completion-bash -o /usr/share/bash_completion.d/gradle-completion.bash; \
    echo '. /usr/share/bash_completion.d/gradle-completion.bash' >> ~/.bashrc

# Install GCP sdk (gcloud etc..)
RUN curl -sSL https://sdk.cloud.google.com | bash

# Install Flink (for cmd-line utils)
RUN cd /tmp &&\
    curl -O http://apache.spd.co.il/flink/flink-1.7.1/flink-1.7.1-bin-scala_2.11.tgz &&\
    tar xzf flink-1.7.1-bin-scala_2.11.tgz &&\
    mv flink-1.7.1 /opt/flink &&\
    rm flink-1.7.1-bin-scala_2.11.tgz

# Update GCP sdk to latest
RUN export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update -y && apt-get install google-cloud-sdk -y

# Install latest `kubectl` (K8S)
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && \
    mv ./kubectl /usr/lib/google-cloud-sdk/bin && \
    chmod +x /usr/lib/google-cloud-sdk/bin/kubectl && \
    ln -s /usr/lib/google-cloud-sdk/bin/kubectl /usr/bin/kubectl

# Use Java 8 by default
RUN update-java-alternatives --set java-1.8.0-openjdk-amd64

ENV PATH=$PATH:/opt/gradle/bin:/opt/flink/bin:/root/google-cloud-sdk/bin

CMD ["tail","-f","/dev/null"]

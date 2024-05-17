FROM docker.io/library/openjdk:11-jre

COPY --from=docker.io/ochinchina/supervisord:latest /usr/local/bin/supervisord /usr/bin/supervisord
COPY supervisord.conf /usr/local/kafka/supervisord.conf
COPY kafka-docker-config.sh /usr/local/kafka/bin/kafka-docker-config.sh

RUN curl -s https://dlcdn.apache.org/kafka/3.0.0/kafka_2.13-3.0.0.tgz | tar -xz --strip-components=1 -C /usr/local/kafka

WORKDIR /usr/local/kafka
ENV PATH=/usr/local/kafka/bin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

CMD ["supervisord"]

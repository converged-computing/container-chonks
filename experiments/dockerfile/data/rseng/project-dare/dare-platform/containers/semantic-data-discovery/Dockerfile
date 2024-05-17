FROM python:3.7-buster

RUN pip install --upgrade pip

ENV SOLR_HOST=solr
ENV SOLR_CORE=linked
ENV VIRTUOSO_SPARQL=virtuoso

WORKDIR /opt/
RUN  wget https://gitlab.com/project-dare/semantic-data-discovery/-/archive/master/semantic-data-discovery-master.zip; \
    unzip semantic-data-discovery-master.zip; \
    rm semantic-data-discovery-master.zip; \
    mkdir /etc/app; \
    cp ./semantic-data-discovery-master/config/config_docker.json /etc/app/config.json;

WORKDIR /opt/semantic-data-discovery-master

RUN pip install waitress; \
    pip install --no-cache-dir -r requirements.txt;

EXPOSE 5000

COPY docker_entry.sh /opt/semantic-data-discovery-master/

ENTRYPOINT [ "sh", "./docker_entry.sh" ]
# CMD tail -f /dev/null
FROM python:3.6-alpine3.7

ENV SPROV_API_HOST=sprov
ENV SPROV_API_PORT=8082
ENV MSGQ_HOST=rabbitmq
ENV MSGQ_PORT=5672

RUN pip install --upgrade pip

RUN apk --no-cache \
     --update-cache add --virtual dep zip procps build-base wget libxslt libxslt-dev && \
     wget https://gitlab.com/project-dare/s-ProvFlow/-/archive/1.2.7/s-ProvFlow-1.2.7.zip && \
     unzip s-ProvFlow-1.2.7.zip && \
     find ./s-ProvFlow-1.2.7 -type f -name "*.log" | xargs -I {} rm -f {} && \
     find ./s-ProvFlow-1.2.7 -type f -name "*.pyc" | xargs -I {} rm -f {} && \
     pip install --no-cache-dir -r ./s-ProvFlow-1.2.7/prov-queue/requirements.txt && \
     apk del dep && apk add libxslt && \
     rm s-ProvFlow-1.2.7.zip && \
     apk --no-cache add mongodb

WORKDIR /s-ProvFlow-1.2.7/prov-queue

COPY docker_entry.sh .

EXPOSE 5000

ENTRYPOINT [ "sh", "./docker_entry.sh" ]

FROM python:3.6-alpine3.7

## Substitute the variables below in the K8s deployment from a secret.
ENV SPROV_API_KEYCLOAK_CLIENT_ID=sprov-api-client-id
ENV SPROV_API_KEYCLOAK_CLIENT_SECRET=sprov-api-client-secret
ENV AUTH_VALIDATE_BEARER_TOKEN=false

ENV SPROV_DB=sprov-db
ENV SPROV_DB_HOST=mongodb
ENV SPROV_DB_PORT=27017

RUN mkdir -p /tmp/import

RUN pip install --upgrade pip

RUN apk --no-cache \
     --update-cache add --virtual dep zip procps build-base wget libxslt libxslt-dev && \
     wget https://gitlab.com/project-dare/s-ProvFlow/-/archive/1.2.7/s-ProvFlow-1.2.7.zip && \
     unzip s-ProvFlow-1.2.7.zip && \
     find ./s-ProvFlow-1.2.7 -type f -name "*.log" | xargs -I {} rm -f {} && \
     find ./s-ProvFlow-1.2.7 -type f -name "*.pyc" | xargs -I {} rm -f {} && \
     pip install --no-cache-dir -r ./s-ProvFlow-1.2.7/provenance-api/requirements.txt && \
     apk del dep && apk add libxslt && \
     rm s-ProvFlow-1.2.7.zip && \
     apk --no-cache add mongodb

## Must be run in a separate layer apparently, or it will not get installed.
## It is needed to run the `envsubst` command in docker_entry.sh
RUN apk add gettext

WORKDIR /s-ProvFlow-1.2.7/provenance-api/src/prov-services/

COPY SPROV_API_client_secrets.json .
COPY docker_entry.sh .

EXPOSE 8082

ENTRYPOINT [ "sh", "./docker_entry.sh" ]


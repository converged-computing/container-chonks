FROM python:3.7-alpine3.7

LABEL maintainer="Project DARE <support@project-dare.eu>" \
      org.opencontainers.image.title="D4py registry" \
      org.opencontainers.image.description="Registry to serve processing elements for Dispel4py" \
      org.opencontainers.image.source="https://gitlab.com/project-dare/d4py-registry.git" \
      org.opencontainers.image.vendor="Project DARE"

RUN pip install --upgrade pip

ARG RELEASE=v1.2
ARG BUILD_DATE

LABEL org.opencontainers.image.revision=$RELEASE \
      org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.version=$RELEASE

# Install python packages and mysql
RUN apk add --no-cache mariadb-client-libs mysql-client && \
    apk add --no-cache --virtual .build-deps build-base mariadb-dev libffi-dev git && \
    git clone --branch $RELEASE --single-branch https://gitlab.com/project-dare/d4p-registry.git registry && \
    pip install -r /registry/python_env_requirements.txt && \
    pip install gunicorn && \
    rm -rf /registry/.git && \
    apk del .build-deps

RUN apk add --no-cache bash

WORKDIR /registry
COPY ./docker_entrypoint.sh .
EXPOSE 8000
ENTRYPOINT ["sh", "./docker_entrypoint.sh"]
CMD []

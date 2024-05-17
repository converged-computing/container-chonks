FROM python:3.7-alpine3.7

RUN pip install --upgrade pip

ARG RELEASE=v1.3
ARG BUILD_DATE

# Install python packages and mysql
RUN apk add --no-cache mariadb-client-libs mysql-client && \
    apk add --no-cache --virtual .build-deps build-base git mariadb-dev libffi-dev git && \
    git clone --branch $RELEASE --single-branch https://gitlab.com/project-dare/workflow-registry.git && \
    pip install -r /workflow-registry/requirements.txt && \
    pip install gunicorn && \
    rm -rf /workflow-registry/.git && \
    apk del .build-deps

RUN apk add --no-cache bash vim

WORKDIR /workflow-registry
COPY ./docker_entrypoint.sh .
EXPOSE 8002
CMD bash docker_entrypoint.sh
# CMD tail -f /dev/null

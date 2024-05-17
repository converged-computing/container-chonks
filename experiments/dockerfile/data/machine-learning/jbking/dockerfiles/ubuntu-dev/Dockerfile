FROM ubuntu:19.04

ENV DEBIAN_FRONTEND=noninteractive
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
 curl \
 git \
 zip \
 unzip \
 iputils-ping \
 vim-nox \
 openssh-client \
 openssh-server \
 silversearcher-ag \
 wait-for-it \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

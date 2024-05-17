FROM ubuntu:focal

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends software-properties-common \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN add-apt-repository ppa:deadsnakes/ppa
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
 python3.6-dev \
 python3.7-dev \
 python3.8-dev \
 tox \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

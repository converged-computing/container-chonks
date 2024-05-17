FROM ubuntu:trusty

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends software-properties-common \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN add-apt-repository ppa:fkrull/deadsnakes
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
 python2.7 python-pip python-dev \
 python3 python3-pip python3-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# install common utilities
COPY requirements.txt /tmp/
RUN pip2 install -r /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

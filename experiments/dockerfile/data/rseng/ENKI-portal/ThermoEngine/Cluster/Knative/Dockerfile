# Copyright (c) ENKI Development Team.
# Distributed under the terms of the Affero General Public License
# Latest version uses Python 3.11 and Ubuntu 22.04
# ThermoEngine has not yet been ported to Python 3.11
# This image was created on May 30, 2023
ARG BASE_CONTAINER=jupyter/docker-stacks-foundation:python-3.10.8
FROM $BASE_CONTAINER

LABEL maintainer="Mark Ghiorso <ghiorso@ofm-research.org>"
USER root

# compilers required for ENKI libgnustep-base-dev --no-install-recommends
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y dist-upgrade && \
    apt-get -y autoremove && \
    apt-get install -y  \
    git \
    nano-tiny \
    tzdata \
    unzip \
    vim-tiny \
    openssh-client \
    less \
    # ---- enki dependencies ----
    gfortran \
    gcc \
    cmake \
    clang-14 \
    libgsl-dev \
    liblapack-dev \
    zip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY /usr/local/lib

RUN git clone https://gitlab.com/ENKI-portal/rubiconobjc.git && \
    cd ./rubiconobjc && \
    pip install --upgrade . && \
    cd .. && \
    rm -rf ./rubiconobjc

ARG SAVE_PATH=$PATH
#ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
#ENV TZ=US/Pacific
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN git clone https://github.com/plaurent/gnustep-build && \
    cd gnustep-build/ubuntu-22.04-clang-14.0-runtime-2.1/ && \
    bash GNUstep-buildon-ubuntu2204.sh && \
    cd ../.. && \
    rm -rf ./gnustep-build

ENV PATH $SAVE_PATH

# Install ThermoEngine repository (note && \ missing from first line)
ENV RUNTIME_VERSION gnustep-2.1
COPY / /thermoengine/
RUN cd /thermoengine/Cluster && \
    make && \
    /usr/bin/install -c -p  ./obj/libswimdew.so.0.0.1 /usr/local/lib && \
    ln -s /usr/local/lib/libswimdew.so.0.0.1 /usr/local/lib/libswimdew.so.0 && \
    ln -s /usr/local/lib/libswimdew.so.0 /usr/local/lib/libswimdew.so && \
    /usr/bin/install -c -p  ./obj/libphaseobjc.so.0.0.1 /usr/local/lib && \
    ln -s /usr/local/lib/libphaseobjc.so.0.0.1 /usr/local/lib/libphaseobjc.so.0 && \
    ln -s /usr/local/lib/libphaseobjc.so.0 /usr/local/lib/libphaseobjc.so && \
    cd .. && \
    make pyinstall && \
    cd .. && \
    rm -rf ./thermoengine

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID

WORKDIR $HOME
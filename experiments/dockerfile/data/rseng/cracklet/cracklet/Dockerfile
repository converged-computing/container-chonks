FROM ubuntu:18.04
MAINTAINER Thibault Roch <thibault.roch@epfl.ch>

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

## for apt to be noninteractive
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#run
RUN apt-get -qq update && apt-get -y -qq install \
    clang \
    g++ \
    gfortran \
    curl \
    doxygen \
    git \
    gpg \
    wget \
    libgsl-dev \
    libfftw3-dev \
    python3-pip \
    python3-breathe \
    python3-dev \
    python3-pytest \
    python3-mpi4py \
    python3-numpy \
    python3-pytest \
    python3-sphinx \
    python3-sphinx-rtd-theme \
    && rm -rf /var/lib/apt/lists/*

# https://apt.kitware.com/
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null \
    && echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ bionic main' | tee /etc/apt/sources.list.d/kitware.list >/dev/null \
    && apt-get update \
    && rm /usr/share/keyrings/kitware-archive-keyring.gpg \
    && apt-get install -y \
    kitware-archive-keyring \
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install gcovr

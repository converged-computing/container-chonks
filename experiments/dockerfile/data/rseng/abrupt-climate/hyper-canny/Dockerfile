FROM ubuntu:xenial
MAINTAINER Johan Hidding <j.hidding@esciencecenter.nl>

RUN apt-get update && apt-get install --no-install-recommends -yq \
    build-essential g++-5 python3 python3-pip \
    libpng12-dev mesa-opencl-icd ocl-icd-opencl-dev opencl-headers \
    libnetcdf-dev libnetcdf-c++4-dev libhdf5-dev \
    python3-wheel python3-setuptools ninja-build pkg-config \
    lcov curl git libfftw3-dev locales

RUN apt-get install --no-install-recommends -yq \
    language-pack-en

RUN pip3 install meson

COPY . /usr/src/hyper-canny
WORKDIR /usr/src/hyper-canny
ENV LC_ALL=en_GB.UTF-8

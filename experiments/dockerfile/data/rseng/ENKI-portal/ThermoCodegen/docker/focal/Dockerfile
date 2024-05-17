# Copyright (C) 2018 ENKI Project
#
# Please see the AUTHORS file in the main source directory for a full list
# of contributors.
#
# This file is part of Thermocodegen
#
# Thermocodegen is free software: you can redistribute it and/or modify
# it under the terms of the MIT License
#
# Thermocodegen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# License for more details.
#
# You should have received a copy of the MIT license
# along with Thermocodegen
#
# Builds a Docker image with a full installation of ThermoCodegen

# build off Ubuntu 20.04LTS (Focal) with a few fixes for docker
FROM phusion/baseimage:focal-1.2.0 AS base
MAINTAINER cwilson <cwilson@carnegiescience.edu>

ARG BRANCH=main
ARG BUILD=Release
ARG REPO=https://gitlab.com/ENKI-portal/ThermoCodegen.git 

# Get Ubuntu updates
USER root
RUN apt-get update && \ 
    apt-get upgrade -y -o Dpkg::Options::="--force-confold" -o Dpkg::Options::="--force-confdef" && \
    apt-get -y install locales sudo && \
    apt-get clean && \
    echo "C.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set locale environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8

COPY set-home-permissions.sh /etc/my_init.d/set-home-permissions.sh

# Set up user so that we do not run as root
# See https://github.com/phusion/baseimage-docker/issues/186
# Disable forward logging
# Add script to set up permissions of home directory on myinit
# Run ldconfig so that /usr/local/lib is in the default search
# path for the dynamic linker.
RUN useradd -m -s /bin/bash -G sudo,docker_env,adm tcg && \
    echo "tcg:docker" | chpasswd && \
    echo "tcg ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    echo "PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\W\[\033[00m\]\$ '" >> /home/tcg/.bashrc && \
    echo "cat /home/tcg/WELCOME" >> /home/tcg/.bashrc && \
    rm /etc/my_init.d/10_syslog-ng.init && \
    chmod +x /etc/my_init.d/set-home-permissions.sh && \
    ldconfig

ENV INSTALL_PREFIX  /usr/local/thermocodegen
ENV INCLUDE         $INSTALL_PREFIX/include:$INCLUDE
ENV LD_LIBRARY_PATH $INSTALL_PREFIX/lib:$LD_LIBRARY_PATH
ENV LIBRARY_PATH    $INSTALL_PREFIX/lib:$LIBRARY_PATH
ENV PATH            $INSTALL_PREFIX/bin:$PATH
ENV PKG_CONFIG_PATH $INSTALL_PREFIX/lib/pkgconfig:$PKG_CONFIG_PATH
ENV PYTHONPATH      $INSTALL_PREFIX/lib/python3.8/site-packages:$PYTHONPATH
ENV MANPATH         $INSTALL_PREFIX/share/man:$MANPATH
 
# Weird Timezone hack for some reason
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir $INSTALL_PREFIX && \
    chgrp adm -R $INSTALL_PREFIX && \
    chmod g+w -R $INSTALL_PREFIX && \
    chmod a+w /tmp

USER tcg
ENV TCG_HOME /home/tcg
RUN touch $TCG_HOME/.sudo_as_admin_successful && \
    mkdir $TCG_HOME/shared && \
    mkdir -p $INSTALL_PREFIX/lib/python3.8/site-packages
VOLUME /home/tcg/shared

# Print a default welcome message on startup
COPY WELCOME.base $TCG_HOME/WELCOME

WORKDIR $TCG_HOME
USER root
ENTRYPOINT ["/sbin/my_init","--quiet","--","/sbin/setuser","tcg","/bin/bash","-l","-c"]
CMD ["/bin/bash","-i"]

#############################################################################################
# Next stage
FROM base as env

USER root
WORKDIR /tmp

# Install dependencies
RUN apt-get update && \
    apt-get -y --with-new-pkgs \
        -o Dpkg::Options::="--force-confold" -o Dpkg::Options::="--force-confdef" upgrade && \
    apt-get -y install \
                       git \
                       gcc \
                       g++ \
                       gfortran \
                       cmake \
                       flex \
                       wget \
                       gir1.2-gtksource-3.0 \
                       gir1.2-gtk-3.0 \
                       adwaita-icon-theme-full \
                       pkg-config \
                       tcl \
                       vim \
                       libgsl-dev \
                       pybind11-dev \
                       doxygen \
                       imagemagick \
                       plantuml \
                       pandoc \
                       environment-modules \
                       nodejs \
                       npm \
                       cython3 \
                       python3 \
                       python3-setuptools \
                       python3-matplotlib \
                       python3-ply \
                       python3-future \
                       python3-gi \
                       python3-lxml \
                       python3-cairocffi \
                       python3-cairo \
                       python3-gi-cairo \
                       python3-pip \
                       python3-requests \
                       python3-sphinx \
                       python3-sphinx-argparse \
                       python3-nbsphinx \
                       python3-mock \
                       python3-sphinx-rtd-theme \
                       python3-breathe && \
               apt-get clean && \
               rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# download and install spud from source
RUN git clone -q https://github.com/FluidityProject/spud.git && \
    cd spud && \
    ./configure --prefix=$INSTALL_PREFIX && \
    make && \
    make install && \
    rm -rf /tmp/*
ENV SPUD_DIR $INSTALL_PREFIX

# supress some spurious gtk errors
ENV NO_AT_BRIDGE 1

# sphinx-js dependencies: jsdoc and typedoc (TypeScript support)
RUN npm install --global \
        jsdoc \
        typedoc && \
    rm -rf /tmp/* /var/tmp/*

# Install python packages
RUN pip3 install \
                 -Iv sympy==1.3 \
                 -Iv numpy==1.22.4 \
                 -Iv scipy==1.6.3 \
                 pandas==1.4.3 \
                 pytest==4.6.9 \
                 jupyter-client==6.1.2 \
                 jupyter-console==6.0.0 \
                 jupyter-core==4.6.3 \
                 jupyterlab==2.3.2 \
                 nbconvert==5.6.1 \
                 MarkupSafe==1.1.0 \
                 Jinja2==2.10.1 \
                 molmass==2021.6.18 \
                 prompt-toolkit==3.0.30

# supress deprecation warnings from older packages
ENV PYTHONWARNINGS ignore::DeprecationWarning

USER tcg
WORKDIR $TCG_HOME

# update welcome message
COPY WELCOME.env $TCG_HOME/WELCOME

USER root

#############################################################################################
# Next stage
FROM env as tcg

USER root
WORKDIR /tmp

# Install ThermoCodegen
RUN git clone -b $BRANCH $REPO  && \
    cd ThermoCodegen && \
    mkdir build && \
    cd build && \
    cmake ..  -DCMAKE_INSTALL_PREFIX=$INSTALL_PREFIX -DCMAKE_BUILD_TYPE=$BUILD  && \
    make install && \
    rm -rf /tmp/*
ENV THERMOCODEGEN_HOME        $INSTALL_PREFIX
ENV THERMOCODEGEN_CMAKE_PATH  $INSTALL_PREFIX/share/thermocodegen/cmake
ENV CMAKE_MODULE_PATH         $INSTALL_PREFIX/share/thermocodegen/cmake/modules:$CMAKE_MODULE_PATH
ENV DIAMOND_CONFIG_PATH       $INSTALL_PREFIX/share/thermocodegen/diamond:$DIAMOND_CONFIG_PATH
ENV CPLUS_INCLUDE_PATH        $INSTALL_PREFIX/include/swimdew:$CPLUS_INCLUDE_PATH

USER tcg
WORKDIR $TCG_HOME

# update welcome message
COPY WELCOME.tcg $TCG_HOME/WELCOME
RUN cp -r $INSTALL_PREFIX/share/thermocodegen/examples/Systems $TCG_HOME/systems

USER root

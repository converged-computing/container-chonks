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
# You should have received a copy of the MIT
# along with Thermocodegen
#
# Builds a Docker image with a full installation of TerraFERMA v2.0 and ThermoCodegen v0.6.9

# build using the TerraFERMA v2.0
FROM ghcr.io/terraferma/dev:fenics-2019.1.0-focal AS env
MAINTAINER mspieg <mspieg@ldeo.columbia.edu>

ARG BRANCH=main
ARG BUILD=Release
ARG REPO=https://gitlab.com/ENKI-portal/ThermoCodegen.git 

USER root
WORKDIR /tmp

# Install dependencies not included in TF image
RUN apt-get update && \
    apt-get -y --with-new-pkgs \
        -o Dpkg::Options::="--force-confold" -o Dpkg::Options::="--force-confdef" upgrade && \
    apt-get -y install \
                     flex \
                     pkg-config \
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
                     python3-scipy \
                     python3-requests \
                     python3-sphinx \
                     python3-sphinx-argparse \
                     python3-nbsphinx \
                     python3-mock \
                     python3-sphinx-rtd-theme \
                     python3-breathe && \
               apt-get clean && \
               rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# sphinx-js dependencies: jsdoc and typedoc (TypeScript support)
RUN npm install --global \
        jsdoc \
        typedoc && \
    rm -rf /tmp/* /var/tmp/*

# install thermocodegen dependencies (does it really need cython?)
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
                 
USER tfuser
WORKDIR $TF_HOME

# update welcome message
COPY WELCOME.env $TF_HOME/WELCOME

USER root

#############################################################################################
# Next stage
FROM env as tcg

USER root
WORKDIR /tmp

# Install ThermoCodegen
ENV THERMOCODEGEN_HOME /usr/local/thermocodegen
RUN git clone -b $BRANCH $REPO  && \
    cd ThermoCodegen && \
    mkdir build && \
    cd build && \
    cmake ..  -DCMAKE_INSTALL_PREFIX=${THERMOCODEGEN_HOME} -DCMAKE_BUILD_TYPE=$BUILD  && \
    make install && \
    rm -rf /tmp/* && \
    chgrp adm -R $THERMOCODEGEN_HOME && \
    chmod g+w -R $THERMOCODEGEN_HOME

ENV THERMOCODEGEN_CMAKE_PATH  $THERMOCODEGEN_HOME/share/thermocodegen/cmake
ENV CMAKE_MODULE_PATH         $THERMOCODEGEN_HOME/share/thermocodegen/cmake/modules:$CMAKE_MODULE_PATH
ENV PYTHONPATH                $THERMOCODEGEN_HOME/lib/python3.8/site-packages:$PYTHONPATH
ENV DIAMOND_CONFIG_PATH       $THERMOCODEGEN_HOME/share/thermocodegen/diamond:$DIAMOND_CONFIG_PATH
ENV PATH                      $THERMOCODEGEN_HOME/bin:$PATH
ENV CPLUS_INCLUDE_PATH        $THERMOCODEGEN_HOME/include/swimdew:$CPLUS_INCLUDE_PATH
ENV LD_LIBRARY_PATH           $THERMOCODEGEN_HOME/lib:$LD_LIBRARY_PATH
ENV LIBRARY_PATH              $THERMOCODEGEN_HOME/lib:$LIBRARY_PATH

USER tfuser
WORKDIR $TF_HOME

# update welcome message
COPY WELCOME.tcg $TF_HOME/WELCOME
RUN cp -r $THERMOCODEGEN_HOME/share/thermocodegen/examples/Systems $TF_HOME/systems

USER root

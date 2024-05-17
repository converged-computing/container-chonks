# Copyright (c) ENKI Development Team.
# Distributed under the terms of the Affero General Public License
# Latest version uses Python 3.11 and Ubuntu 22.04
# ThermoEngine has not yet been ported to Python 3.11
# This image was created on May 30, 2023
ARG BASE_CONTAINER=jupyter/all-spark-notebook:4d70cf8da953
FROM $BASE_CONTAINER

LABEL maintainer="Mark Ghiorso <ghiorso@ofm-research.org>"

USER root

# compilers required for ENKI libgnustep-base-dev --no-install-recommends
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y dist-upgrade
RUN apt-get -y autoremove
RUN apt-get install -y  \
    gfortran \
    gcc \
    cmake \
    clang-14 \
    libgsl-dev \
    liblapack-dev \
    zip
RUN rm -rf /var/lib/apt/lists/*

USER $NB_UID

# install latex packages
RUN pip install --no-cache-dir jupyterlab_latex
RUN jupyter serverextension enable --sys-prefix jupyterlab_latex
RUN pip install --no-cache-dir openpyxl
RUN pip install --no-cache-dir snakeviz
RUN conda clean --all -f -y
RUN jupyter labextension install @enki-portal/jupyterlab-gitlab --no-build
RUN jupyter labextension install @enki-portal/shared --no-build
RUN jupyter labextension install @enki-portal/enkiintro --no-build
RUN jupyter labextension install @jupyterlab/latex --no-build
RUN jupyter lab build
RUN jupyter lab clean
RUN npm cache clean --force
RUN rm -rf /home/$NB_USER/.cache/yarn
RUN rm -rf /home/$NB_USER/.node-gyp
RUN fix-permissions $CONDA_DIR
RUN fix-permissions /home/$NB_USER

# install additional package...
RUN pip install --no-cache-dir nbgitpuller
RUN pip install --no-cache-dir deprecation
RUN pip install --no-cache-dir numdifftools
RUN pip install --no-cache-dir jupyter-resource-usage
RUN pip install --no-cache-dir VESIcal
RUN pip install --no-cache-dir jupyterlab-gitlab-msg
RUN jupyter serverextension enable --sys-prefix jupyterlab_gitlab

USER root

ENV LD_LIBRARY /usr/local/lib

RUN git clone https://gitlab.com/ENKI-portal/rubiconobjc.git
RUN cd ./rubiconobjc && \
    pip install --no-cache-dir . && \
    cd .. && \
    rm -rf ./rubiconobjc

# Install GNUstep components from sources (requires Python 2.7, hence the path change)
ARG SAVE_PATH=$PATH
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

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

USER $NB_UID
    

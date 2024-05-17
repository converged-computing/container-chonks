# Dispel4py Docker file based on https://gitlab.com/project-dare/dispel4py/blob/master/Dockerfile

# FROM ubuntu:latest
FROM python:3.7
RUN apt-get update && apt-get install -y openmpi-bin=3.1.3-11 \
libopenmpi-dev=3.1.3-11 git vim sudo uuid-runtime libgeos-dev libgdal-dev

ENV USER mpiuser
ENV HOME /home/mpiuser/docker
ENV MPLBACKEND=Agg
ENV GEOS_DIR `geos-config --prefix`

RUN adduser ${USER} --disabled-password --gecos ""

RUN pip install mpi4py==3.0.1 numpy==1.18.5 ujson pyyaml
RUN pip install GDAL==`gdal-config --version`

USER ${USER}
WORKDIR ${HOME}

USER root

RUN pip install cwl-runner
RUN pip install cwltool==1.0.20190621234233
RUN pip install pyjwt

ARG RELEASE=master

RUN git clone --branch $RELEASE --single-branch https://gitlab.com/project-dare/dispel4py.git \
    && cd dispel4py && python setup.py install

# icclim - uncomment the below for the icclim image
# RUN git clone https://github.com/cerfacs-globc/icclim && cd icclim && \
    # gcc -fPIC -g -c -Wall ./icclim/libC.c -o ./icclim/libC.o && \
    # gcc -shared -o ./icclim/libC.so ./icclim/libC.o && \
    # python setup.py install
# RUN pip install netcdf4 cython
# RUN pip install netcdftime
# RUN rm -rf icclim

WORKDIR ${HOME}

COPY mpiexec-d4py-tool.cwl ${HOME}
COPY entrypoint.sh ${HOME}
COPY start_mpi.sh ${HOME}
COPY env_prep.sh ${HOME}
COPY start_simple.sh ${HOME}
COPY d4p-simple.cwl ${HOME}

CMD bash env_prep.sh && sleep 1 && bash entrypoint.sh
# CMD tail -f /dev/null

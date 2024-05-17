FROM python:3.7

RUN apt-get update && apt-get install -y \
  git \
  openmpi-bin=3.1.3-11 \
  libopenmpi-dev=3.1.3-11 \
  libgeos-dev \
  libgdal-dev \
  sudo \
  vim 

ENV USER mpiuser
ENV HOME /home/mpiuser/docker
RUN adduser ${USER} --disabled-password --gecos ""
WORKDIR ${HOME}

RUN pip install mpi4py==3.0.1
 
# Add the various Python dependencies.
RUN pip install \
  matplotlib==3.1.3 \
  numpy==1.19.0 \
  pandas==1.0.3 \
  scipy==1.4.1 \
  pyyaml==5.3.1 \
  && pip install shapely --no-binary shapely \
  && pip install \
  cwl-runner \
  cwltool==1.0.20190621234233 \
  Pillow==7.0.0 \
  ujson

# A simple pip install gdal will fail, because We need to install the GDAL 
# python module that fits exactly to the native gdal libraries we installed
# with apt-get above.
RUN pip install GDAL==`gdal-config --version`

# set matplotlib backend, this needs to be changed if the python version is changed.
RUN echo "backend : Agg" > /usr/local/lib/python3.7/site-packages/matplotlib/mpl-data/matplotlibrc

RUN chown -R ${USER}:${USER} /home/mpiuser
USER ${USER}

COPY entrypoint.sh ${HOME}
CMD bash entrypoint.sh
# CMD tail -f /dev/null

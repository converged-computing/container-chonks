FROM python:3.7

RUN apt update && apt install -y gcc-7 git make cmake gfortran-7 libnetcdf-dev libnetcdff-dev libudunits2-dev libproj-dev proj-data proj-bin libgeos-dev

RUN pip install cwl-runner
RUN pip install cwltool==1.0.20190621234233
RUN pip install numpy
RUN pip install pandas
RUN pip install xarray
RUN pip install netCDF4
RUN pip install pydap
RUN pip install dask[dataframe]
RUN pip install matplotlib
RUN pip install cython
RUN pip install scipy
RUN pip install pyshp
RUN pip install six
RUN pip install shapely --no-binary shapely
RUN pip install cartopy

RUN useradd -ms /bin/bash mpiuser
RUN mkdir /home/mpiuser/docker

ENV USER mpiuser
ENV HOME /home/mpiuser/docker

ENV FC gfortran-7
ENV CC gcc-7

RUN cd ${HOME} && git clone https://github.com/wavebitscientific/datetime-fortran.git && cd datetime-fortran && mkdir build && cd build && cmake .. && make && cd ${HOME}

RUN cd ${HOME} && git clone https://github.com/jacobwilliams/json-fortran.git && cd json-fortran && mkdir build && cd build && cmake .. && make && cd ${HOME}

RUN mkdir ${HOME}/workflow_cmip6
RUN cd ${HOME} && git        clone -b master https://gitlab.com/project-dare/wp7_cyclone-tracking.git ${HOME}/workflow_cmip6

RUN cd ${HOME} && git clone https://github.com/cerfacs-globc/cctrack.git ./tracking && cd tracking && cp Makefile.nemo Makefile.dare && \
sed -i 's<INCDIR=.*<INCDIR=/usr/include<' Makefile.dare && sed -i 's<LIBDIR=.*<LIBDIR=/usr/lib<' Makefile.dare && \
sed -i 's<BINDIR=.*<BINDIR=$(HOME)/workflow_cmip6<' Makefile.dare && \
sed -i 's<DATETIMEINCDIR=.*<DATETIMEINCDIR=$(HOME)/datetime-fortran/build/include<' Makefile.dare && \
sed -i 's<DATETIMELIBDIR=.*<DATETIMELIBDIR=$(HOME)/datetime-fortran/build/lib<' Makefile.dare && \
sed -i 's<UDUNITSINCDIR=.*<UDUNITSINCDIR=/usr/include<' Makefile.dare && \
sed -i 's<UDUNITSLIBDIR=.*<UDUNITSLIBDIR=/usr/lib<' Makefile.dare && \
sed -i 's<JSONFORTRAN=.*<JSONFORTRAN=$(HOME)/json-fortran/build<' Makefile.dare && \
sed -i 's<^FC=.*<FC=gfortran-7<' Makefile.dare && \
sed -i 's<^CC=.*<CC=gcc-7<' Makefile.dare \
&& mkdir lib && make -f Makefile.dare

RUN cd ${HOME}  && git  clone https://github.com/cerfacs-globc/cctrack_tracking_products.git ${HOME}/cyclone_tracking_products && cd ${HOME}/cyclone_tracking_products && python setup.py install && cd ${HOME}

ENV LD_LIBRARY_PATH="${HOME}/json-fortran/build/lib/"
ENV CARTOPY_USER_BACKGROUNDS="${HOME}/workflow_cmip6"

WORKDIR ${HOME}

RUN mkdir ${HOME}/results
COPY input_files.txt ${HOME}/workflow_cmip6/input_files.txt
COPY config_cmip6.txt ${HOME}/workflow_cmip6/config_cmip6.txt
COPY cyclone_config_CMIP6.json ${HOME}/workflow_cmip6/cyclone_config_CMIP6.json

RUN cp ${HOME}/cyclone_tracking_products/cyclonetrackprod/images.json ${HOME}/workflow_cmip6/images.json
RUN cp ${HOME}/cyclone_tracking_products/cyclonetrackprod/BMNG_hiver.jpg ${HOME}/workflow_cmip6/BMNG_hiver.jpg

RUN ls -l ${HOME} ${HOME}/tracking ${HOME}/workflow_cmip6

ENTRYPOINT bash ${HOME}/workflow_cmip6/tracking_master.sh ${HOME}/workflow_cmip6 ${HOME}/results ${HOME}/workflow_cmip6/cyclone_config_CMIP6.json ${HOME}/workflow_cmip6/config_cmip6.txt ${HOME}/workflow_cmip6/input_files.txt

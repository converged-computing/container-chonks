FROM alpine:3.9 as builder

# to compile hdf5 with fortran we need gawk because there is an awk line in
# the configure script that the busybox awk doesnt support (length + 1). 
RUN apk --no-cache --update-cache add \
    gawk \
    wget \
    bash \
    boost-dev \
    cmake \
    gcc \
    gfortran \
    bison \
    git \
    zlib \
    zlib-dev \
    build-base \
    libgfortran \
    gsl \
    make 

RUN apk --no-cache --update-cache add \
    -X http://dl-cdn.alpinelinux.org/alpine/edge/main \
    numactl

# we should build this ourselves as well because this will break when edge
# gets an upgraded gfortran with higher module version.
RUN apk --no-cache --update-cache add \
    -X http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    openmpi \
    openmpi-dev

# the repo version doesnt have parallel hdf5, so build custom. this needs
# gawk, see note above.
RUN cd /tmp ; \
    wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.6/src/hdf5-1.10.6.tar.gz ; \
    tar xvf hdf5-1.10.6.tar.gz ; \
    cd hdf5-1.10.6/ ; \
    ./configure --prefix=/usr/local --enable-parallel --enable-fortran --enable-tools=no --enable-tests=no ; \
    make -j16 ; \
    make install

# this is the library for Adaptable Seismic Data Format
RUN cd /tmp ; \
    git clone https://github.com/SeismicData/asdf-library.git ; \
    cd asdf-library ; \
    cmake . . -DCMAKE_Fortran_COMPILER=mpif90 -DCMAKE_INSTALL_PREFIX=/usr/local ; \
    make ; \
    make install

# use specific version of specfem3d devel that was tested to work properly.
# there is a bug in the specfem3d configure file, it uses pushd/popd but runs in sh. we patch that with sed.
RUN cd /tmp ; \
    git clone --recursive --branch devel https://github.com/geodynamics/specfem3d.git ; \
    cd specfem3d/ ; \
    git checkout 72ff487685c89139b22124958708b29f4c76f640 ; \
    sed -i 's|#! /bin/sh|#! /bin/bash|' configure ; \
    FC=gfortran CC=gcc MPIFC=mpif90 ./configure --with-mpi --with-asdf=yes --enable-vectorization; \
    make xmeshfem3D xgenerate_databases xspecfem3D xdecompose_mesh

# create a new image that just contains the necessary binaries.
FROM alpine:3.9

ENV PATH /usr/local/bin:$PATH

RUN apk --no-cache --update-cache add \
    libgfortran openssh-client  &&\
    apk --no-cache --update-cache add \
    -X http://dl-cdn.alpinelinux.org/alpine/edge/main \
    numactl &&\
    apk --no-cache --update-cache add \
    -X http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    openmpi \
    openmpi-dev

COPY --from=builder /usr/local/lib/* /usr/local/lib/
COPY --from=builder /tmp/specfem3d/bin/ /usr/local/bin 



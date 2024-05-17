FROM gcc
LABEL maintainer=@joshuacook
RUN apt-get update && \
      apt-get install -y \
      gsl-bin \
      libgsl0-dbg \
      libgsl0-dev \
      libgsl2

RUN apt-get update && \
    apt-get install -y gdb

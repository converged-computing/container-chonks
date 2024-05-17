FROM registry.gitlab.com/project-dare/dare-platform/specfem3d:latest

RUN apk --no-cache --update-cache add \
    git \
    linux-headers \
    libxml2-dev \
    libxslt-dev \
    gcc \
    libc-dev \
    python3-dev \
    py3-pip \
    python3 \
    bash \
    rsync \
	curl \ 
    zip && \
    pip3 install cwlref-runner

ENV USER mpiuser
ENV HOME /home/mpiuser/docker
RUN adduser ${USER} --disabled-password --gecos "" && mkdir ${HOME} && chown ${USER} ${HOME}

USER ${USER}
WORKDIR ${HOME}

RUN git clone -b RA_total_script --depth 1 https://gitlab.com/project-dare/WP6_EPOS.git
RUN mv WP6_EPOS/specfem3d/specfem3d_test_input_cwl/* ${HOME}
RUN rm -rf WP6_EPOS

RUN sed -i 's/SPECFEM3D_HOME: \"\/home\/mpiuser\/specfem3d"/SPECFEM3D_HOME: \"\/usr\/local\"/' env_preparation.cwl

COPY ./entrypoint.sh .
COPY ./run_simulations.py .
COPY ./exec_specfem.sh .


ENTRYPOINT bash entrypoint.sh
# CMD tail -f /dev/null
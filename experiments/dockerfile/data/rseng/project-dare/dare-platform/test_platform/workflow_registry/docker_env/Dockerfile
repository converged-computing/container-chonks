FROM python:3.7

RUN apt update && apt install -y openmpi-bin=3.1.3-11 libopenmpi-dev=3.1.3-11 git vim sudo libgeos-dev

ENV USER mpiuser
ENV HOME /home/mpiuser/docker

RUN adduser ${USER} --disabled-password --gecos ""

RUN pip install mpi4py==3.0.1 pyyaml

USER ${USER}
WORKDIR ${HOME}

USER root

RUN pip install cwl-runner
RUN pip install cwltool==1.0.20190621234233

WORKDIR ${HOME}

COPY entrypoint.sh ${HOME}
COPY arguments.cwl ${HOME}
COPY arguments.yaml ${HOME}
COPY demo_workflow.cwl ${HOME}
COPY spec.yaml ${HOME}
COPY tar_param.cwl ${HOME}
COPY tar_param.yaml ${HOME}

CMD bash entrypoint.sh
FROM jupyter/scipy-notebook:latest

ENV SERVER_HOST="localhost"
ENV SERVER_PORT=80
ENV KAFKA_BROKERS="localhost"
ENV KAFKA_TOPIC="vp_traces"
ENV CACHE_HOST="localhost"
ENV CACHE_PORT=88
ENV ENABLE_TC="false"
ENV BANDWIDTH="12Mbps"
ENV LATENCY=15
ENV JITTER=2
ENV GRANT_SUDO="yes"

USER root

RUN apt-get update && apt-get install -y gcc g++ openssh-server htop build-essential python-dev python3-dev iproute2 inetutils-ping kmod iperf3 bmon

USER $NB_UID

COPY requirements.txt /tmp/

RUN mkdir -p code/explora-vr-dash-client/ && chown -R jovyan:users /home/jovyan/code/ && chown -R jovyan:users /home/jovyan/code/explora-vr-dash-client

WORKDIR /home/jovyan/code/explora-vr-dash-client/

COPY --chown=jovyan:users . .

RUN pip install --requirement /tmp/requirements.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

USER $NB_UID

RUN chmod +x ./src/run_no_prefetch_workload.sh
RUN chmod +x ./src/run_prefetch_workload.sh
RUN chmod +x ./src/traffic-control.sh
RUN chmod +x ./src/run_experiment.sh

USER root

RUN chmod +x ./src/traffic-control.sh


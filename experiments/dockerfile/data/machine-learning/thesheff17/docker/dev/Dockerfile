FROM ubuntu:rolling

# docker build . -t thesheff17/dev:latest

RUN echo `date` > /root/build_date.txt

RUN \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    curl \
    vim \
    tmux \
    man \
    python3 \
    python3-dev \
    python3-venv \
    libpq-dev \
    postgresql-client \
    postgresql-client-common && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN yes | unminimize

COPY requirements.txt /root/requirements.txt

RUN \
    curl -q "https://bootstrap.pypa.io/get-pip.py" -o "/root/get-pip.py" && \
    python3 /root/get-pip.py && \
    python3 -m venv /opt/venv && \
    /bin/bash -c " source /opt/venv/bin/activate && pip3 install -r /root/requirements.txt"

CMD ["/bin/bash"]

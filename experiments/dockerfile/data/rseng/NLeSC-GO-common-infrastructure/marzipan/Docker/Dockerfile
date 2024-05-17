FROM ubuntu:18.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 \
    python3-pip \
    python3-dev \
    software-properties-common \
    git \
    vim

#RUN apt-get install -y software-properties-common

RUN apt-add-repository ppa:ansible/ansible && \
    apt-get update && \
    apt-get install -y ansible

# cleanup
RUN rm -rf /tmp/* /var/cache/apt/*

RUN pip3 install pyone configparser ruamel.YAML
#RUN apt-get install -y git

# WORKDIR
WORKDIR /marzipan
COPY Marzipan /marzipan/Marzipan
COPY inventory_builder /marzipan/inventory_builder
COPY marzipan_scripts /marzipan/marzipan_scripts
COPY marzipan_ansible /marzipan/marzipan_ansible
RUN mv /marzipan/marzipan_scripts/marzipan_deploy.py /marzipan/marzipan_deploy.py

# clone emma repo
RUN git clone https://github.com/NLeSC-GO-common-infrastructure/emma.git && cd emma && git checkout emma_marzipan


#RUN ln -s /marzipan/marzipan_scripts/marzipan_deploy.py /marzipan/marzipan_deploy.py
ENTRYPOINT ["/marzipan/marzipan_deploy.py"]

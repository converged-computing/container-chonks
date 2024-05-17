FROM ubuntu:latest

# time docker build . -t thesheff17/dev:latest

RUN  echo 'Acquire::http { Proxy "http://172.17.0.2:3142"; };' >> /etc/apt/apt.conf.d/01proxy

RUN \
    apt-get update && \
    apt-get upgrade -y && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -yq \
    vim tmux build-essential python3 python3-pip python3-dev wget curl gcc g++ make git cmake vim-youcompleteme && \
    vim-addon-manager install youcompleteme && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# install node
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get install -y nodejs

# install golang
RUN wget https://golang.org/dl/go1.14.4.linux-amd64.tar.gz && \
     tar -C /usr/local -xzf go1.14.4.linux-amd64.tar.gz && \
     export PATH=$PATH:/usr/local/go/bin




COPY ./vimrc /root/.vimrc 

CMD ["/bin/bash"]

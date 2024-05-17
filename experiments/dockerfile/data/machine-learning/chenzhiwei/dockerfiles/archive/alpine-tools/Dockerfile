FROM alpine:3.6

RUN apk add --no-cache \
        apache2-utils \
        bash \
        bash-completion \
        bind-tools \
        curl \
        git \
        iproute2 \
        iputils \
        jq \
        net-tools \
        nmap \
        openssh-client \
        rsync \
        unzip \
        vim \
        vimdiff \
        wget \
    && echo '. /etc/profile.d/bash_completion.sh' > /root/.bashrc \
    && mkdir -p /root/.ssh \
    && curl -sSL https://github.com/chenzhiwei/home/raw/master/.vimrc > /root/.vimrc \
    && curl -sSL https://github.com/chenzhiwei/home/raw/master/.gitconfig > /root/.gitconfig \
    && curl -sSL https://github.com/chenzhiwei/home/raw/master/.ssh/config > /root/.ssh/config

CMD ["tail", "-f", "/dev/null"]

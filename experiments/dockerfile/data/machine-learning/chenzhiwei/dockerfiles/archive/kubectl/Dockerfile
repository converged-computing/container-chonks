FROM docker.io/library/alpine:latest

RUN apk add --no-cache \
#        apache2-utils \
        bash \
#        binutils \
#        bind-tools \
        busybox-extras \
        curl \
#        file \
#        git \
        iproute2 \
        iputils \
#        jq \
        net-tools \
#        nmap \
#        openssh-client \
        openssl \
        unzip \
        vim \
        vimdiff \
    && version=$(curl -s -L https://dl.k8s.io/release/stable.txt) \
    && curl -kL -o /usr/bin/kubectl https://storage.googleapis.com/kubernetes-release/release/$version/bin/linux/amd64/kubectl \
    && chmod +x /usr/bin/kubectl

CMD ["/bin/bash"]

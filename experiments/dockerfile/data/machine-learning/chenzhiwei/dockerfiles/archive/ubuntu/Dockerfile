# Ubuntu Docker image with sshd

FROM ubuntu:16.04
MAINTAINER Chen Zhiwei <zhiweik@gmail.com>

# Set default root password
ARG ROOT_PASSWORD=password

# Unlock root user
RUN passwd -u root \

    # Set root password
    && echo "root:$ROOT_PASSWORD" | chpasswd \

    # Force change root password in first login
    && chage -d 0 root \

    # Generate locale
    && locale-gen en_US.UTF-8 \

    # Install essential packages
    && apt update \
    && apt -y install bash-completion curl git net-tools openssh-server rsync vim \

    # Allow root ssh
    && sed -i 's/^PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config \

    && mkdir -p /var/run/sshd

EXPOSE 22

ENTRYPOINT ["/usr/sbin/sshd", "-D"]

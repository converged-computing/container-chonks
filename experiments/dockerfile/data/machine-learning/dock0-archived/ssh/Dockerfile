FROM docker.pkg.github.com/dock0/service/service:20210811-9219a80
MAINTAINER akerl <me@lesaker.org>
RUN pacman -S --noconfirm --needed openssh

ENV ADMIN akerl
ENV KEY_URL https://id-ed25519.pub/groups/default.txt

RUN useradd -d /var/lib/ssh -M ssh_key_sync
RUN mkdir -m=0700 /var/lib/ssh && chown ssh_key_sync /var/lib/ssh
RUN echo "$KEY_URL" > /var/lib/ssh/key_url
ADD sshd_config /etc/ssh/sshd_config
ADD run /service/sshd/run
ADD sync /var/lib/ssh/sync

RUN groupadd remote
RUN useradd -d "/home/$ADMIN" -G remote -m "$ADMIN"
RUN passwd -d "$ADMIN"

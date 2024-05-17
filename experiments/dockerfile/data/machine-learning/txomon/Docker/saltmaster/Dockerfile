#FROM base/archlinux
FROM nfnty/arch-mini
MAINTAINER Javier Domingo Cansino <javierdo1@gmail.com>

RUN pacman -Sy --noconfirm archlinux-keyring
RUN pacman -Su --force --noconfirm
RUN pacman -S --noconfirm salt python2-pygit2

EXPOSE 4505
EXPOSE 4506

VOLUME [ "/etc/salt", "/var/cache/salt", "/var/logs/salt", "/srv/salt"]

CMD salt-master
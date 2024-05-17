#FROM base/archlinux
FROM nfnty/arch-mini
MAINTAINER Javier Domingo Cansino <javierdo1@gmail.com>

RUN pacman -Sy --noconfirm archlinux-keyring
RUN pacman -Su --force --noconfirm
RUN pacman -S --noconfirm weechat perl python2 lua tcl ruby aspell guile

EXPOSE 9000
CMD weechat

#
#  Author: Enrique Pérez
#  Date: Thu Oct  7 06:07:29 PM CEST 2021
#
#  vim:ts=4:sts=4:sw=4:et
#
#  https://github.com/enriquepablo/dockerfiles
#
# enriquepablo/scilab:6.1.1

FROM archlinux:base-devel-20211010.0.36274

MAINTAINER Enrique Pérez <enrique@cazalla.net>

ARG SCI_USER="sci"
ARG SCI_UID="1000"
ARG SCI_GID="100"
ARG SCI_HOME="/home/sci"

ENV LIBGL_ALWAYS_SOFTWARE=1

USER root

RUN pacman --noconfirm -Sy && \
    pacman --noconfirm -S git vim fakeroot sudo jdk8-openjdk libxft libxtst \
                          binutils xorg-mkfontscale xorg-font-util \
                          extra/xorg-fonts-100dpi extra/xorg-fonts-75dpi extra/xorg-fonts-encodings \
                          extra/xorg-fonts-misc extra/xorg-fonts-type1 community/ttf-junicode extra/freetype2 \
                          extra/gnu-free-fonts community/opendesktop-fonts gtk2 gtkglext texlive-core && \
    pacman --noconfirm -Scc

RUN fc-cache && mkfontscale && mkfontdir

RUN useradd -l -m -s /bin/bash -G wheel -N -u "${SCI_UID}" "${SCI_USER}"

RUN echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER "${SCI_USER}"
WORKDIR "${SCI_HOME}"

RUN gpg --recv-key 702353E0F7E48EDB

RUN git clone https://aur.archlinux.org/ncurses5-compat-libs.git && \
    cd ncurses5-compat-libs && \
    makepkg --noconfirm -si && \
    cd .. && rm -rf ncurses5-compat-libs

RUN git clone https://aur.archlinux.org/scilab-bin.git && \
    cd scilab-bin && \
    makepkg --noconfirm -si && \
    cd .. && rm -rf scilab-bin

# Configure environment
ENV SCI_USER="${SCI_USER}" \
    SCI_UID=${SCI_UID} \
    SCI_GID=${SCI_GID} \
    SCI_HOME=${SCI_HOME} \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

CMD ["scilab"]

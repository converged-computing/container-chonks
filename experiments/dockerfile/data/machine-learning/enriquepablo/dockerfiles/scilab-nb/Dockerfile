#
#  Author: Enrique Pérez
#  Date: Thu Oct  7 06:07:29 PM CEST 2021
#
#  vim:ts=4:sts=4:sw=4:et
#
#  https://github.com/enriquepablo/dockerfiles
#
# enriquepablo/scilab-nb:6.1.1

FROM enriquepablo/scilab:6.1.1

MAINTAINER Enrique Pérez <enrique@cazalla.net>

RUN sudo pacman --noconfirm -Sy && \
    sudo pacman --noconfirm -S jupyterlab extra/xorg-server-xvfb firefox && \
    sudo pacman --noconfirm -Scc

RUN git clone https://aur.archlinux.org/jupyter-metakernel.git && \
    cd jupyter-metakernel && \
    makepkg --noconfirm -si && \
    cd .. && rm -rf jupyter-metakernel

RUN git clone https://aur.archlinux.org/jupyter-scilab_kernel-git.git && \
    cd jupyter-scilab_kernel-git && \
    makepkg --noconfirm -si && \
    cd .. && rm -rf jupyter-scilab_kernel-git

RUN mkdir nb

CMD ["xvfb-run", "--auto-servernum", "jupyter", "lab", "-y", "--ip", "0.0.0.0", "--notebook-dir", "~/nb/"]

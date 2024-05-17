FROM opensuse/leap:15.2
MAINTAINER Matwey V. Kornilov <matwey.kornilov@gmail.com>

ENV CC gcc-7
ENV CXX g++-7


RUN zypper -n ar -p 1 'https://download.opensuse.org/repositories/devel:/gcc/openSUSE_Leap_15.2/devel:gcc.repo'
RUN zypper -n ar -p 1 'https://download.opensuse.org/repositories/KDE:/Qt:/6.0/openSUSE_Leap_15.2/KDE:Qt:6.0.repo'


RUN zypper -n --gpg-auto-import-keys install --no-recommends --auto-agree-with-licenses --force-resolution gcc7-c++ qt6-widgets-devel qt6-test-devel qt6-gui-devel qt6-core-devel qt6-openglwidgets-devel qt6-opengl-devel qt6-base-devel cmake make git tar

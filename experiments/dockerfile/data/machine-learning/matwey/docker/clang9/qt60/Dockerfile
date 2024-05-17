FROM opensuse/leap:15.2
MAINTAINER Matwey V. Kornilov <matwey.kornilov@gmail.com>

ENV CC clang
ENV CXX clang++


RUN zypper -n ar -p 1 'https://download.opensuse.org/repositories/devel:/tools:/compiler/openSUSE_Leap_15.2/devel:tools:compiler.repo'
RUN zypper -n ar -p 1 'https://download.opensuse.org/repositories/KDE:/Qt:/6.0/openSUSE_Leap_15.2/KDE:Qt:6.0.repo'


RUN zypper -n --gpg-auto-import-keys install --no-recommends --auto-agree-with-licenses --force-resolution clang9 qt6-widgets-devel qt6-test-devel qt6-gui-devel qt6-core-devel qt6-openglwidgets-devel qt6-opengl-devel qt6-base-devel cmake make git tar

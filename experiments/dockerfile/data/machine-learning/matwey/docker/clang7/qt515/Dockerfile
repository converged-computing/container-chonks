FROM opensuse/leap:15.2
MAINTAINER Matwey V. Kornilov <matwey.kornilov@gmail.com>

ENV CC clang
ENV CXX clang++


RUN zypper -n ar -p 1 'https://download.opensuse.org/repositories/devel:/tools:/compiler/openSUSE_Leap_15.2/devel:tools:compiler.repo'
RUN zypper -n ar -p 1 'https://download.opensuse.org/repositories/KDE:/Qt:/5.15/openSUSE_Leap_15.2/KDE:Qt:5.15.repo'


RUN zypper -n --gpg-auto-import-keys install --no-recommends --auto-agree-with-licenses --force-resolution clang7 libQt5Widgets-devel libQt5Test-devel libQt5Gui-devel libQt5Core-devel cmake make git tar

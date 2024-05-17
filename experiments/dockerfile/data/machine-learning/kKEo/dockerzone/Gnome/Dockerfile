FROM ubuntu:16.04

RUN apt-get update

RUN apt-get install -y git autoconf autotools-dev gettext yelp-tools cmake

RUN apt-get install -y gettext pkg-config gnome-common

RUN apt-get install sudo apt-file

RUN adduser --disabled-password --ingroup sudo jhbuild 


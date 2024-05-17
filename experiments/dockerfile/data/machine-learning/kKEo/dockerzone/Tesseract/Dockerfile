FROM jitesoft/tesseract-ocr

RUN apt-get update 
RUN apt-get -y upgrade
RUN apt-get -y install imagemagick tesseract-ocr-pol zip unzip vim less
RUN apt-get -y install openssh-server
RUN adduser --disabled-password --gecos '' ocr && echo "ocr:ocr" | chpasswd
RUN apt-get -y install inotify-tools

COPY convert.sh /usr/bin/convert.sh
COPY auto.sh /usr/bin/auto.sh

USER ocr
RUN mkdir /home/ocr/original /home/ocr/output
USER root

ENTRYPOINT service ssh start && sh /usr/bin/auto.sh

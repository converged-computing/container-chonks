FROM ubuntu:14.04
MAINTAINER hnlq.sysu@gmail.com

RUN apt-get update && apt-get install -y wget
RUN wget -O - "http://dl.chenyufei.info/cow/cow-linux64-0.9.4.gz" | gzip -d > /cow
RUN chmod +x /cow; \
    mkdir -p /.cow

ADD rc /.cow/rc 

EXPOSE 8388

CMD /cow

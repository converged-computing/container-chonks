FROM docker-staging.imio.be/base:latest
RUN \
    apt-get -qy update && apt-get -qy install firefox rsync make xvfb gcc python27 python27-virtualenv python27-setuptools libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev git
RUN mkdir /home/imio/cpskin-test && mkdir /home/imio/make-eggs && mkdir /home/imio/.buildout/
WORKDIR /home/imio/.buildout/
RUN wget -qO buildout-cache.tar.bz2 http://files.imio.be/website-buildout-cache.tar.bz2
RUN tar jxvf buildout-cache.tar.bz2 1>/dev/null
RUN rm buildout-cache.tar.bz2
COPY default.cfg /home/imio/.buildout/default.cfg
RUN chown imio:imio -R /home/imio/cpskin-test/ && chown imio:imio -R /home/imio/.buildout &&  chown imio:imio -R /home/imio/make-eggs
WORKDIR /home/imio/make-eggs
USER imio
RUN \
    git clone https://github.com/IMIO/buildout.website.git . &&\
    /opt/python2.7.8/bin/python bootstrap.py -c prod.cfg &&\
    bin/buildout -N -t 7 -c prod.cfg
USER root
RUN rm -rf /home/imio/make-eggs/
USER imio
WORKDIR /home/imio

COPY entrypoint.sh /home/imio/entrypoint.sh
USER root
RUN chmod +x entrypoint.sh && chown imio:imio entrypoint.sh
USER imio
ENTRYPOINT /home/imio/entrypoint.sh

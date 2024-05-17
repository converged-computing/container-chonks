FROM debian:stretch
WORKDIR /home
#RUN apt-get update && apt-get install -y wget libc6-i386 vlc vlc-data vlc-plugin-pulse browser-plugin-vlc mplayer2 && apt-get purge && \
#rm -rf /var/lib/apt/lists/* && apt-get clean

RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y && apt-get install -y curl gzip tar && apt-get purge && rm -rf /var/lib/apt/lists/* && apt-get clean

RUN curl http://simple-help.com/releases/SimpleHelp-linux-amd64.tar.gz | tar -xzv 
RUN useradd -u 40000 simplehelp

WORKDIR /home/SimpleHelp
RUN sed -i 's/&//g' serverstart.sh && chown -R simplehelp /home/SimpleHelp

EXPOSE 8008

USER simplehelp

CMD ["sh", "serverstart.sh"]

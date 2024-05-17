# nginx proxy, confd and s6 on Ubuntu Bionic
FROM markusma/nginx:1.20-ubuntu-bionic-s6

RUN apt-get update \
 && apt-get install -y --no-install-recommends software-properties-common \
 && add-apt-repository ppa:certbot/certbot \
 && apt-get update \
 && apt-get install -y --no-install-recommends certbot \
 && apt-get purge -y --autoremove -o APT::AutoRemove::RecommendsImportant=false software-properties-common \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* $HOME/.cache

#RUN wget https://dl.eff.org/certbot-auto -O /usr/local/bin/certbot-auto \
# && chmod +x /usr/local/bin/certbot-auto \
# && yes | certbot-auto --install-only

COPY etc/ /etc/
COPY bin/ /usr/local/bin/

RUN mkdir -p /var/www/letsencrypt /etc/nginx/conf.d

EXPOSE 80 443

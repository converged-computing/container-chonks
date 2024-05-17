#
# Howto build: docker build -t djdefi/docker-webapp .
# Howto run: docker run [-i] -p 8888:80 -t djdefi/docker-webapp [/bin/bash -i]
# Access via boot2docker: boot2docker ssh -L 8888:localhost:8888
# VERSION 0.0.1

FROM djdefi/docker-webapp-base 
MAINTAINER DJ DeFi <djdefi+github@gmail.com>

#
# Prep web app 
ADD /webapp /app

#
# link app to apache root
RUN rm -fr /var/www && ln -s /app /var/www

# chown app to www-data
RUN chown -R www-data /app

EXPOSE 80

CMD ["/usr/sbin/apache2", "-D", "FOREGROUND"]

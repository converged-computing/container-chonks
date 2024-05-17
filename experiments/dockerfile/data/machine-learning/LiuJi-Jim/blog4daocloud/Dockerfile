FROM luodaoyi/docker-library-nginx-git

RUN mkdir html && cd html
RUN git clone --depth=1 https://github.com/liuji-jim/liuji-jim.github.io.git html
RUN cp -rf html/* /usr/share/nginx/html
RUN rm -rf html
RUN sed -i "s|#gzip  on;|gzip  on; etag  off; server_tokens off; gzip_types *;|" /etc/nginx/nginx.conf
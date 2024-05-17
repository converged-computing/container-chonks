FROM zooniverse/nginx:1.20

RUN mkdir -p /nginx-cache/  &&  touch /etc/nginx-deny.conf

ADD nginx.conf /etc/nginx/nginx.conf
ADD nginx-redirects.conf /etc/nginx/redirects.conf
ADD nginx-proxy.conf /etc/nginx/proxy.conf
ADD nginx-proxy-security-headers.conf /etc/nginx/proxy-security-headers.conf
ADD nginx-fem-redirects.conf /etc/nginx/fem-redirects.conf
ADD nginx-fem-staging-redirects.conf /etc/nginx/fem-staging-redirects.conf
ADD nginx-s3-proxy-headers.conf /etc/nginx/s3-proxy-headers.conf
ADD nginx-az-proxy-headers.conf /etc/nginx/az-proxy-headers.conf
ADD sites/ /etc/nginx/sites/

FROM fedora

MAINTAINER Johan Swensson <kupo at kupo dot se>

RUN dnf install deltarpm yum-utils -y && dnf update -y && dnf install httpd -y && dnf clean all
ADD index.html /var/www/html/index.html
RUN sed -i 's/Listen 80/Listen 8080/' /etc/httpd/conf/httpd.conf && chmod -R a+rwx /run/httpd /etc/httpd/logs
EXPOSE 8080
ENTRYPOINT ["/usr/sbin/httpd"]
CMD ["-D", "FOREGROUND"]


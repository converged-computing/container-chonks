FROM registry.access.redhat.com/rhel7/rhel-atomic

RUN microdnf --enablerepo=rhel-7-server-rpms \
install httpd --nodocs ;\
microdnf clean all ;\
sed -i 's/Listen 80/Listen 8080/' /etc/httpd/conf/httpd.conf && chmod -R a+rwx /run/httpd /etc/httpd/logs 

EXPOSE 8080

ENTRYPOINT ["/usr/sbin/httpd"]
CMD ["-D", "FOREGROUND"]


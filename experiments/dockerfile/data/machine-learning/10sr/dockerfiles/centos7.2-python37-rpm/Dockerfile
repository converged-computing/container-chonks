FROM centos:7.2.1511

ARG PYTHON_VERSION=3.7.7

RUN echo 'skip_missing_names_on_install=False' >>/etc/yum.conf

RUN yum install -y rpmdevtools tar wget && \
        yum install -y glibc-devel bzip2-devel expat-devel openssl-devel readline-devel sqlite-devel zlib-devel && \
        yum install -y  libffi-devel && \
        yum groupinstall -y "Development Tools" && \
        yum clean all && rm -rf /var/cache/yum

WORKDIR /root

RUN rpmdev-setuptree
RUN wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz -O /root/rpmbuild/SOURCES/Python-$PYTHON_VERSION.tgz

WORKDIR /root/rpmbuild/SPECS/
COPY python37.spec .
RUN rpmbuild -bb --clean python37.spec

RUN file /root/rpmbuild/RPMS/x86_64/Python37-$PYTHON_VERSION-10sr.el7.centos.x86_64.rpm

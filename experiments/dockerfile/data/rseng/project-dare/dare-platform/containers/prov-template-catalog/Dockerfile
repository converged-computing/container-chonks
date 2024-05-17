FROM centos:7

MAINTAINER KNMI R&D Observations and Data Technology Department

USER root

RUN yum update -y && yum install -y epel-release deltarpm && yum update -y

RUN yum install -y git python-devel python2-pip npm httpd openssl mod_ssl mod_wsgi graphviz && \
    yum clean all && rm -rf /var/cache/yum

RUN pip install flask && \
    pip install flask-jwt-simple && \
    pip install flask-API && \
    pip install authomatic && \
    pip install pymongo && \
    pip install python-openid && \
    pip install pyOpenSSL && \
    pip install prov && \
    pip install pydot && \
    pip install requests

WORKDIR /

## For no copy from local (already checked out) repository instead of
## cloning a git repository, so we have the latest development edits,
## instead of only what has been pushed to master. On the other, hand
## the local copy will not work in a k8s deployment.
RUN git clone https://github.com/EnvriPlus-PROV/ProvTemplateCatalog.git /tmp/ProvTemplateCatalog

RUN npm install -g webpack && npm install axios

RUN mkdir -p /var/www/repoConf /data/

WORKDIR /tmp/ProvTemplateCatalog/templates
RUN npm install && npm install --save vue

## Copy the application code and compile it.
RUN npm run build

## Copy static content
RUN cp --recursive --dereference /tmp/ProvTemplateCatalog/static /var/www/repoConf
RUN mkdir /var/www/repoConf/templates &&\
    cp /tmp/ProvTemplateCatalog/templates/index.html /var/www/repoConf/templates &&\
    cp /tmp/ProvTemplateCatalog/example_wsgi_conf.conf /var/www/repoConf/repoConf.wsgi &&\
    cp /tmp/ProvTemplateCatalog/app.py /var/www/repoConf/ &&\
    cp /tmp/ProvTemplateCatalog/example_config.py /var/www/repoConf/config.py 

WORKDIR /data/
RUN git clone https://github.com/EnvriPlus-PROV/EnvriProvTemplates.git
WORKDIR /data/EnvriProvTemplates
RUN python setup.py install

WORKDIR /

RUN touch /var/www/repoConf/out.log &&\
    chown apache.apache /var/www/repoConf/out.log &&\
    chmod 600 /var/www/repoConf/out.log

EXPOSE 80
EXPOSE 443
ENV FLASK_ENV=development

CMD ["/tmp/ProvTemplateCatalog/docker-cmd.sh"]
# CMD ["python", "/var/www/repoConf/app.py"]


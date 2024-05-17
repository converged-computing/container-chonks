FROM alpine:edge
LABEL maintainer "William L Anderson <band@acm.org>"

ENV WORKBENCH_PACKAGES bash curl git jq sqlite

RUN apk add --update --no-cache $WORKBENCH_PACKAGES && \
    rm -fr /var/cache/apk/*

# install Tool1 (jq) data file
COPY nyt.json /usr/local/opt/dsatcl/nyt.json

# install Tool2: json2csv (convert JSON to CSV)
RUN cd /tmp && \
    curl -L https://github.com/jehiah/json2csv/releases/download/v.1.2.0/json2csv-1.2.0.linux-amd64.go1.8.tar.gz | tar -zx && \
    cp -v /tmp/json2csv-1.2.0.linux-amd64.go1.8/json2csv /usr/local/bin

# install Tool3 (csvkit) and python modules req'd by Tool3 (scrape)
RUN apk add --update --no-cache python \
    python-dev \
    py-pip \
    build-base \
    libxml2-dev \
    libxslt-dev && \
    pip install --upgrade pip && \
    pip install csvkit && \
    pip install lxml && \
    pip install cssselect && \
    rm -fr /var/cache/apk/*

# install Tool4 (scrape), Tool6 (sample), Tool7 (Rio) (from JJ's tool set)
RUN cd /tmp && \
    git clone https://github.com/jeroenjanssens/data-science-at-the-command-line.git && \
    cd /tmp/data-science-at-the-command-line/tools && cp -v scrape sample Rio /usr/local/bin

# install Tool5 (xml2json)
RUN apk add --update --no-cache nodejs nodejs-npm && \
	npm install npm@latest -g && \
	npm install -g xml2json-command

# install Tool7 (Rio) - depends on R and R packages
RUN apk add --update --no-cache R R-dev && \
    R -e "install.packages('dplyr',repos='http://cran.revolutionanalytics.com')" && \
    R -e "install.packages('tidyr',repos='http://cran.revolutionanalytics.com')" && \
    R -e "install.packages('sqldf',repos='http://cran.revolutionanalytics.com')" && \
    R -e  "install.packages('ggplot2',repos='http://cran.revolutionanalytics.com')" && \
    apk del R-dev && \
    rm -fr /var/cache/apk/*

CMD ["/bin/bash"]

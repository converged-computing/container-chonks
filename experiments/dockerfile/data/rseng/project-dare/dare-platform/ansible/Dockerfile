FROM alpine

COPY 3d/kubespray/requirements.txt .

RUN set -ex \
     && apk add --no-cache py-pip build-base python-dev libffi-dev openssl-dev \
     && pip install --upgrade pip \
     && pip install -r requirements.txt \
     && mkdir /ansible \
     && apk del build-base py-pip libffi-dev openssl-dev

WORKDIR /ansible
 
ENTRYPOINT ["ansible-playbook"]

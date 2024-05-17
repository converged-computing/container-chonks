FROM ubuntu:16.04

RUN apt update \
    && DEBIAN_FRONTEND=noninteractive apt -y --no-install-recommends install phpldapadmin slapd ldap-utils \
    && rm -rf /var/lib/apt/lists

COPY init.sh /usr/bin/init.sh

CMD ["init.sh"]

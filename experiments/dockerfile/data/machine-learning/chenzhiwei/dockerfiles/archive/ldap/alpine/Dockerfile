FROM alpine:3.6

RUN apk add --no-cache openldap openldap-clients

COPY slapd.init.ldif /tmp/slapd.init.ldif

COPY ldap.sh /usr/bin/ldap.sh

CMD ["ldap.sh"]

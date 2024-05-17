# Fully configured mail server with SMTP, IMAP and SpamAssassin
#
# The ./etc/passwd, ./etc/shadow, ./etc/aliases contents will be appended to
# the corresponding files in /etc

FROM phusion/baseimage:0.11

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y exim4-daemon-heavy spamassassin sa-exim procmail
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y dovecot-imapd
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y sasl2-bin

## exim4 configuration
COPY mailname /etc/mailname
COPY exim4 /etc/exim4
# Enable spamassassin
RUN sed -i '1ilocal_scan_path = /usr/lib/exim4/local_scan/sa-exim.so\n' /etc/exim4/exim4.conf.template
RUN sed -i 's/^SAEximRunCond: 0$/#SAEximRunCond: 0/' /etc/exim4/sa-exim.conf
# Enable TLS
RUN sed -i '1iMAIN_TLS_ENABLE = yes\nMAIN_TLS_PRIVATEKEY = /etc/exim4/mail.key\nMAIN_TLS_CERTIFICATE = /etc/exim4/mail.pem\n' /etc/exim4/exim4.conf.template
RUN usermod -a -G ssl-cert Debian-exim
# Enable port 465
RUN sed -i 's/SMTPLISTENEROPTIONS=.*/SMTPLISTENEROPTIONS='"'"'-oX 465:25'"'"'/' /etc/default/exim4
RUN sed -i '/\.ifdef MAIN_TLS_ENABLE/atls_on_connect_ports=465' /etc/exim4/exim4.conf.template
# Enable authentication
RUN echo 'plain_saslauthd_server:\n  driver = plaintext\n  public_name = PLAIN\n  server_condition = ${if saslauthd{{$auth2}{$auth3}}{1}{0}}\n  server_set_id = $auth2\n  server_prompts = :\n  .ifndef AUTH_SERVER_ALLOW_NOTLS_PASSWORDS\n  server_advertise_condition = ${if eq{$tls_cipher}{}{}{*}}\n  .endif' >>/etc/exim4/exim4.conf.template
RUN usermod -a -G sasl Debian-exim
RUN update-exim4.conf

## Dovecot configuration
# use mbox format
RUN sed -i 's/^#mail_access_groups =.*/mail_access_groups = mail/' /etc/dovecot/conf.d/10-mail.conf
RUN sed -i 's/^#mail_location =.*/mail_location = mbox:~\/mail:INBOX=\/var\/mail\/%u/' /etc/dovecot/conf.d/10-mail.conf
# require SSL for all connections
RUN sed -i 's/^ssl =.*/ssl = required/' /etc/dovecot/conf.d/10-ssl.conf
RUN sed -i 's/^ssl_cert =.*/ssl_cert = <\/etc\/ssl\/certs\/mail.pem/' /etc/dovecot/conf.d/10-ssl.conf
RUN sed -i 's/^ssl_key =.*/ssl_key = <\/etc\/ssl\/private\/mail.key/' /etc/dovecot/conf.d/10-ssl.conf
RUN sed -i 's/^#log_path =.*/log_path = \/dev\/stderr/' /etc/dovecot/conf.d/10-logging.conf
# add run directory
RUN mkdir /var/run/dovecot
RUN chown dovecot /var/run/dovecot

## SpamAssassin user
RUN useradd -r -m -d /var/lib/spamd -c 'SpamAssassin Daemon' spamd

## Add runit scripts
RUN mkdir /etc/service/saslauthd
COPY service/saslauthd.sh /etc/service/saslauthd/run
RUN chmod +x /etc/service/saslauthd/run

RUN mkdir /etc/service/exim4
COPY service/exim4.sh /etc/service/exim4/run
RUN chmod +x /etc/service/exim4/run

RUN mkdir /etc/service/spamd
COPY service/spamd.sh /etc/service/spamd/run
RUN chmod +x /etc/service/spamd/run

RUN mkdir /etc/service/dovecot
COPY service/dovecot.sh /etc/service/dovecot/run
RUN chmod +x /etc/service/dovecot/run

RUN mkdir /var/log/runit

## SSL certificates
COPY ssl/mail.key /etc/ssl/private/mail.key
RUN chmod 0440 /etc/ssl/private/mail.key
COPY ssl/mail.pem /etc/ssl/certs/mail.pem
RUN chmod 0444 /etc/ssl/certs/mail.pem
RUN chown root.ssl-cert /etc/ssl/private/mail.key /etc/ssl/certs/mail.pem

# For some reason Exim refuses to read the certificates from /etc/ssl (TODO: check this is still the case)
RUN cp /etc/ssl/private/mail.key /etc/exim4/
RUN cp /etc/ssl/certs/mail.pem /etc/exim4/
RUN chgrp ssl-cert /etc/exim4/mail.key /etc/exim4/mail.pem

## Users
COPY users /root/users
RUN cat /root/users/passwd >> /etc/passwd
RUN cat /root/users/shadow >> /etc/shadow
RUN cat /root/users/group >> /etc/group
RUN cat /root/users/aliases >> /etc/aliases
RUN rm -rf /root/users

# smtp, smtps, imap, imaps
EXPOSE 25 465 143 993

CMD ["/sbin/my_init"]

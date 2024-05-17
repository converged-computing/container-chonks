FROM wnameless/oracle-xe-11g

EXPOSE 1521 8080

RUN echo "connect / as sysdba \n\
create tablespace USER_tabspace datafile 'USER_tabspace.dat' size 100M autoextend on; \n\
create temporary tablespace USER_tabspace_temp tempfile 'USER_tabspace_temp.dat' size 50M autoextend on; \n\
create user USER identified by password default tablespace USER_tabspace temporary tablespace USER_tabspace_temp; \n\
grant create session to USER; \n\
grant create table to USER; \n\
grant create sequence to USER; \n\
grant unlimited tablespace to USER; \n\
exit" > /tmp/initDb.sql

RUN echo "export ORACLE_HOME=/u01/app/oracle/product/11.2.0/xe" >> /tmp/initDb.sh \
 && echo "export PATH=\$ORACLE_HOME/bin:\$PATH" >> /tmp/initDb.sh \
 && echo "export ORACLE_SID=XE" >>  /tmp/initDb.sh \
 && echo "cat /tmp/initDb.sql | sqlplus /nolog" >> /tmp/initDb.sh \
 && chown oracle:dba /tmp/initDb.sh

CMD /usr/sbin/startup.sh && su -c "sh /tmp/initDb.sh" oracle && /usr/sbin/sshd -D

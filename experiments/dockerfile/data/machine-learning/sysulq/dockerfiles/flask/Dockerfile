FROM ubuntu:12.04

RUN apt-get update
RUN apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
RUN apt-get install -y python
RUN apt-get install -y python-dev
RUN apt-get install -y python-pip
RUN pip install flask
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD app.py /home/app.py
RUN chmod +x /home/app.py
EXPOSE 5000
CMD python /home/app.py

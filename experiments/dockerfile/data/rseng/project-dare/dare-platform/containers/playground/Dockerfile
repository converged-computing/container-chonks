FROM nginx

RUN apt-get update && apt-get install -y build-essential supervisor unzip uwsgi python3 python3-pip python3-setuptools procps vim git curl
RUN apt-get install -y openmpi-bin=3.1.3-11 libopenmpi-dev=3.1.3-11 python3-venv wget

ENV USER mpiuser
ENV HOME /home/mpiuser/docker

RUN adduser ${USER} --disabled-password --gecos ""

USER ${USER}
WORKDIR ${HOME}

USER root
RUN groupadd appusers
RUN usermod -a -G appusers ${USER}
RUN usermod -a -G appusers nginx
RUN chgrp -R appusers /home/mpiuser
RUN chmod -R 777 /home/mpiuser

# dispel4py
RUN git clone https://gitlab.com/project-dare/dispel4py.git && \
    cd dispel4py && python3 setup.py install

# icclim
RUN git clone https://github.com/cerfacs-globc/icclim && cd icclim && \
    gcc -fPIC -g -c -Wall ./icclim/libC.c -o ./icclim/libC.o && \
    gcc -shared -o ./icclim/libC.so ./icclim/libC.o && \
    python3 setup.py install
RUN python3 -m pip install netcdf4 cython
RUN python3 -m pip install netcdftime
RUN rm -rf icclim

ENV HOME=/opt/repo
ARG RELEASE=v1.1

RUN git clone --branch $RELEASE --single-branch https://gitlab.com/project-dare/playground.git ./playground
RUN python3 -m pip install -r ./playground/requirements.txt

RUN mkdir ${HOME}/src
RUN cp ./playground/app/* ${HOME}/src
RUN cp ./playground/scripts/* /home/mpiuser/docker
RUN rm -rf ./playground

# Copy the configuration file from the current directory and paste
# it inside the container to use it as Nginx's default config.
COPY ./nginx.conf /etc/nginx/nginx.conf

# setup NGINX config
RUN mkdir -p /spool/nginx /run/pid && \
    chmod -R 777 /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    chgrp -R 0 /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    chmod -R g+rwX /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    rm /etc/nginx/conf.d/default.conf

# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY ./uwsgi.ini /etc/uwsgi/apps-available/uwsgi.ini
RUN ln -s /etc/uwsgi/apps-available/uwsgi.ini /etc/uwsgi/apps-enabled/uwsgi.ini

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN touch /var/log/supervisor/supervisord.log

EXPOSE 81:81

# setup entrypoint
COPY ./docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN rm /docker-entrypoint.sh

# https://github.com/moby/moby/issues/31243#issuecomment-406879017
RUN ln -s /usr/local/bin/docker-entrypoint.sh / && \
    chmod 777 /usr/local/bin/docker-entrypoint.sh && \
    chgrp -R 0 /usr/local/bin/docker-entrypoint.sh && \
    chown -R nginx:root /usr/local/bin/docker-entrypoint.sh

# https://docs.openshift.com/container-platform/3.3/creating_images/guidelines.html
RUN chgrp -R 0 /var/log /var/cache /run/pid /spool/nginx /var/run /run /tmp /etc/uwsgi /etc/nginx && \
    chmod -R g+rwX /var/log /var/cache /run/pid /spool/nginx /var/run /run /tmp /etc/uwsgi /etc/nginx && \
    chown -R nginx:root ${HOME} && \
    chmod -R 777 ${HOME} /etc/passwd

# enter
WORKDIR ${HOME}
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["supervisord"]

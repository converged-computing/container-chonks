FROM jupyterhub/jupyterhub:latest
LABEL maintainer="Yaron Rosenbaum"

# Install pip3 install notebook
RUN pip3 install --no-cache-dir notebook jupyterlab ray

# add default users and passwords
RUN useradd -ms /bin/bash yaron
RUN echo 'yaron:iamyaron' | chpasswd

RUN useradd -ms /bin/bash mike
RUN echo 'yaron:iammike' | chpasswd

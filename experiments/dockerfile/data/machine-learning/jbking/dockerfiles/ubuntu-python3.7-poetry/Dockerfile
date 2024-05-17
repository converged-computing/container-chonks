FROM jbking/ubuntu-dev:20191019-1420

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
 python3.7 \
 python3-distutils \
 python3-setuptools \
 python3.7-venv \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3.7
RUN echo export PATH="$HOME/.poetry/bin:$PATH" >> "$HOME/.bashrc"
RUN sed -i s/python/python3.7/ ~/.poetry/bin/poetry

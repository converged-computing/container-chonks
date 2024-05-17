FROM jbking/ubuntu-tox-with-deadsnakes:05-Dec-18

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
 python3.5 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN /venv/bin/pip install docutils

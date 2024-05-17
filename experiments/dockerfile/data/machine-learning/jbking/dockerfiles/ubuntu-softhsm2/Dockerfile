FROM ubuntu:18.10

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
 softhsm2 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

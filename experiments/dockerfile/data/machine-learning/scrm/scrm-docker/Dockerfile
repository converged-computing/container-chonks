FROM alpine
MAINTAINER Paul Staab <develop (at) paulstaab.de>

# Download scrm's as static binary
ADD https://github.com/scrm/scrm/releases/download/v1.7.3/scrm-x64-static /usr/local/bin/scrm
RUN chmod +x /usr/local/bin/scrm

# Create a non-privileged user to run scrm
RUN adduser -S scrm
USER scrm
WORKDIR /home/scrm

# Run scrm by default
ENTRYPOINT ["/usr/local/bin/scrm"]

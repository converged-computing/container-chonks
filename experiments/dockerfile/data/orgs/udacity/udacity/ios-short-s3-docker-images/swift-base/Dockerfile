FROM ubuntu:zesty

# Add packages required by Swift and Kitura
RUN echo "deb http://security.ubuntu.com/ubuntu trusty-security main" >> /etc/apt/sources.list
RUN apt-get update; \
        apt-get install -y openssl libcurl3 libicu52 libxml2 libbsd-dev libatomic1; \
        apt-get autoremove -y; \
        rm -rf /var/lib/apt/lists/*

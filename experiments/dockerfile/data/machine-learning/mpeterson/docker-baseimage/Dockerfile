FROM ubuntu:18.04
MAINTAINER mpeterson <docker@peterson.com.ar>

# Change this ENV variable to skip the docker cache from this line on
ENV LATEST_CACHE 2017-04-10T13:00+02:00

# Make APT non-interactive
ENV DEBIAN_FRONTEND noninteractive

# Ensure UTF-8
ENV LANG       en_US.UTF-8
ENV LC_ALL     en_US.UTF-8

# prevent init scripts from running during install/update
#  policy-rc.d (for most scripts)
RUN { \
        echo '#!/bin/sh'; \
        echo 'exit 101'; \
} > /usr/sbin/policy-rc.d
RUN chmod +x /usr/sbin/policy-rc.d
#  initctl (for some pesky upstart scripts)
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -sf /bin/true /sbin/initctl
# see https://github.com/dotcloud/docker/issues/446#issuecomment-16953173

# this forces dpkg not to call sync() after package extraction and speeds up install
RUN echo "force-unsafe-io" > /etc/dpkg/dpkg.cfg.d/02apt-speedup
# # we don't need an apt cache in a container
RUN { \
        aptGetClean='"rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true";'; \
        echo "DPkg::Post-Invoke { ${aptGetClean} };"; \
        echo "APT::Update::Post-Invoke { ${aptGetClean} };"; \
        echo 'Dir::Cache::pkgcache ""; Dir::Cache::srcpkgcache "";'; \
        echo 'Acquire::http {No-Cache=True;};'; \
} > /etc/apt/apt.conf.d/no-cache

# and remove the translations, too
RUN echo 'Acquire::Languages "none";' > /etc/apt/apt.conf.d/no-languages

## Enable Ubuntu Universe and Multiverse.
RUN sed -i 's/^#\s*\(deb.*universe\)$/\1/g' /etc/apt/sources.list
RUN sed -i 's/^#\s*\(deb.*multiverse\)$/\1/g' /etc/apt/sources.list

# Upgrade the system to the latest version
RUN apt-get update
RUN apt-get dist-upgrade -y --no-install-recommends

# Install packages needed for this image
RUN apt-get install -y --no-install-recommends apt-transport-https ca-certificates software-properties-common locales

# Enforce UTF-8 workaround for locale-gen missing from newer ubuntu images
RUN locale-gen --purge en_US.UTF-8

# This after the package installation so we can use the docker cache
RUN mkdir /build
ADD . /build

# Starting the installation of this particular image

# Often used tools
RUN apt-get install -y --no-install-recommends curl less vim psmisc

# End of particularities of this image

# Give the possibility to override any file on the system
RUN cp -R /build/overrides/. / || :

# Clean everything up
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /build

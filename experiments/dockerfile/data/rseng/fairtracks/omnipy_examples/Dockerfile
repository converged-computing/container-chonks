FROM prefecthq/prefect:2.13-python3.10-kubernetes

RUN pip install omnipy_examples
RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
            locales; \
            apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
	        rm -rf /var/lib/apt/lists/*;
RUN set -eux; \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen; \
    echo "de_DE.UTF-8 UTF-8" >> /etc/locale.gen; \
    locale-gen; \
    update-locale en_us.UTF-8;
RUN ln -sf /usr/local/lib/python3.10/site-packages /opt/prefect/src

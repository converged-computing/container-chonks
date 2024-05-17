FROM google/cloud-sdk:287.0.0-alpine@sha256:9cbf1749c0ef2a1335fb10ba83bb9567af3388aecb323d0a5f7a8bd912b825fb

# use with -e CLOUDSDK_CORE_PROJECT=...,

RUN apk --no-cache add openjdk8-jre && \
    gcloud components install cloud-datastore-emulator beta --quiet

EXPOSE 8081

HEALTHCHECK --interval=3s --timeout=1s --retries=10 \
    CMD curl --fail http://localhost:8081

CMD ["gcloud", "beta", "emulators", "datastore", "start", "--host-port=0.0.0.0:8081"]

FROM google/cloud-sdk:287.0.0@sha256:007ad7eb0489222bb5084c1bedb22da660e59afa4f0a9377c617624c565f3aaa

# use with -e CLOUDSDK_CORE_PROJECT=...,

EXPOSE 8081

HEALTHCHECK --interval=3s --timeout=1s --retries=10 \
    CMD curl --fail http://localhost:8081

CMD ["gcloud", "beta", "emulators", "datastore", "start", "--host-port=0.0.0.0:8081"]

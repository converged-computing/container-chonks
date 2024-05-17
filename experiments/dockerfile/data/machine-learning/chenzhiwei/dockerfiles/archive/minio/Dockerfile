FROM minio/mc as mc

FROM minio/minio

COPY --from=mc /usr/bin/mc /usr/bin/mc

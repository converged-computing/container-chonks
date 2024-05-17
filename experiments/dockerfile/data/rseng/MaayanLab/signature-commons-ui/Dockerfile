FROM nginx:1.12-alpine

COPY ./entrypoint.sh /entrypoint.sh
RUN set -x && chmod +x /entrypoint.sh

COPY ./out /sigcom

EXPOSE 80

ENV PREFIX=/sigcom
ENV NEXT_PUBLIC_METADATA_API=/metadata-api
ENV NEXT_PUBLIC_DATA_API=/data-api
ENV NEXT_PUBLIC_ENRICHR_URL=https://maayanlab.cloud/Enrichr

ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["nginx", "-g", "daemon off;"]

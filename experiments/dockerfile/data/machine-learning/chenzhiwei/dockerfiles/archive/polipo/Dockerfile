FROM alpine:3.8 as builder

RUN apk add --no-cache gcc libc-dev make openssl \
    && wget https://github.com/jech/polipo/archive/polipo-1.1.1.tar.gz \
    && tar xf polipo-1.1.1.tar.gz \
    && cd polipo-polipo-1.1.1 \
    && make

FROM alpine:3.8

COPY --from=builder /polipo-polipo-1.1.1/polipo /usr/local/bin/polipo

EXPOSE 8123
ENTRYPOINT ["polipo"]
CMD ["proxyAddress=0.0.0.0", "dnsNameServer=8.8.8.8"]

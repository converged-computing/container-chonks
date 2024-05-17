FROM alpine:3.8

RUN apk add --no-cache python py-pip libsodium \
    && pip install https://github.com/shadowsocks/shadowsocks/archive/2.9.1.tar.gz

ENTRYPOINT ["ssserver"]

CMD ["-p", "8388", "-k", "123456", "-m", "aes-256-cfb"]

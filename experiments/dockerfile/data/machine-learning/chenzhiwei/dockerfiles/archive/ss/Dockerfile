FROM alpine as builder

RUN apk add --no-cache binutils curl jq

RUN SS_VERSION=$(curl -s  https://api.github.com/repos/shadowsocks/shadowsocks-rust/releases/latest | jq -r .name) \
    && curl -sLO https://github.com/shadowsocks/shadowsocks-rust/releases/download/${SS_VERSION}/shadowsocks-${SS_VERSION}.x86_64-unknown-linux-musl.tar.xz \
    && tar xf shadowsocks-${SS_VERSION}.x86_64-unknown-linux-musl.tar.xz \
    && strip ss* || true

RUN V2RAY_PLUGIN_VERSION=$(curl -s https://api.github.com/repos/shadowsocks/v2ray-plugin/releases/latest | jq -r .name) \
    && curl -sLO https://github.com/shadowsocks/v2ray-plugin/releases/download/${V2RAY_PLUGIN_VERSION}/v2ray-plugin-linux-amd64-${V2RAY_PLUGIN_VERSION}.tar.gz \
    && tar xf v2ray-plugin-linux-amd64-${V2RAY_PLUGIN_VERSION}.tar.gz

FROM alpine

COPY --from=builder ss* /usr/bin/
COPY --from=builder v2ray-plugin_linux_amd64 /usr/bin/v2ray-plugin

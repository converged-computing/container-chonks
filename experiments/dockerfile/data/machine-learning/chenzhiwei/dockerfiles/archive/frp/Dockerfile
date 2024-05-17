FROM alpine as builder

RUN apk add --no-cache jq

RUN FRP_VERSION=$(wget -q -O - https://api.github.com/repos/fatedier/frp/releases/latest | jq -r .name | sed 's/v//g') \
    && wget -q https://github.com/fatedier/frp/releases/download/v${FRP_VERSION}/frp_${FRP_VERSION}_linux_amd64.tar.gz \
    && tar --strip-components=1 -xf frp_${FRP_VERSION}_linux_amd64.tar.gz -C /tmp

FROM alpine

ENV FRPS_BIND_PORT=11700 \
    FRPS_TOKEN=frp \
    FRPS_ALLOW_PORTS=11000-11010,11022

ENV FRPC_SERVER_ADDR=127.0.0.1 \
    FRPC_SERVER_PORT=11700 \
    FRPC_TOKEN=frp \
    FRPC_SSH_REMOTE_PORT=11022 \
    FRPC_SSH_USE_ENCRYPTION=false \
    FRPC_SSH_USE_COMPRESSION=true

COPY --from=builder /tmp/frpc /tmp/frps /usr/bin/
COPY frpc.ini frps.ini /etc/frp/

CMD ["frpc", "-c", "/etc/frp/frpc.ini"]

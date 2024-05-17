from alpine

MAINTAINER Dan Sheffner <Dan@Sheffner.com>
# since alpine does not have gnu lib instead uses musl
# CGO_ENABLED=0 go build -a -installsuffix cgo

COPY ./alpine_go_webserver /root/alpine_go_webserver
CMD ["/root/alpine_go_webserver"]

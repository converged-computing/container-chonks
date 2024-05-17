FROM golang:1.17 as builder

COPY server.go /server.go

RUN CGO_ENABLED=0 GOOS=linux go build -o /server /server.go && strip /server

FROM scratch

COPY --from=builder /server /server

USER 65535:65535
EXPOSE 8080

CMD ["/server"]

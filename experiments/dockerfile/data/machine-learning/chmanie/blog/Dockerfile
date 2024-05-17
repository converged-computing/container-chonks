FROM ghcr.io/getzola/zola:v0.17.2 AS builder

WORKDIR /app
COPY . .
RUN ["zola", "build"]

FROM docker.io/svenstaro/miniserve
COPY --from=builder /app/public /public
EXPOSE 8080

ENTRYPOINT ["/app/miniserve", "/public/", "--index", "index.html"]

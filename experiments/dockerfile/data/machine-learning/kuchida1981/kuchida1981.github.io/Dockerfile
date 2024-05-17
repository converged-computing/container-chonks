FROM debian:bullseye
ARG HUGO_VERSION=0.111.3
ARG ARCH=arm64
ENV TZ "Asia/Tokyo"
RUN apt-get update && apt-get install -y curl
RUN curl -L -O https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-${ARCH}.deb
RUN dpkg -i hugo_extended_${HUGO_VERSION}_linux-${ARCH}.deb
EXPOSE 1313
ENTRYPOINT ["hugo"]
CMD ["server", "--bind", "0.0.0.0", "-D"]

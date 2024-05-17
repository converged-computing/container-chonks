ARG GOLANG_IMAGE_TAG=1.21
ARG AZTERRAFORM_TAG=latest
FROM mcr.microsoft.com/oss/go/microsoft/golang:${GOLANG_IMAGE_TAG} as build
COPY .. /src
WORKDIR /src

RUN ls -a && export CGO_ENABLED=0 && \
    go install avm-gh-app

FROM mcr.microsoft.com/azterraform:${AZTERRAFORM_TAG} as runner
COPY --from=build /go/bin /usr/local/go/bin
WORKDIR /app

ENTRYPOINT ["avm-gh-app"]
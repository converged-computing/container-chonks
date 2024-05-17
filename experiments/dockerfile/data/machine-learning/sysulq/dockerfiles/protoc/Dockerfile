FROM alpine:3.8 as protoc_builder
RUN apk add --no-cache build-base curl automake autoconf libtool git zlib-dev

ENV GRPC_VERSION=1.16.0 \
        GRPC_JAVA_VERSION=1.16.1 \
        GRPC_WEB_VERSION=1.0.0 \
        PROTOBUF_VERSION=3.6.1 \
        PROTOBUF_C_VERSION=1.3.1 \
        PROTOC_GEN_DOC_VERSION=1.1.0 \
        OUTDIR=/out
RUN mkdir -p /protobuf && \
        curl -L https://github.com/google/protobuf/archive/v${PROTOBUF_VERSION}.tar.gz | tar xvz --strip-components=1 -C /protobuf
RUN git clone --depth 1 --recursive -b v${GRPC_VERSION} https://github.com/grpc/grpc.git /grpc && \
        rm -rf grpc/third_party/protobuf && \
        ln -s /protobuf /grpc/third_party/protobuf
RUN mkdir -p /grpc-java && \
        curl -L https://github.com/grpc/grpc-java/archive/v${GRPC_JAVA_VERSION}.tar.gz | tar xvz --strip-components=1 -C /grpc-java
RUN mkdir -p /grpc-web && \
        curl -L https://github.com/grpc/grpc-web/archive/${GRPC_WEB_VERSION}.tar.gz | tar xvz --strip-components=1 -C /grpc-web
RUN mkdir -p /protobuf-c && \
        curl -L https://github.com/protobuf-c/protobuf-c/releases/download/v${PROTOBUF_C_VERSION}/protobuf-c-${PROTOBUF_C_VERSION}.tar.gz | tar xvz --strip-components=1 -C /protobuf-c
RUN cd /protobuf && \
        autoreconf -f -i -Wall,no-obsolete && \
        ./configure --prefix=/usr --enable-static=no && \
        make -j2 && make install
RUN cd grpc && \
        make -j2 plugins
RUN cd /grpc-java/compiler/src/java_plugin/cpp && \
        g++ \
        -I. -I/protobuf/src \
        *.cpp \
        -L/protobuf/src/.libs \
        -lprotoc -lprotobuf -lpthread --std=c++0x -s \
        -o protoc-gen-grpc-java
RUN cd /protobuf-c && \
        ./configure --prefix=/usr && \
        make -j2
RUN cd /protobuf && \
        make install DESTDIR=${OUTDIR}
RUN cd /grpc && \
        make install-plugins prefix=${OUTDIR}/usr
RUN cd /grpc-java/compiler/src/java_plugin/cpp && \
        install -c protoc-gen-grpc-java ${OUTDIR}/usr/bin/
RUN cd /grpc-web/javascript/net/grpc/web && \
        make && \
        install protoc-gen-grpc-web ${OUTDIR}/usr/bin/
RUN cd /protobuf-c && \
        make install DESTDIR=${OUTDIR}
RUN find ${OUTDIR} -name "*.a" -delete -or -name "*.la" -delete

RUN apk add --no-cache go
ENV GOPATH=/go \
        PATH=/go/bin/:$PATH
RUN go get -u -v -ldflags '-w -s' \
        github.com/Masterminds/glide \
        github.com/golang/protobuf/protoc-gen-go \
        github.com/gogo/protobuf/protoc-gen-gofast \
        github.com/gogo/protobuf/protoc-gen-gogo \
        github.com/gogo/protobuf/protoc-gen-gogofast \
        github.com/gogo/protobuf/protoc-gen-gogofaster \
        github.com/gogo/protobuf/protoc-gen-gogoslick \
        github.com/twitchtv/twirp/protoc-gen-twirp \
        github.com/chrusty/protoc-gen-jsonschema \
        github.com/grpc-ecosystem/grpc-gateway/protoc-gen-swagger \
        github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway \
        github.com/johanbrandhorst/protobuf/protoc-gen-gopherjs \
        github.com/ckaznocha/protoc-gen-lint \
        github.com/mwitkow/go-proto-validators/protoc-gen-govalidators \
        github.com/lyft/protoc-gen-validate \
        moul.io/protoc-gen-gotemplate \
        github.com/micro/protoc-gen-micro \
        && (cd ${GOPATH}/src/github.com/lyft/protoc-gen-validate && make build) \
        && install -c ${GOPATH}/bin/protoc-gen* ${OUTDIR}/usr/bin/

RUN mkdir -p ${GOPATH}/src/github.com/pseudomuto/protoc-gen-doc && \
        curl -L https://github.com/pseudomuto/protoc-gen-doc/archive/v${PROTOC_GEN_DOC_VERSION}.tar.gz | tar xvz --strip 1 -C ${GOPATH}/src/github.com/pseudomuto/protoc-gen-doc
RUN cd ${GOPATH}/src/github.com/pseudomuto/protoc-gen-doc && \
        make build && \
        install -c ${GOPATH}/src/github.com/pseudomuto/protoc-gen-doc/protoc-gen-doc ${OUTDIR}/usr/bin/

FROM znly/upx as packer
COPY --from=protoc_builder /out/ /out/
RUN upx --lzma \
        /out/usr/bin/protoc \
        /out/usr/bin/grpc_* \
        /out/usr/bin/protoc-gen-*

FROM alpine:3.7
RUN apk add --no-cache libstdc++
COPY --from=packer /out/ /

RUN apk add --no-cache curl && \
        mkdir -p /protobuf/google/protobuf && \
        for f in any duration descriptor empty struct timestamp wrappers; do \
        curl -L -o /protobuf/google/protobuf/${f}.proto https://raw.githubusercontent.com/google/protobuf/master/src/google/protobuf/${f}.proto; \
        done && \
        mkdir -p /protobuf/google/api && \
        for f in annotations http; do \
        curl -L -o /protobuf/google/api/${f}.proto https://raw.githubusercontent.com/grpc-ecosystem/grpc-gateway/master/third_party/googleapis/google/api/${f}.proto; \
        done && \
        mkdir -p /protobuf/github.com/gogo/protobuf/gogoproto && \
        curl -L -o /protobuf/github.com/gogo/protobuf/gogoproto/gogo.proto https://raw.githubusercontent.com/gogo/protobuf/master/gogoproto/gogo.proto && \
        mkdir -p /protobuf/github.com/mwitkow/go-proto-validators && \
        curl -L -o /protobuf/github.com/mwitkow/go-proto-validators/validator.proto https://raw.githubusercontent.com/mwitkow/go-proto-validators/master/validator.proto && \
        mkdir -p /protobuf/github.com/lyft/protoc-gen-validate/gogoproto && \
        mkdir -p /protobuf/github.com/lyft/protoc-gen-validate/validate && \
        curl -L -o /protobuf/github.com/lyft/protoc-gen-validate/gogoproto/gogo.proto https://raw.githubusercontent.com/lyft/protoc-gen-validate/master/gogoproto/gogo.proto && \
        curl -L -o /protobuf/github.com/lyft/protoc-gen-validate/validate/validate.proto https://raw.githubusercontent.com/lyft/protoc-gen-validate/master/validate/validate.proto && \
        apk del curl && \
        chmod a+x /usr/bin/protoc

ENTRYPOINT ["/usr/bin/protoc", "-I/protobuf"]
# Prefer debian over ubuntu
FROM debian:wheezy
# Let's install go just like Docker (from source).
RUN apt-get update -q
RUN apt-get install -qy build-essential curl git mercurial bzr
RUN curl -s https://go.googlecode.com/files/go1.2.src.tar.gz | tar -v -C /usr/local -xz
RUN cd /usr/local/go/src && ./make.bash --no-clean 2>&1
ENV PATH /usr/local/go/bin:/go/bin:$PATH
ENV GOPATH /go
# we're using godep to save / restore dependancies
RUN go get code.google.com/p/gorest
RUN go get github.com/carabasdaniel/go-rest-test
WORKDIR /go
EXPOSE 4050
CMD go run $GOPATH/src/github.com/carabasdaniel/go-rest-test/main.go
FROM alpine:latest

# 安装GCC
RUN apk --no-cache add gcc musl-dev

# 将hello.c复制到容器中
COPY hello.c .

# 编译C程序
RUN gcc -o hello hello.c

# 运行C程序
CMD ["./hello"]

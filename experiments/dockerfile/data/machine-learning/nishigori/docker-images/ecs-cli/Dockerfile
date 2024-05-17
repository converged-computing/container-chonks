FROM centos:7

# https://github.com/aws/amazon-ecs-cli/releases
ENV ECS_CLI_VERSION v1.6.0

RUN set -x \
  && curl -o /usr/local/bin/ecs-cli https://s3.amazonaws.com/amazon-ecs-cli/ecs-cli-linux-amd64-${ECS_CLI_VERSION} \
  && echo "$(curl -s https://s3.amazonaws.com/amazon-ecs-cli/ecs-cli-linux-amd64-${ECS_CLI_VERSION}.md5) /usr/local/bin/ecs-cli" | md5sum -c - | grep OK \
  && chmod +x /usr/local/bin/ecs-cli \
  && /usr/local/bin/ecs-cli --version

ENTRYPOINT ["/usr/local/bin/ecs-cli"]
CMD ["--version"]

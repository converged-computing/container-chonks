FROM python:3.6-alpine

# https://pypi.python.org/pypi/ecs-deploy/
ENV ECS_DEPLOY_VER 1.4.3

RUN set -x \
  && apk upgrade --no-cache \
  && pip install --no-cache-dir ecs-deploy==$ECS_DEPLOY_VER

ENTRYPOINT ["ecs", "deploy"]
CMD ["--help"]

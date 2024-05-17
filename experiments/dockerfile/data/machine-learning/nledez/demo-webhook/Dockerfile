# syntax=docker/dockerfile:1.3
FROM python:3.11 as builder

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VIRTUALENVS_CREATE=true \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_VERSION=1.6.1

RUN pip install -U pip &&\
    pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /tmp/

RUN mv /tmp/poetry.lock /tmp/pyproject.toml ./ &&\
    poetry install --without=tests --no-interaction --no-ansi &&\
    rm poetry.lock pyproject.toml

FROM python:3.11

WORKDIR /app
COPY entrypoint.sh /entrypoint.sh
COPY sandbox/ /app/sandbox/
COPY --from=builder /app/.venv /app/.venv

RUN chmod +x /entrypoint.sh &&\
    find /app/sandbox -name __pycache__ | xargs rm -rf

USER nobody
EXPOSE 8000
CMD ["/entrypoint.sh"]

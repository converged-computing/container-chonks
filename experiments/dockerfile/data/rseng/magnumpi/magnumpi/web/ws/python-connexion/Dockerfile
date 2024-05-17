FROM python:3.9-buster

WORKDIR  /src

COPY pymagnumpi/dist /src/pymagnumpi/dist
COPY web/ws/python-connexion /src/web/ws/python-connexion
COPY input /src/input

RUN cd /src/pymagnumpi/dist && pip install ./magnumpi-*-cp39-cp39-linux_x86_64.whl && cd /src/web/ws/python-connexion && pip install .

ENV CELERY_BROKER_URL=redis://redis:6379
ENV CELERY_RESULT_BACKEND=redis://redis:6379
ENV MAGNUMPI_INPUTDATA_DIR=/src

CMD gunicorn -w 4 -b 0.0.0.0:8888 magnumpi_webservice.serve:app

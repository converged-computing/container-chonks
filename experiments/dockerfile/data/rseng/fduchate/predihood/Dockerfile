# requires option -f for building image independently of the context (mainly to copy mongiris/)
FROM python:3
WORKDIR /code/
# to avoid downloading all python packages again, only ADD (not copy) requirements and do pip install -r first
ADD ./predihood/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./mongiris/ /code/mongiris/
RUN cd /code/mongiris/ && python3 -m pip install .
COPY ./predihood/ /code/predihood/
EXPOSE 27017
EXPOSE 8081
#ENV FLASK_APP=predihood/main.py
#ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONPATH "${PYTHONPATH}:/code/predihood/"
CMD cd ./predihood/predihood/ && python3 main.py
#COPY run-predihood.sh /docker-entrypoint-initdb.d/run-predihood.sh # ne se passe rien :/

# pull official base image
FROM continuumio/miniconda3:latest

# set work directory
WORKDIR /usr/www/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN conda install numpy
RUN conda install -c conda-forge spglib

# create gims user
RUN mkdir -p /home/gims
RUN addgroup --system gims && adduser --system --group gims

# create the appropriate directories
ENV HOME=/home/gims
ENV APP_HOME=/home/gims/app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# copy and install project
COPY . $APP_HOME
RUN pip install --no-cache $APP_HOME[prod]
RUN chown -R gims:gims $APP_HOME

# change to the gims user
USER gims

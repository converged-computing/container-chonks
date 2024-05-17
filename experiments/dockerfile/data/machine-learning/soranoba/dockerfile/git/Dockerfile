# git @ Ubuntu12.10
#
# $ docker build -t soranoba/git .

FROM ubuntu:12.10
MAINTAINER Hinagiku Soranoba <soranoba@gmail.com>

# default update
RUN apt-get update

# install git
RUN apt-get install -y git

# copy ssh key
ADD .ssh /root/.ssh
ADD .gitconfig /.gitconfig

# bash-completion
RUN apt-get install -y bash-completion
ADD bashrc __bashrc
RUN cat __bashrc >> ~/.bashrc
RUN rm __bashrc

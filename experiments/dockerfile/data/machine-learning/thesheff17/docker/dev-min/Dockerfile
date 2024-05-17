FROM ubuntu:16.04

MAINTAINER Dan Sheffner <Dan@Sheffner.com>

# use tmuxinator through a ruby gem because tmux doesn't work
# very well in docker containers.  If you know the fix let me know

# helper ENV variables
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

ENV EDITOR vim
ENV SHELL bash

# build date
RUN echo `date` > /root/build_date.txt

# local.sources.list is a local mirror
# public.sources.list is a public mirror
# use whatever you have
# COPY ./public.sources.list /etc/apt/sources.list
COPY ./local.sources.list /etc/apt/sources.list

# apt-get
RUN \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -yq curl wget git python3-pip python3-dev \ 
    build-essential gcc vim lsb-release mysql-client zsh \
    libpq-dev libjpeg-dev ffmpeg tmux screen cmake htop \
    net-tools inetutils-ping apt-utils libssl-dev \
    libmemcached-dev python-dev python-pip man && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# gem install 
# RUN gem install tmuxinator

# pip upgrades
RUN pip3 install --upgrade pip && pip2 install --upgrade pip


# virtualenv 
RUN pip2 install virtualenvwrapper virtualenv && \
    cd /root/ && \
    /bin/bash -c "source /usr/local/bin/virtualenvwrapper.sh && \
    mkvirtualenv --python=/usr/bin/python3 venv" && \
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> /root/.bashrc 

# these files get messed up for some reason
RUN \
    echo "#!/bin/bash" > /root/.virtualenvs/preactivate && \
    echo "# This hook is run before every virtualenv is activated." >> /root/.virtualenvs/preactivate && \
    echo "# argument: environment name " >> /root/.virtualenvs/preactivate && \
    echo "#!/bin/bash" > /root/.virtualenvs/venv/bin/preactivate && \
    echo "# This hook is run before this virtualenv is activated." >> /root/.virtualenvs/venv/bin/preactivate

# python3 pip 
RUN \
   /bin/bash -c " source /root/.virtualenvs/venv/bin/activate && \
   pip3 install boto3 django django-environ django-secure whitenoise \
    django-braces django-crispy-forms django-floppyforms django-model-utils \
    pillow django-allauth psycopg2 unicode-slugify django-autoslug pytz django-redis \
    redis pymysql libsass django-compressor django-sass-processor django-debug-toolbar \
    django_extensions django-nose django-axes python-dateutil pyflakes coverage sphinx \
    werkzeug django-test-plus factory_boy ipdb sqlalchemy bpython"

# flask
RUN /bin/bash -c " source /root/.virtualenvs/venv/bin/activate && \
    pip3 install flask flask-bcrypt flask-login flask-migrate flask-sqlalchemy flask-script \
    flask-testing flask-wtf mako markupsafe wtforms alembic gunicorn itsdangerous py-bcrypt "
 
# go
RUN wget --quiet https://storage.googleapis.com/golang/go1.8.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go1.8.linux-amd64.tar.gz
RUN echo 'export PATH=$PATH:/usr/local/go/bin' >> /root/.bashrc
RUN echo 'export GOBIN=/root/go/bin' >> /root/.bashrc
RUN echo 'export GOPATH=/root/go/bin' >> /root/.bashrc 
RUN rm go1.8.linux-amd64.tar.gz

# vim modules
RUN mkdir -p /root/.vim/autoload /root/.vim/bundle /root/.vim/colors/ /root/.vim/ftplugin/
RUN curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
WORKDIR /root/.vim/bundle/
RUN git clone https://github.com/tpope/vim-sensible.git
RUN git clone https://github.com/ctrlpvim/ctrlp.vim.git

# project died
# RUN git clone https://github.com/kien/ctrlp.vim.git
RUN git clone https://github.com/scrooloose/nerdtree
RUN git clone https://github.com/Lokaltog/vim-powerline.git
RUN git clone https://github.com/jistr/vim-nerdtree-tabs.git
RUN git clone https://github.com/python-mode/python-mode.git
# RUN git clone --recursive https://github.com/davidhalter/jedi-vim.git
RUN git clone https://github.com/fatih/vim-go.git 
RUN git clone https://github.com/vim-syntastic/syntastic.git

WORKDIR /root/.vim/colors/ 
RUN wget https://raw.githubusercontent.com/thesheff17/youtube/master/vim/wombat256mod.vim
WORKDIR /root/.vim/ftplugin/
RUN wget https://raw.githubusercontent.com/thesheff17/youtube/master/vim/python_editing.vim
WORKDIR /root/
RUN wget https://raw.githubusercontent.com/thesheff17/youtube/master/vim/vimrc2
RUN mv vimrc2 .vimrc 

# go packages
RUN export PATH=$PATH:/usr/local/go/bin && \
    export GOPATH=/root/go/bin && \
    export GOBIN=/root/go/bin && \
    go get github.com/nsf/gocode && \
    go get github.com/alecthomas/gometalinter && \
    go get golang.org/x/tools/cmd/goimports && \
    go get golang.org/x/tools/cmd/guru && \
    go get golang.org/x/tools/cmd/gorename && \
    go get github.com/golang/lint/golint && \
    go get github.com/rogpeppe/godef && \
    go get github.com/kisielk/errcheck && \
    go get github.com/jstemmer/gotags && \
    go get github.com/klauspost/asmfmt/cmd/asmfmt && \ 
    go get github.com/fatih/motion && \
    go get github.com/zmb3/gogetdoc && \
    go get github.com/josharian/impl

# tmux setup
# ADD tmuxinator /root/.tmuxinator
RUN echo 'set-option -g default-shell /bin/bash' > /root/.tmux.conf

# a bunch of attempts that failed.  Something causes +GoInstallBinaries to prompt for enter or u.  I see -- more -- 
# Let me know if you have a patch for this.
# RUN mkdir /root/go
# ENV HOME /root
# ENV GOPATH /usr/local/go
# ENV PATH $PATH:$GOPATH/bin
# ENV GOROOT=/root/go
# RUN vim +PluginInstall  +qall
# RUN vim +GoInstallBinaries +qall
# RUN vim +PluginInstall +GoInstallBinaries +qall

# RUN mkdir -p /root/go/bin
# RUN export GOBIN=/root/go/bin && export GOPATH=/root/go/bin && export PATH=$PATH:/usr/local/go/bin && set nomore | go run /root/.vim/bundle/
# RUN export GOBIN=/root/go/bin && export GOPATH=/root/go/bin && export PATH=$PATH:/usr/local/go/bin && echo "\n"| vim +GoInstallBinaries +qall 
#

# create a shared file structure
RUN mkdir -p /root/git/

# Copy over samples
COPY ./webserver.go /root/bin/
COPY ./webserver.py /root/bin/

# put back public mirror
COPY ./public.sources.list /etc/apt/sources.list

# gem tmux no longer used
# CMD ["/usr/local/bin/tmuxinator", "start", "default"]

# CMD ["/bin/bash"]

WORKDIR /root/
CMD ["/usr/bin/tmux"]

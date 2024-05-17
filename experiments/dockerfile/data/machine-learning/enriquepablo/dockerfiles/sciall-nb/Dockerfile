#
#  Author: Enrique Pérez
#  Date: Thu Oct  7 06:07:29 PM CEST 2021
#
#  vim:ts=4:sts=4:sw=4:et
#
#  https://github.com/enriquepablo/dockerfiles
#
# enriquepablo/sciall-nb:1.0.0

FROM enriquepablo/scilab-nb:6.1.1

MAINTAINER Enrique Pérez <enrique@cazalla.net>

ENV SCI_HOME /home/sci

RUN sudo pacman --noconfirm -Sy && \
    sudo pacman --noconfirm -S python-pandas python-patsy python-scipy python-matplotlib \
                               python-sympy r python-pandas-datareader python-numexpr python-bottleneck \
                               python-beautifulsoup4 python-lxml python-tabulate python-olefile gnuplot rlwrap \
                               gcc-fortran python-lxml python-yaml python-cairo jupyter-jsmol nodejs npm maxima \
                               spyder python-spyder-kernels julia && \
    sudo pacman --noconfirm -Scc

RUN sudo R -e "install.packages(c('repr', 'IRdisplay', 'IRkernel'), type = 'source', repos = 'http://cran.us.r-project.org')"
RUN R -e "IRkernel::installspec()"

RUN sudo jupyter labextension install @techrah/text-shortcuts
RUN sudo jupyter labextension install @jupyter-widgets/jupyterlab-manager

RUN git clone https://github.com/robert-dodier/maxima-jupyter.git

WORKDIR "${SCI_HOME}"/maxima-jupyter

RUN curl -kLO https://beta.quicklisp.org/quicklisp.lisp && \
    sbcl --non-interactive --load quicklisp.lisp \
      --eval "(quicklisp-quickstart:install)" \
      --eval "(ql-util:without-prompting (ql:add-to-init-file))"    

RUN export PYTHON_SITE=$(python -c 'import site; print(site.getsitepackages()[0])') && \
    sudo cp maxima_lexer.py ${PYTHON_SITE}/pygments/lexers/

ENV JUPYTERLAB_DIR=/usr/share/jupyter/lab

RUN sudo mkdir -p ${JUPYTERLAB_DIR}/staging/node_modules/codemirror/mode/maxima/ && \
    sudo cp maxima.js ${JUPYTERLAB_DIR}/staging/node_modules/codemirror/mode/maxima/ && \
    sudo patch ${JUPYTERLAB_DIR}/staging/node_modules/codemirror/mode/meta.js codemirror-mode-meta-patch && \
    sudo jupyter lab build && \
    maxima --batch-string="load(\"load-maxima-jupyter.lisp\");jupyter_install();"

RUN julia -e "using Pkg; Pkg.add(\"IJulia\")"

WORKDIR "${SCI_HOME}"

FROM jupyter/minimal-notebook

# Enable git extension, nbgitpuller and toc
RUN pip install --no-cache-dir nbgitpuller && \
jupyter serverextension enable --py nbgitpuller --sys-prefix && \
jupyter labextension install @jupyterlab/git && \
pip install jupyterlab-git && \
jupyter serverextension enable --py jupyterlab_git && \
jupyter labextension install @jupyterlab/toc

ENV NBGITPULLER_APP lab

RUN pip install requests==2.24.0 wget==3.2 PyYAML==5.3.1

USER $NB_UID

# miRGalaxy image

FROM quay.io/bgruening/galaxy:20.09

MAINTAINER Ilias Glogovitis, ilias@uni-plovdiv.bg

# Enable Conda dependency resolution
ENV GALAXY_CONFIG_BRAND="miRGalaxy" \
    GALAXY_CONFIG_CONDA_AUTO_INSTALL=True \
    GALAXY_CONFIG_CONDA_ENSURE_CHANNELS=iuc,conda-forge,bioconda,defaults,viascience,travis

# Install libtbb2 package for bowtie
RUN apt-get update && apt-get install libtbb2 -y

# Install tools
COPY MirGalaxy.yaml $GALAXY_ROOT/tools_0.yaml
COPY NGS_1.yaml $GALAXY_ROOT/tools_1.yaml
COPY NGS_2.yaml $GALAXY_ROOT/tools_2.yaml
COPY NGS_3.yaml $GALAXY_ROOT/tools_3.yaml


# Split into multiple layers
RUN df -h && \
    install-tools $GALAXY_ROOT/tools_0.yaml && \
    /tool_deps/_conda/bin/conda clean --all --yes && \
    rm -rf /tool_deps/_conda/pkgs && \
    df -h

RUN df -h && \ 
    install-tools $GALAXY_ROOT/tools_1.yaml && \
    /tool_deps/_conda/bin/conda clean --all --yes && \
    rm -rf /tool_deps/_conda/pkgs && \
    df -h
    
RUN df -h && \
    install-tools $GALAXY_ROOT/tools_2.yaml && \
    /tool_deps/_conda/bin/conda clean --all --yes && \
    rm -rf /tool_deps/_conda/pkgs && \
    df -h

RUN df -h && \
    install-tools $GALAXY_ROOT/tools_3.yaml && \
    /tool_deps/_conda/bin/conda clean --all --yes && \
    rm -rf /tool_deps/_conda/pkgs && \
    df -h

RUN mkdir -p $GALAXY_ROOT/workflows
COPY mirgalaxy-workflows/* $GALAXY_ROOT/workflows/

COPY create_admin_user.sh $GALAXY_ROOT/create_admin_user.sh

RUN apt-get update && apt-get -y install netcat && apt-get clean
RUN chmod +x $GALAXY_ROOT/create_admin_user.sh

ENV PATH="${PATH}:/tool_deps/_conda/bin"
RUN startup_lite && \
    galaxy-wait && \
    $GALAXY_ROOT/create_admin_user.sh  && \
    workflow-install --publish --workflow_path $GALAXY_ROOT/workflows/ -g http://localhost:8080 -u $GALAXY_DEFAULT_ADMIN_EMAIL -p $GALAXY_DEFAULT_ADMIN_PASSWORD

# Add Container Style
ENV GALAXY_CONFIG_DISPLAY_GALAXY_BRAND="mirGalaxy"
ENV GALAXY_CONFIG_WELCOME_URL=$GALAXY_CONFIG_DIR/web/welcome.html
COPY config/welcome.html $GALAXY_CONFIG_DIR/web/welcome.html
COPY config/welcome-mirgalaxy.png $GALAXY_CONFIG_DIR/web/welcome-mirgalaxy.png

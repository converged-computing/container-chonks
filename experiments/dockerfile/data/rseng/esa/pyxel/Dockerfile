#
# Pyxel with Jupyter notebook server
#
# $ docker build .

# $ docker-compose build

# Use a Docker image with 'mamba' pre-installed
FROM mambaorg/micromamba:1.5.6

# Copy Pyxel source code
RUN mkdir -p pyxel-dev/src
WORKDIR pyxel-dev
COPY --chown=$MAMBA_USER:$MAMBA_USER . src/pyxel

# Install Pyxel
RUN micromamba install --yes -n base --file src/pyxel/continuous_integration/environment.yml && \
    micromamba install --yes -n base -c conda-forge git && \
    micromamba clean --all --yes
ARG MAMBA_DOCKERFILE_ACTIVATE=1  # (otherwise python will not be found)

# Install Pyxel
RUN python -m pip install -e src/pyxel --no-deps
RUN python -c "import pyxel; pyxel.show_versions()"

# Get Pyxel data
RUN git clone --depth 1 --branch master https://gitlab.com/esa/pyxel-data.git pyxel-data

# Expose Jupyter notebook port
EXPOSE 8888
CMD jupyter lab --ip=0.0.0.0 --no-browser --NotebookApp.quit_button=True --notebook-dir=pyxel-data
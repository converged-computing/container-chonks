FROM ubuntu

RUN apt-get update && apt-get install -y \
  --no-install-recommends \
  ca-certificates \
  build-essential \
  qtbase5-dev \
  libqt5svg5-dev \
  libzmq3-dev \
  libdw-dev \
  libgl1-mesa-glx \
  mesa-utils \
  git \
  cmake

RUN useradd -m groot && mkdir /home/groot/trees
USER groot
WORKDIR /home/groot

RUN git clone https://github.com/BehaviorTree/Groot.git && \
      cd Groot && \
      git submodule update --init --recursive && \
      mkdir build; cd build && \
      cmake .. && \
      make && \
      mkdir ~/bin && cp Groot ~/bin

ENTRYPOINT ["bin/Groot"]

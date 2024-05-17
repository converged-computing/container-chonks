FROM          lively-server
MAINTAINER    Robert Krahn <robert.krahn@gmail.com>

USER root

#RUN echo "deb http://us.archive.ubuntu.com/ubuntu/ trusty-updates multiverse" >> /etc/apt/sources.list; \
#    echo "deb-src http://us.archive.ubuntu.com/ubuntu/ trusty-updates multiverse" >> /etc/apt/sources.list;

RUN apt-get update; \
    apt-get upgrade -y; \
    apt-get -y install libopencv-dev build-essential cmake git libgtk2.0-dev pkg-config python-dev python-numpy libdc1394-22 libdc1394-22-dev libjpeg-dev libpng12-dev libtiff4-dev libjasper-dev libavcodec-dev libavformat-dev libswscale-dev libxine-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libv4l-dev libtbb-dev libqt4-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev x264 v4l-utils unzip

RUN mkdir $HOME/opencv; \
    cd $HOME/opencv; \
    wget https://github.com/Itseez/opencv/archive/3.0.0.zip -O opencv-3.0.0.zip; \
    unzip opencv-3.0.0.zip;

RUN cd $HOME/opencv/opencv-3.0.0; \
    mkdir build; \
    cd build; \
    cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_TBB=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D WITH_V4L=ON -D WITH_QT=ON -D WITH_OPENGL=ON -D WITH_IPP=OFF ..; \
    make -j $(nproc); \
    sudo make install;

RUN sudo /bin/bash -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/opencv.conf'; \
    sudo ldconfig;

RUN npm install -g opencv;

RUN chown -R lively:lively /home/lively/.npm

USER lively
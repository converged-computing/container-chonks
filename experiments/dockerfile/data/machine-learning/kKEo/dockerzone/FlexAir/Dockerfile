FROM ubuntu:14.04

RUN apt-get update && apt-get install -y wget 

# INSTALL JDK
RUN cd /opt && wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/7u67-b01/jdk-7u67-linux-x64.tar.gz \
   && tar xzf jdk-7u67-linux-x64.tar.gz \
   && rm jdk-7u67-linux-x64.tar.gz \
   && echo "export JAVA_HOME=/opt/jdk1.7.0_67" >> /etc/profile

# DOWNLOAD 
RUN    wget http://www.eu.apache.org/dist/flex/4.14.0/binaries/apache-flex-sdk-4.14.0-bin.tar.gz -O /opt/apache-flex-sdk-4.14.0-bin.tar.gz \
    && cd /opt && tar xzf apache-flex-sdk-4.14.0-bin.tar.gz \
    && rm apache-flex-sdk-4.14.0-bin.tar.gz \
    && echo "export FLEX_HOME=/opt/apache-flex-sdk-4.14.0-bin" >> /etc/profile

ENV PATH /opt/jdk1.7.0_67/bin:$PATH 

RUN mkdir /opt/adobe-air-2.6 && cd /opt/adobe-air-2.6 \
  && wget http://airdownload.adobe.com/air/lin/download/2.6/AdobeAIRSDK.tbz2 \
  && tar jxf AdobeAIRSDK.tbz2 \
  && rm AdobeAIRSDK.tbz2

#INSTALL GRADLE
RUN   apt-get install -y python-software-properties \
   && apt-get install -y software-properties-common \
   && add-apt-repository -y ppa:cwchien/gradle \
   && apt-get update \
   && apt-get install -y gradle

RUN apt-get install -y git curl unzip

RUN cd /home && git clone https://github.com/Gamua/Starling-Framework.git

ENV AIR_HOME /opt/adobe-air-2.6

ENV FLEX_HOME /opt/apache-flex-sdk-4.14.0-bin

RUN   mkdir -p /opt/playerglobal/14.0 && cd /opt/playerglobal/14.0 \
   && wget http://fpdownload.macromedia.com/get/flashplayer/installers/archive/playerglobal/playerglobal14_0.swc -O playerglobal.swc 
   
ENV PLAYERGLOBAL_HOME /opt/playerglobal

RUN curl -LO http://downloads.sourceforge.net/project/osmf.adobe/OSMF%202.0%20Release%20%28final%20source%2C%20ASDocs%2C%20pdf%20guides%20and%20release%20notes%29/OSMF.swc \
   && mv OSMF.swc $FLEX_HOME/frameworks/libs/osmf.swc

RUN cd /home && wget https://swfobject.googlecode.com/files/swfobject_2_2.zip \
  && unzip swfobject_2_2.zip \
  && rm swfobject_2_2.zip

RUN apt-get install -y vim 

RUN echo -e "<body> \n\
<script src=\"http://ajax.googleapis.com/ajax/libs/swfobject/2.2/swfobject.js\" type=\"text/javascript\"></script> \n\
<script type=\"text/javascript\"> \n\
(function() { \n\
    var flashvars = {}, \n\
    params = {wmode:\"direct\"}, \n\
    attributes = {}; \n\
    swfobject.embedSWF(\"demo_web.swf\", \"placeholder\", \"800\", \"600\", "9.0.0", \"/swf/expressInstall.swf\", flashvars, params, attributes); \n\
})(); \n\
</script> \n\
<div id=\"placeholder\"></div> \n\
</body>" > /home/embedded.html

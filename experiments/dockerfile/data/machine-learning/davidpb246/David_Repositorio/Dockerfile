FROM ibmcom/websphere-traditional:8.5.5.22
EXPOSE 9443
EXPOSE 9043
EXPOSE 7777

ENV TZ=America/Costa_Rica
ENV HOME=/home/was

USER root

RUN dnf --disableplugin=subscription-manager install -y maven git \
    && /opt/IBM/WebSphere/AppServer/bin/manageprofiles.sh -create -profileName Appsrv01 -profilePath /opt/IBM/WebSphere/AppServer/V85/ND/profile_cmd/appsrv -profileTemplate \
    && /opt/IBM/WebSphere/AppServer/V85/ND/profileTemplates/default/ -cell cell02 -node node02 -hostName agente2


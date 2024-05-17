FROM openjdk:8-jre-alpine as build

RUN apk --update --no-cache add zip maven wget && \
     wget https://gitlab.com/project-dare/s-ProvFlow/-/archive/1.2.7/s-ProvFlow-1.2.7.zip && \
     unzip s-ProvFlow-1.2.7.zip && \
     find ./s-ProvFlow-1.2.7 -type f -name "*.log" | xargs -I {} rm -f {} && \
     find ./s-ProvFlow-1.2.7 -type f -name "*.pyc" | xargs -I {} rm -f {} && \
     cd ./s-ProvFlow-1.2.7/sprovflow-viewer && \
     mvn compile war:war

FROM tomcat:9-jre8-alpine

COPY --from=build /s-ProvFlow-1.2.7/sprovflow-viewer/target/sprovflow-viewer.war /usr/local/tomcat/webapps/

## We cannot rely on tomcat to unpack the war file, because this will mess up
## the config map mounts in the k8s deployment spec in sprov-view-dp.yaml.
RUN mkdir -p /usr/local/tomcat/webapps/sprovflow-viewer && cd /usr/local/tomcat/webapps/sprovflow-viewer && unzip ../sprovflow-viewer.war

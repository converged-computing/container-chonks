FROM maven:3-jdk-8-alpine as build

RUN apk add --no-cache --virtual .dep git && \
    git clone https://gitlab.com/project-dare/data-catalogue.git && \
    cd data-catalogue && \
    mvn clean package && \
    apk del .dep

FROM tomcat:9-jre8-alpine

COPY --from=build data-catalogue/target/virtuoso-linker.war /usr/local/tomcat/webapps/

EXPOSE 8080

CMD ["catalina.sh", "run"]

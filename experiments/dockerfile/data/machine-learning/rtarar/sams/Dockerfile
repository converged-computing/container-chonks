# build stage
FROM maven:3-jdk-8 as builder
RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN mvn clean package -DskipTests=true

# create Image stage
FROM openjdk:8-jre-alpine
RUN apk --no-cache add curl
COPY --from=builder /usr/src/app/target/hl7-incident-processor*.jar hl7-incident-processor.jar

RUN sh -c 'touch ./hl7-incident-processor.jar'
ENTRYPOINT ["java","-jar","./hl7-incident-processor.jar"]

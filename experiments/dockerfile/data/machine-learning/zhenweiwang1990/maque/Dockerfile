FROM java:8-jdk as builder

WORKDIR /app
ADD . .
RUN ./mvnw package

##########################

FROM builder as prod

WORKDIR /app
COPY --from=builder /app/ /app/
EXPOSE 8080
CMD ["java","-jar","target/spring-petclinic-2.1.0.BUILD-SNAPSHOT.jar"]

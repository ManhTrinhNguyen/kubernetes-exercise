FROM openjdk:17.0.2-jdk
EXPOSE 8080
RUN mkdir /opt/app
COPY build/libs/bootcamp-kubernetes-exercise-project-1.0-SNAPSHOT.jar /opt/app/java-app.jar
WORKDIR /opt/app
CMD ["java", "-jar", "java-app.jar"]
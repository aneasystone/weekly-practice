FROM ghcr.io/graalvm/native-image-community:21 AS builder

WORKDIR /build
COPY . /build
RUN ./mvnw --no-transfer-progress package -DskipTests=true

FROM ghcr.io/graalvm/jdk-community:21

EXPOSE 8080
COPY --from=builder /build/target/hello-0.0.1-SNAPSHOT.jar app.jar
CMD ["java","-jar","app.jar"]

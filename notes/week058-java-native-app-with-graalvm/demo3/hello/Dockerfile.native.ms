FROM ghcr.io/graalvm/native-image-community:21 AS builder

WORKDIR /build
COPY . /build
RUN ./mvnw --no-transfer-progress native:compile -Pnative -DskipTests=true

FROM almalinux:9

EXPOSE 8080
COPY --from=builder /build/target/hello app
ENTRYPOINT ["/app"]
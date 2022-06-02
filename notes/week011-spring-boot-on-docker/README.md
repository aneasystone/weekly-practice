# WEEK011 - 在 Docker 环境中开发 Spring Boot 项目

在 WEEK009 中，有一篇关于 Docker 的 [Getting Started Guide](../week009-spring-guides/guides/gs/spring-boot-docker/README.md)，在那篇教程中我们已经学习了如何编写 Dockerfile 将 Spring Boot 应用构建成 Docker 镜像。在这篇教程中，我们将继续使用之前的那个 Spring Boot 应用，并学习一些更深入的知识。

## 一个简单的 Dockerfile

我们还是先从一个简单的 Dockerfile 开始：

```
FROM openjdk:17-jdk-alpine
ARG JAR_FILE
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

在这里我们定义了一个 `JAR_FILE` 变量，在 `docker build` 构建镜像时，通过 `--build-arg` 参数来指定 jar 文件的位置，这是为了创建一个适用于 Maven 和 Gradle 的通用 Dockerfile，因为 Maven 和 Gradle 构建出来的 jar 文件位置是不一样的。如果我们使用的是 Maven，使用下面的命令构建镜像：

```
# docker build --build-arg JAR_FILE=target/*.jar -t myorg/myapp .
```

如果我们使用的是 Gradle，则使用下面的命令构建镜像：

```
# docker build --build-arg JAR_FILE=build/libs/*.jar -t myorg/myapp .
```

如果我们的项目已经明确了是 Maven 项目，可以去掉 `JAR_FILE` 变量，简化 Dockerfile：

```
FROM openjdk:17-jdk-alpine
COPY target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

然后直接使用下面的命令构建镜像：

```
# docker build -t myorg/myapp .
```

使用 `docker run` 运行镜像：

```
# docker run -p 8080:8080 myorg/myapp
```

如果想看看打出来的镜像里面的内容具体是什么，可以通过 `--entrypoint` 参数将容器的入口命令修改为 `/bin/sh`： 

```
# docker run -ti --entrypoint /bin/sh myorg/myapp
```

这样就可以在 shell 终端中做一些我们想做的事，这在排查问题时非常有用，比如查看镜像里的文件：

```
/ # ls
app.jar  dev      home     media    proc     run      srv      tmp      var
bin      etc      lib      mnt      root     sbin     sys      usr
```

如果是一个已经在运行中的容器，我们可以通过 `docker exec` 来挂接：

```
docker exec -ti <container-id> /bin/sh
/ #
```

其中 `<container-id>` 可以是容器的 ID 或名称，可以通过 `docker ps` 查看。

### Entry Point

### 更小的镜像

## 使用分层优化 Dockerfile

## 一些优化技巧

## 多阶段构建（Multi-Stage Build）

## 安全性

## 构建插件

## 持续集成

## Buildpacks

## Knative

## 参考

1. [Spring Boot Docker](https://spring.io/guides/topicals/spring-boot-docker/)

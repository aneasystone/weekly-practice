# 在 Docker 环境中开发 Spring Boot 项目

这篇教程介绍了如何构建一个 Docker 镜像来运行 Spring Boot 应用，我们首先创建一个基础的 Dockerfile 文件，然后试着做一些调整，最后还会介绍使用 Maven 插件来代替 `docker` 命令构建镜像。

开始教程之前，确保你的机器上已经安装了 Docker。

## 使用 Spring Initializr 创建一个项目

访问 [start.spring.io](https://start.spring.io/)，创建一个 Spring Boot 项目，或者直接访问这个链接（[pre-initialized project](https://start.spring.io/#!type=maven-project&language=java&platformVersion=2.7.0&packaging=jar&jvmVersion=11&groupId=com.example&artifactId=demo&name=demo&description=Demo%20project%20for%20Spring%20Boot&packageName=com.example.demo&dependencies=web)），点击 Generate 按钮下载项目初始代码。

## 设置 Spring Boot 应用

刚创建的项目入口类如下所示：

```
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }

}
```

此时我们可以直接 `mvn package` 将代码打成 jar 包并运行，不过这个应用现在还看不到什么用处。所以我们决定为其加一个 Web 首页：

```
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class DemoApplication {

  @RequestMapping("/")
  public String home() {
    return "Hello Docker World";
  }

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }

}
```

我们在 `Application` 类中添加一个 `home()` 方法，通过 `@RestController` 和 `@RequestMapping("/")` 将这个方法设置成 Web 首页。

打包并运行：

```
$ mvn clean package && java -jar .\target\demo-0.0.1-SNAPSHOT.jar
```

访问首页：

```
$ curl http://localhost:8080
Hello Docker World
```

## 构建第一个镜像

在项目根目录创建一个 Dockerfile 文件：

```
FROM openjdk:17-jdk-alpine
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
```

然后运行如下的 `docker build` 命令：

```
# docker build -t springio/gs-spring-boot-docker .
```

这是一个非常简单的 Dockerfile，其中使用了 4 个指令：

* `FROM`：指定 `openjdk:17-jdk-alpine` 为基础镜像，基础镜像中包含了程序运行所需的环境；需要注意的是，本地编译打包所使用的 Java 版本最好和基础镜像中的版本一致，譬如我本地使用的是 JDK 17，基础镜像使用 JDK 8，运行时就会报错：

```
Exception in thread "main" java.lang.UnsupportedClassVersionError: com/example/demo/DemoApplication has been compiled by a more recent version of the Java Runtime (class file version 55.0), this version of the Java Runtime only recognizes class file versions up to 52.0
```

* `ARG`：定义一个 JAR_FILE 参数，可以在构建镜像时通过 `--build-arg` 设置参数值，譬如你如果是 Gradle 项目，打包后的 jar 文件在 build/libs 目录，而不是 target 目录，你就可以这样构建镜像：`docker build --build-arg JAR_FILE=build/libs/\*.jar -t springio/gs-spring-boot-docker .`；
* `COPY`：将 jar 文件拷贝到镜像中；
* `ENTRYPOINT`：指定容器启动后需要执行的命令。

通过上面的命令，我们构建了一个名为 `springio/gs-spring-boot-docker` 的镜像，可以通过下面的 `docker run` 命令运行它：

```
# docker run -p 8080:8080 springio/gs-spring-boot-docker
```

## 指定用户

从运行日志中，可以看到默认情况下，Docker 容器中的程序是以 root 用户运行的（started by root）：

```
2022-05-25 00:00:41.598  INFO 1 --- [           main] com.example.demo.DemoApplication         : Starting DemoApplication v0.0.1-SNAPSHOT using Java 17-ea on 0d5422937dda with PID 1 (/app.jar started by root in /)
```

使用 root 运行程序存在一定的安全风险，最好的做法是创建一个普通用户来运行容器中的程序，我们创建一个新的 Dockerfile_rootless 文件：

```
FROM openjdk:17-jdk-alpine
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
```

我们新增了两个指令：

* `RUN`：在构建 Docker 镜像时执行的命令，执行结果是内置在镜像中的。在这里我们使用了 `addgroup` 添加了一个用户组 spring，并使用 `adduser` 将用户 spring 添加到该用户组；
* `USER`：指定了容器中的程序以 spring 用户来运行。

重新构建镜像并运行：

```
> docker build -t springio/gs-spring-boot-docker -f Dockerfile_rootless .
> docker run -p 8080:8080 springio/gs-spring-boot-docker
...
2022-05-25 00:11:51.096  INFO 1 --- [           main] com.example.demo.DemoApplication         : Starting DemoApplication v0.0.1-SNAPSHOT using Java 17-ea on 0e49a18ea22f with PID 1 (/app.jar started by spring in /)
...
```

从启动日志可以看出，程序是以 spring 用户运行的。

## 镜像分层

我们知道 Docker 的镜像是分层存储的，在 Dockerfile 中的每一行指令都会生成一个新的分层，在构建和运行时，相同的分层会通过缓存提高性能。在上面的 Dockerfile 中，我们通过 `COPY ${JAR_FILE} app.jar` 将打包后的 jar 文件拷贝到镜像中，这样会生成一个新的分层，而这个分层的大小取决于你这个 jar 文件的大小，一般来说 Spring Boot 项目打包后的文件是一个 fat jar，包含了程序的所有依赖，通常会比较大。

然而我们仔细想想，这个 jar 文件中包含的依赖或资源文件，在开发过程中，其实变动是很少的，经常变动的是我们的程序代码，如果我们能把程序依赖和程序代码分开来添加到镜像里，就可以充分使用 Docker 镜像的缓存机制，加快镜像构建的速度，也减少了多个镜像存储的空间。

我们使用 `jar -xf` 命令将 jar 文件解压：

```
# mkdir -p target/dependency && cd target/dependency
# jar -xf ../*.jar
```

查看解压后的目录，我们发现，实际上一个 jar 包里的内容大体可以分成三个部分：

* /BOOT-INF/lib
* /META-INF
* /BOOT-INF/classes

其中 `/BOOT-INF/lib` 和 `/META-INF` 都是变动不多的部分，变动最多的是 `/BOOT-INF/classes` 目录下的程序代码。我们稍微修改下 Dockerfile 文件，将 jar 文件中的内容分层添加：

```
FROM openjdk:17-jdk-alpine
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring
ARG DEPENDENCY=target/dependency
COPY ${DEPENDENCY}/BOOT-INF/lib /app/lib
COPY ${DEPENDENCY}/META-INF /app/META-INF
COPY ${DEPENDENCY}/BOOT-INF/classes /app
ENTRYPOINT ["java", "-cp", "app:app/lib/*", "com.example.demo.DemoApplication"]
```

https://spring.io/guides/gs/spring-boot-docker/

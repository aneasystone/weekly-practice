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

### Dockerfile 中的 [`ENTRYPOINT`](https://docs.docker.com/engine/reference/builder/#entrypoint)

在上面的 Dockerfile 文件中，我们在最后一行使用了 `ENTRYPOINT` 指令指定了容器在启动之后执行 `java -jar /app.jar` 命令：

```
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

上面这种 `ENTRYPOINT` 为 `exec 格式`，除此之外，`ENTRYPOINT` 还有另一种 `shell 格式`：

```
ENTRYPOINT java -jar /app.java
```

`shell 格式` 和 `exec 格式` 的区别在于：`shell 格式` 在启动时是使用 `/bin/sh -c` 来执行的，这会导致容器中 PID 为 1 的进程是 `/bin/sh` 而不是 ENTRYPOINT 中指定的 Java，所以当我们使用 `docker stop` 停止容器时，接收到 `SIGTERM` 信号的是 `/bin/sh` 而不是 Java，我们的 Java 进程就不能优雅退出了。为了解决这个问题，一般在执行的命令前加上 `exec`：

```
ENTRYPOINT exec java -jar /app.java
```

而 `exec 格式` 就是使用 `exec` 来执行的，可以确保容器中 PID 为 1 的进程是 ENTRYPOINT 中指定的进程，一般推荐使用这种格式，而且还可以配合 `CMD` 指令内置程序的命令行参数，`shell 格式` 下 `CMD` 是无效的。

为了验证上面的说法，我写了三个 Dockerfile 文件，第一个是 `Dockerfile_exec`：
```
FROM openjdk:17-jdk-alpine
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
```
第二个是 `Dockerfile_shell_without_exec`：

```
FROM openjdk:17-jdk-alpine
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT java -jar /app.jar
```

第三个是 `Dockerfile_shell_with_exec`：

```
FROM openjdk:17-jdk-alpine
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT exec java -jar /app.jar
```

然后依次构建镜像：

```
# docker build -f Dockerfile_exec -t java-exec .
# docker build -f Dockerfile_shell_without_exec -t java-shell-without-exec .
# docker build -f Dockerfile_shell_with_exec -t java-shell-with-exec .
```

然后依次执行：

```
# docker run -it --rm --name java java-exec
```

再使用 `docker stop` 停止，可以看到响应时间很快：

```
# time docker stop java
java

real	0m0.278s
user	0m0.019s
sys	0m0.022s
```

这说明容器是正常结束的，因为如果 Java 进程没有接收到 `SIGTERM` 信号，是不会立即退出的，要等大约 10s 左右时间，docker 向容器发送 `SIGKILL` 信号时才会退出。不过奇怪的是，三个容器都可以正常退出，连 `ENTRYPOINT` 中不使用 `exec` 的 `java-shell-without-exec` 一样可以正常退出。

为了探究是怎么回事，使用 `docker images history` 查看并对比各个镜像：

```
[root@localhost demo]# docker image history java-exec --no-trunc | head -n 2
...
sha256:xx   18 minutes ago   /bin/sh -c #(nop)  ENTRYPOINT ["java" "-jar" "/app.jar"]

[root@localhost demo]# docker image history java-shell-with-exec --no-trunc | head -n 2
...
sha256:xxx   18 minutes ago   /bin/sh -c #(nop)  ENTRYPOINT ["/bin/sh" "-c" "exec java -jar /app.jar"]

[root@localhost demo]# docker image history java-shell-without-exec --no-trunc | head -n 2
...
sha256:xxx   18 minutes ago   /bin/sh -c #(nop)  ENTRYPOINT ["/bin/sh" "-c" "java -jar /app.jar"]
```

可以发现 `java-shell-without-exec` 镜像中的 `ENTRYPOINT java -jar /app.jar` 被替换成了 `ENTRYPOINT ["/bin/sh" "-c" "java -jar /app.jar"]`，怀疑是 `docker build` 时对镜像做了什么优化导致的，但是并没有什么证据。

然后去看了 Dockerfile 官方文档中的 [`ENTRYPOINT`](https://docs.docker.com/engine/reference/builder/#entrypoint) 的例子，又写了三个 Dockerfile，第一个是 `Dockerfile_top_exec`：

```
FROM ubuntu
ENTRYPOINT ["top", "-b"]
CMD ["-c"]
```

第二个是 `Dockerfile_top_shell_without_exec`：

```
FROM ubuntu
ENTRYPOINT top -b
```

第三个是 `Dockerfile_top_shell_with_exec`：

```
FROM ubuntu
ENTRYPOINT exec top -b
```

然后再依次构建镜像：

```
# docker build -f Dockerfile_top_exec -t top-exec .
# docker build -f Dockerfile_top_shell_with_exec -t top-shell-with-exec .
# docker build -f Dockerfile_top_shell_without_exec -t top-shell-without-exec .
```

当我们执行到 `top-shell-without-exec` 时：

```
# docker run -it --rm --name top top-shell-without-exec
```

奇怪的事情发生了，`docker stop` 花了 10s！

```
# time docker stop top
top

real	0m10.258s
user	0m0.016s
sys	0m0.027s
```

再使用 `docker images history` 查看并对比各个镜像：

```
[root@localhost test]# docker image history top-exec --no-trunc | head -n 2
...
sha256:xxx   8 minutes ago   /bin/sh -c #(nop)  ENTRYPOINT ["top" "-b"]

[root@localhost test]# docker image history top-shell-with-exec --no-trunc | head -n 2
...
sha256:xxx   14 minutes ago   /bin/sh -c #(nop)  ENTRYPOINT ["/bin/sh" "-c" "exec top -b"]

[root@localhost test]# docker image history top-shell-without-exec --no-trunc | head -n 2
...
sha256:xxx   14 minutes ago   /bin/sh -c #(nop)  ENTRYPOINT ["/bin/sh" "-c" "top -b"]
```

和上面的例子几乎是一模一样的，结果证明，并不是 `docker build` 做的手脚。难道是 Java 进程比较特殊吗？

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
1. [docker 与 gosu](https://cloud.tencent.com/developer/article/1454344)

## 更多

### 为什么不使用 `exec` Java 进程也能优雅退出？

使用 Python 或 Go 写两个小程序，验证其他进程是不是一样？

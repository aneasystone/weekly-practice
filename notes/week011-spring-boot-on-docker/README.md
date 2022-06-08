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

当 `ENTRYPOINT` 中的命令比较长时，可以编写一个简单的 Shell 脚本，这时 Dockerfile 的内容如下：

```
FROM openjdk:17-jdk-alpine
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
COPY run_without_exec.sh run.sh
RUN chmod +x run.sh
ENTRYPOINT ["./run.sh"]
```

脚本 `run_without_exec.sh` 内容如下：

```
#!/bin/sh
java -jar /app.jar
```

构建镜像并运行，这时再执行 `docker stop` 命令，我们发现会等待 10s 左右才退出，这是因为程序 Java 程序不是容器里 PID 为 1 的进程，它接收不到退出信号，导致 `docker` 等 10s 后将容器强制 kill 掉了。解决这个问题的方法是在 Shell 脚本中使用 `exec` 执行命令：

```
#!/bin/sh
exec java -jar /app.jar
```

另外在 Shell 脚本中要慎用 `sudo` 命令，而应该使用 `gosu`，可以参见 [docker 与 gosu](https://cloud.tencent.com/developer/article/1454344) 这篇文章查看他们之间的区别。

还有一点需要注意的是，如果我们在 Dockerfile 中使用环境变量，下面这样的 `exec 格式` 是不行的：

```
ENTRYPOINT ["java", "${JAVA_OPTS}", "-jar", "/app.jar"]
```

因为 `${JAVA_OPTS}` 这种变量需要 Shell 才能解析，而上面的 `ENTRYPOINT` 直接使用 `exec` 执行，并没有使用 Shell。解决方法是将启动命令写到一个 Shell 文件里，或者直接在 `ENTRYPOINT` 中使用 Shell：

```
ENTRYPOINT ["sh", "-c", "java ${JAVA_OPTS} -jar /app.jar"]
```

使用下面的命令验证 `${JAVA_OPTS}` 是否生效：

```
# docker run -p 8080:8080 -e "JAVA_OPTS=-Ddebug -Xmx128m" myorg/myapp
```

到目前为止，我们还没有用到命令行参数，如果像下面这样运行：

```
# docker run -p 8080:8080 myorg/myapp --debug
```

我们的本意是向 Java 进程传入 `--debug` 参数，可惜的是这并不生效，因为这个命令行参数被传给 `sh` 进程了。解决方法是在启动命令中使用 Shell 的两个特殊变量 `${0}` 和 `${@}`：

```
ENTRYPOINT ["sh", "-c", "java ${JAVA_OPTS} -jar /app.jar ${0} ${@}"]
```

如果运行的是 Shell 脚本，直接使用 `${@}` 变量即可：

```
#!/bin/sh
exec java ${JAVA_OPTS} -jar /app.jar ${@}
```

### 更小的镜像

注意上面所使用的基础镜像是 `openjdk:17-jdk-alpine`，`alpine` 镜像相对于标准的 [openjdk](https://hub.docker.com/_/openjdk) 镜像要小，不过不能保证所有的 Java 版本都有 `alpine` 镜像，比如 [Java 11 就没有对应的 `alpine` 镜像](https://stackoverflow.com/questions/53375613/why-is-the-java-11-base-docker-image-so-large-openjdk11-jre-slim)。

或者你可以使用 label 中带 jre 的镜像，jre 比 jdk 要小一点，不过也不是所有的版本都有对应的 jre 镜像，而且要注意的是，有些程序的运行可能依赖 jdk，在 jre 环境下是运行不了的。

另外一个方法是使用 [Jigsaw 项目的 JLink 工具](https://openjdk.java.net/projects/jigsaw/quick-start#linker)。`Jigsaw` 是 OpenJDK 项目下的一个子项目，旨在为 Java SE 平台设计、实现一个标准的 **模块系统**（Module System），并应用到该平台和 JDK 中。使用 JLink 可以让你按需选择模块来构建出自定义的 JRE 环境，这比官方提供的 JRE 要更小。不过这种方法不具备通用性，你要为不同的应用构建不同的 JRE 环境，虽然你能得到一个更小的单个镜像，但是不同的 JRE 基础镜像加起来还是不小的。

综上所述，构建镜像时我们并不一定非要追求镜像的体积能最小。镜像的体积能小一点当然很好，可以让上传和下载都很快，不过一旦镜像被缓存过，这个优势也就没有了。所以，不要凭自己的小聪明来构建更小的镜像，而让镜像缓存失效。如果你使用的都是同样的基础镜像，那么应该尝试去优化应用层，尽可能的将那些变动最多的内容放在镜像的最高层，那些体积大的变动不多的内容放在镜像的低层。

## 使用分层优化 Dockerfile

Spring Boot 应用使用了一种 [可执行的 JAR 文件格式](https://docs.spring.io/spring-boot/docs/current/reference/html/executable-jar.html)，这种 JAR 文件天然具有分层的特点。我们可以使用下面的命令将 JAR 文件解压：

```
# mkdir target/dependency && cd target/dependency
# jar -xf ../*.jar
```

JAR 文件的结构类似下面这样：

```
example.jar
 |
 +-META-INF
 |  +-MANIFEST.MF
 +-org
 |  +-springframework
 |     +-boot
 |        +-loader
 |           +-<spring boot loader classes>
 +-BOOT-INF
    +-classes
    |  +-com
    |     +-example
    |        +-YourClasses.class
    +-lib
       +-dependency1.jar
       +-dependency2.jar
```

所有的应用类放在 `BOOT-INF/classes` 目录下，而所有的依赖都在 `BOOT-INF/lib` 目录下。另外，`org.springframework.boot.loader` 目录下是 Spring Boot loader 的相关代码，是整个 JAR 文件能执行的关键，可以在 `META-INF/MANIFEST.MF` 文件中看到一些端倪：

```
Main-Class: org.springframework.boot.loader.JarLauncher
Start-Class: com.example.demo.DemoApplication
```

接下来我们创建一个带分层的 Dockerfile 文件：

```
FROM openjdk:17-jdk-alpine
ARG DEPENDENCY=target/dependency
COPY ${DEPENDENCY}/BOOT-INF/lib /app/lib
COPY ${DEPENDENCY}/META-INF /app/META-INF
COPY ${DEPENDENCY}/BOOT-INF/classes /app
ENTRYPOINT ["java", "-cp", "app:app/lib/*", "com.example.demo.DemoApplication"]
```

这个文件中包含了三层，其中 `BOOT-INF/lib` 目录是程序的依赖部分，几乎很少变动，我们将这一层放在第一层，而变动最多的应用代码 `/BOOT-INF/classes` 放在第三层，这样每次构建时都可以充分利用第一层的缓存，加快构建和启动速度。

而且当 JAR 文件比较大时，解压后的 JAR 文件启动速度要更快一点。

> 有一点值得注意的是，我们上面看到 JAR 文件中还包括 Spring Boot loader 的相关代码，但是在 Dockerfile 里并没有用到，所以我们在 `ENTRYPOINT` 中需要手工指定启动类 `com.example.demo.DemoApplication`。不过我们也可以将 Spring Boot loader 拷贝到容器里，使用 `org.springframework.boot.loader.JarLauncher` 来启动应用。下面直接使用 `JarLauncher` 来启动应用：
> ```
> $ jar -xf demo.jar
> $ java org.springframework.boot.loader.JarLauncher
> ```
> 使用 `JarLauncher` 启动应用的好处是不用再硬编码启动类，对于任意的 Spring Boot 项目都适用，而且还可以保证 classpath 的加载顺序，在 `BOOT-INF` 目录下可以看到一个 `classpath.idx` 文件，`JarLauncher` 就是用它来构建 classpath 的。

### Spring Boot Layer Index

从 Spring Boot 2.3.0 开始，构建出的 JAR 文件中多了一个 `layers.idx` 文件，这个文件包含了 JAR 文件的分层信息，类似于下面这样：

```
- "dependencies":
  - "BOOT-INF/lib/"
- "spring-boot-loader":
  - "org/"
- "snapshot-dependencies":
- "application":
  - "BOOT-INF/classes/"
  - "BOOT-INF/classpath.idx"
  - "BOOT-INF/layers.idx"
  - "META-INF/"
```

除了 `layers.idx` 文件，在 lib 目录我们还可以看到一个 `spring-boot-jarmode-layertools.jar` 文件，这个依赖文件可以让你的应用以一种新的模式来运行（`jarmode=layertools`）：

```
$ java -Djarmode=layertools -jar ./target/demo-0.0.1-SNAPSHOT.jar
Usage:
  java -Djarmode=layertools -jar demo-0.0.1-SNAPSHOT.jar

Available commands:
  list     List layers from the jar that can be extracted
  extract  Extracts layers from the jar for image creation
  help     Help about any command
```

可以使用 `layertools` 的 `extract` 命令将 JAR 文件按照分层信息解压出来：

```
$ mkdir target/extracted
$ java -Djarmode=layertools -jar target/demo-0.0.1-SNAPSHOT.jar extract --destination target/extracted
```

可以看出这里包括了四个分层：

* dependencies
* spring-boot-loader
* snapshot-dependencies
* application

和之前我们手工创建的分层相比，多了一层 `snapshot-dependencies`，这比之前直接将所有的依赖都放在一层更好，因为 SNAPSHOT 依赖也是很容易发生变化的。使用这个分层信息，我们重新编写 Dockerfile：

```
FROM openjdk:11-jdk-alpine
ARG EXTRACTED=target/extracted
COPY ${EXTRACTED}/dependencies/ ./
COPY ${EXTRACTED}/spring-boot-loader/ ./
COPY ${EXTRACTED}/snapshot-dependencies/ ./
COPY ${EXTRACTED}/application/ ./
ENTRYPOINT ["java", "org.springframework.boot.loader.JarLauncher"]
```

> 分层信息文件 `layers.idx` 是 Maven 或 Gradle 的 Spring Boot 插件在打包时自动生成的，如果要自定义 `layers.idx`，可以对插件进行配置，参见 Maven 文档 [Layered Jar or War](https://docs.spring.io/spring-boot/docs/2.7.0/maven-plugin/reference/htmlsingle/#packaging.layers)。

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
1. [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
1. [Spring Boot Reference Documentation: Container Images](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#container-images)
1. [体验SpringBoot(2.3)应用制作Docker镜像(官方方案)](https://blog.csdn.net/boling_cavalry/article/details/106597358)

## 更多

### 关于 `ENTRYPOINT` 的几点疑惑

为了验证上面说的 `ENTRYPOINT` 中必须使用 `exec` 来启动程序的说法，我写了三个 Dockerfile 文件，第一个是 `Dockerfile_exec`：

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

可以发现 `java-shell-without-exec` 镜像中的 `ENTRYPOINT java -jar /app.jar` 被替换成了 `ENTRYPOINT ["/bin/sh" "-c" "java -jar /app.jar"]`，难道是 `docker build` 时对镜像做了什么优化导致的吗？但是目前并没有什么证据。

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

和上面的例子几乎是一模一样的，结果证明，并不是 `docker build` 做的手脚。难道是 Java 进程比较特殊吗？为什么不使用 `exec` Java 进程也能优雅退出呢？后面可以使用 Python 或 Go 写两个小程序，验证其他进程是不是一样的？

另一个疑惑是，在 `ENTRYPOINT` 中指定命令行参数时：

```
ENTRYPOINT ["sh", "-c", "java ${JAVA_OPTS} -jar /app.jar ${0} ${@}"]
```

上面的 `${0}` 表示第 0 个参数，也就是被执行的程序，类似的，`${1}` 表示第一个参数，`${2}` 表示第二个参数，以此类推，`${@}` 表示所有的参数。但是很显然，在这个命令中，直接使用 `${@}` 应该就可以了，这里的 `${0}` 参数是起什么作用呢？而且如果我们和上面一样去执行 `sh -c` 命令：

```
# sh -c "java -jar /app.jar ${0} ${@}" --debug
```

命令行参数是不能生效的，那么 `docker run` 到底是如何启动 `ENTRYPOINT` 中指定的命令的呢？

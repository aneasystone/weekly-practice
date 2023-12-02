# WEEK050 - Java 21 初体验

2023 年 9 月 19 日，[Java 21](https://openjdk.org/projects/jdk/21/) 发布正式版本，这是 Java 时隔两年发布的又一个 LTS 版本，上一个 LTS 版本是 2021 年 9 月 14 日发布的 [Java 17](https://openjdk.org/projects/jdk/17/)：

![](./images/jdk-versions.png)

Java 17 目前是使用最广泛的版本，但随着 Java 21 的发布，这一局面估计会很快被打破，这是因为 Java 21 可能是几年内最为重要的版本，它带来了一系列重要的功能和特性，包括 [记录模式](https://openjdk.org/jeps/440)，[`switch` 模式匹配](https://openjdk.org/jeps/441)，[字符串模板](https://openjdk.org/jeps/430)，[分代式 ZGC](https://openjdk.org/jeps/439)，[不需要定义类的 Main 方法](https://openjdk.org/jeps/445)，等等等等，不过其中最为重要的一项，当属由 [Loom 项目](https://openjdk.org/projects/loom/) 发展而来的 [虚拟线程](https://openjdk.org/jeps/444)。Java 程序一直以文件体积大、启动速度慢、内存占用多被人诟病，但是有了虚拟线程，再结合 [GraalVM](https://www.graalvm.org/) 的原生镜像，我们就可以写出媲美 C、Rust 或 Go 一样小巧灵活、高性能、可伸缩的应用程序。

转眼间，距离 Java 21 发布已经快 3 个月了，网上相关的文章也已经铺天盖地，为了不使自己落伍，于是便打算花点时间学习一下。尽管在坊间一直流传着 **版本任你发，我用 Java 8** 这样的说法，但是作为一线 Java 开发人员，最好还是紧跟大势，未雨绸缪，有备无患。

## 准备开发环境

我这里使用 Docker Desktop 的 [Dev Environments](https://docs.docker.com/desktop/dev-environments/) 作为我们的实验环境。Dev Environments 是 Docker Desktop 从 3.5.0 版本开始引入的一项新特性，目前还处于 Beta 阶段，它通过配置文件的方式方便开发人员创建容器化的、可复用的开发环境，结合 VSCode 的 [Dev Containers 插件](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) 以及它丰富的插件生态可以帮助开发人员迅速展开编码工作，而不用疲于开发环境的折腾。

![](./images/dev-environments.png)

Dev Environments 的界面如上图所示，官方提供了两个示例供参考，一个是单容器服务，一个是多容器服务：

* [https://github.com/dockersamples/single-dev-env](https://github.com/dockersamples/single-dev-env)
* [https://github.com/dockersamples/compose-dev-env](https://github.com/dockersamples/compose-dev-env)

我们可以直接从 Git 仓库地址来创建开发环境，就如官方提供的示例一样，也可以从本地目录创建开发环境，默认情况下，Dev Environments 会自动检测项目的语言和依赖，不过自动检测的功能并不是那么准确，比如我们的目录是一个 Java 项目，Dev Environments 会使用 [docker/dev-environments-java](https://hub.docker.com/r/docker/dev-environments-java) 镜像来创建开发环境，而这个镜像使用的是 Java 11，并不是我们想要的。

> 如果自动检测失败，就会使用 [docker/dev-environments-default](https://hub.docker.com/r/docker/dev-environments-default) 这个通用镜像来创建开发环境。

所以我们还得手动指定镜像，总的来说，就是在项目根目录下创建一个 `compose-dev.yaml` 配置文件，内容如下：

```
services:
  app:
    entrypoint:
    - sleep
    - infinity
    image: openjdk:21-jdk
    init: true
    volumes:
    - type: bind
      source: /var/run/docker.sock
      target: /var/run/docker.sock
```

然后再使用 Dev Environments 打开该目录，程序会自动拉取该镜像并创建开发环境：

![](./images/dev-environments-created.png)

开发环境创建成功后，我们就可以使用 VSCode 打开了：

![](./images/dev-environments-done.png)

使用 VSCode 打开开发环境，实际上就是使用 VSCode 的 [Dev Containers 插件](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) 连接到容器里面，打开终端，敲入 `java -version` 命令：

```
bash-4.4# java -version
openjdk version "21" 2023-09-19
OpenJDK Runtime Environment (build 21+35-2513)
OpenJDK 64-Bit Server VM (build 21+35-2513, mixed mode, sharing)
```

由于这是一个崭新的环境，我们还要为 VSCode 安装一些开发所需的插件，比如 [Extension Pack for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack)：

![](./images/vscode-dev-env.png)

至此我们就得到了一个非常干净纯粹的 Java 21 开发环境。

## 特性体验

接下来，我们就在这个全新的开发环境中一览 Java 21 的全部特性，包括下面 15 个 JEP：

* 430:	[String Templates (Preview)](https://openjdk.org/jeps/430)
* 431:	[Sequenced Collections](https://openjdk.org/jeps/431)
* 439:	[Generational ZGC](https://openjdk.org/jeps/439)
* 440:	[Record Patterns](https://openjdk.org/jeps/440)
* 441:	[Pattern Matching for `switch`](https://openjdk.org/jeps/441)
* 442:	[Foreign Function & Memory API (Third Preview)](https://openjdk.org/jeps/442)
* 443:	[Unnamed Patterns and Variables (Preview)](https://openjdk.org/jeps/443)
* 444:	[Virtual Threads](https://openjdk.org/jeps/444)
* 445:	[Unnamed Classes and Instance Main Methods (Preview)](https://openjdk.org/jeps/445)
* 446:	[Scoped Values (Preview)](https://openjdk.org/jeps/446)
* 448:	[Vector API (Sixth Incubator)](https://openjdk.org/jeps/448)
* 449:	[Deprecate the Windows 32-bit x86 Port for Removal](https://openjdk.org/jeps/449)
* 451:	[Prepare to Disallow the Dynamic Loading of Agents](https://openjdk.org/jeps/451)
* 452:	[Key Encapsulation Mechanism API](https://openjdk.org/jeps/452)
* 453:	[Structured Concurrency (Preview)](https://openjdk.org/jeps/453)

### 字符串模板

https://openjdk.org/jeps/430

### 有序集合

https://openjdk.org/jeps/431

### 分代式 ZGC

https://openjdk.org/jeps/439

### 记录模式

https://openjdk.org/jeps/440

### `switch` 模式匹配

https://openjdk.org/jeps/441

### 外部函数和内存 API

https://openjdk.org/jeps/442

### 未命名模式和变量

https://openjdk.org/jeps/443

### 虚拟线程

https://openjdk.org/jeps/444

### 未命名类和实例的 Main 方法

https://openjdk.org/jeps/445

### 作用域值

https://openjdk.org/jeps/446

### 向量 API

https://openjdk.org/jeps/448

### 弃用 Windows 32-bit x86 移植，为删除做准备

https://openjdk.org/jeps/449

### 准备禁用代理的动态加载

https://openjdk.org/jeps/451

### 密钥封装机制 API

https://openjdk.org/jeps/452

### 结构化并发

https://openjdk.org/jeps/453

## 参考

* [The Arrival of Java 21](https://blogs.oracle.com/java/post/the-arrival-of-java-21)
* [Java 版本历史](https://zh.wikipedia.org/wiki/Java%E7%89%88%E6%9C%AC%E6%AD%B7%E5%8F%B2)
* [JDK11 升级 JDK17 最全实践干货来了 | 京东云技术团队](https://my.oschina.net/u/4090830/blog/10142895)
* [Java 21：下一个LTS版本，提供了虚拟线程、记录模式和模式匹配](https://www.infoq.cn/article/zIiqcmU8hiGhmuSAhzwb)
* [Hello, Java 21](https://spring.io/blog/2023/09/20/hello-java-21/)
* [Runtime efficiency with Spring (today and tomorrow)](https://spring.io/blog/2023/10/16/runtime-efficiency-with-spring)
* [GraalVM for JDK 21 is here!](https://medium.com/graalvm/graalvm-for-jdk-21-is-here-ee01177dd12d)

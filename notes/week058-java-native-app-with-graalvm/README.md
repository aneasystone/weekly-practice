# WEEK058 - 使用 GraalVM 编写 Java 原生应用

随着云原生技术的普及，Java 应用在云环境中的臃肿问题变得更加突出，比如：

* **镜像体积大**：传统的 Java 应用容器镜像通常包含完整的 JVM 和依赖库，导致镜像体积庞大，增加了存储和传输的成本；
* **启动速度慢**：传统的 Java 应用依赖于 JVM 的 **即时编译（JIT）** 机制，启动时需要加载大量类库和依赖，导致启动时间较长；
* **内存占用高**：JVM 需要为运行时分配大量内存，包括堆内存、元空间（Metaspace）等，导致资源浪费和成本增加；

在云原生环境中，尤其是微服务架构下，快速启动和弹性伸缩是核心需求，这也是云原生的基本理念：**轻量**、**快速**、**弹性**。很显然，Java 的这些问题和这个理念是相冲突的，而 GraalVM 正是解决这些问题的关键技术之一。

GraalVM 是由 Oracle 实验室于 2011 年启动的一个研究项目。项目初期主要专注于编译器 [Graal Compiler](https://www.graalvm.org/latest/reference-manual/java/compiler/) 的开发，目标是创建一个高性能的 Java 编译器，以替代传统的 HotSpot JVM 中的 C2 编译器；2017 年，推出了 Truffle 框架，支持多语言互操作，扩展了 GraalVM 的多语言能力，以超强性能运行 JavaScript、Python、Ruby 以及其他语言；不过这时的 GraalVM 还不温不火，只有少部分研究人员和早期尝鲜者在使用，直到 2018 年，GraalVM 1.0 正式发布，推出了 **原生镜像（Native Image）** 功能，标志着其正式进入主流市场。

GraalVM 的原生镜像功能通过 **提前编译（AOT）** 机制，显著改善了 Java 在云原生环境中的表现。GraalVM 可以将 Java 应用编译为独立的可执行文件，无需依赖 JVM，大幅减小了镜像体积；而且这种方式消除了 JIT 编译的开销，使启动时间从秒级降低到毫秒级；此外，原生镜像运行时仅加载必要的类库和资源，内存占用也比传统 Java 应用少得多。

## 快速上手

这一节我们将学习 GraalVM 的安装以及 Native Image 的基本使用。

### GraalVM 的安装

GraalVM 支持常见的操作系统，包括 [Linux](https://www.graalvm.org/latest/getting-started/linux/)、[macOS](https://www.graalvm.org/latest/getting-started/macos/) 和 [Windows](https://www.graalvm.org/latest/getting-started/windows/)。

在 Linux 和 macOS 下，推荐使用 [SDKMAN!](https://sdkman.io/) 来安装 GraalVM。首先我们安装 `SDKMAN!`：

```
$ curl -s "https://get.sdkman.io" | bash
```

安装完成后，使用 `sdk list java` 列出当前系统可用的 JDK 版本：

> 也可以使用 `sdk install java [TAB]` 列出所有可用版本。

```
================================================================================
Available Java Versions for macOS ARM 64bit
================================================================================
 Vendor        | Use | Version      | Dist    | Status     | Identifier
--------------------------------------------------------------------------------
 Corretto      |     | 23.0.1       | amzn    |            | 23.0.1-amzn         
               |     | 21.0.5       | amzn    |            | 21.0.5-amzn         
               |     | 17.0.13      | amzn    |            | 17.0.13-amzn        
               |     | 11.0.25      | amzn    |            | 11.0.25-amzn        
               |     | 8.0.432      | amzn    |            | 8.0.432-amzn        
 Gluon         |     | 22.1.0.1.r17 | gln     |            | 22.1.0.1.r17-gln    
               |     | 22.1.0.1.r11 | gln     |            | 22.1.0.1.r11-gln    
 GraalVM CE    |     | 23.0.1       | graalce |            | 23.0.1-graalce      
               | >>> | 21.0.2       | graalce | installed  | 21.0.2-graalce      
               |     | 17.0.9       | graalce | installed  | 17.0.9-graalce      
 GraalVM Oracle|     | 25.ea.4      | graal   |            | 25.ea.4-graal       
               |     | 25.ea.3      | graal   |            | 25.ea.3-graal       
               |     | 25.ea.2      | graal   |            | 25.ea.2-graal       
               |     | 25.ea.1      | graal   |            | 25.ea.1-graal       
               |     | 24.ea.27     | graal   |            | 24.ea.27-graal      
               |     | 24.ea.26     | graal   |            | 24.ea.26-graal      
               |     | 24.ea.25     | graal   |            | 24.ea.25-graal      
               |     | 24.ea.24     | graal   |            | 24.ea.24-graal      
               |     | 24.ea.23     | graal   |            | 24.ea.23-graal      
               |     | 24.ea.22     | graal   |            | 24.ea.22-graal      
               |     | 23.0.1       | graal   |            | 23.0.1-graal        
               |     | 21.0.5       | graal   |            | 21.0.5-graal        
               |     | 17.0.12      | graal   |            | 17.0.12-graal       
 Java.net      |     | 25.ea.5      | open    |            | 25.ea.5-open        
               |     | 25.ea.4      | open    |            | 25.ea.4-open        
               |     | 25.ea.3      | open    |            | 25.ea.3-open        
               |     | 25.ea.2      | open    |            | 25.ea.2-open        
               |     | 25.ea.1      | open    |            | 25.ea.1-open        
               |     | 24.ea.31     | open    |            | 24.ea.31-open       
               |     | 24.ea.30     | open    |            | 24.ea.30-open       
               |     | 24.ea.29     | open    |            | 24.ea.29-open       
               |     | 24.ea.28     | open    |            | 24.ea.28-open       
               |     | 24.ea.27     | open    |            | 24.ea.27-open       
               |     | 24.ea.26     | open    |            | 24.ea.26-open       
               |     | 23           | open    |            | 23-open             
               |     | 21.0.2       | open    |            | 21.0.2-open         
 JetBrains     |     | 21.0.5       | jbr     |            | 21.0.5-jbr          
               |     | 17.0.12      | jbr     |            | 17.0.12-jbr         
               |     | 11.0.14.1    | jbr     |            | 11.0.14.1-jbr       
 Liberica      |     | 23.0.1.fx    | librca  |            | 23.0.1.fx-librca    
               |     | 23.0.1       | librca  |            | 23.0.1-librca       
               |     | 21.0.5.fx    | librca  |            | 21.0.5.fx-librca    
               |     | 21.0.5       | librca  |            | 21.0.5-librca       
               |     | 17.0.13.fx   | librca  |            | 17.0.13.fx-librca   
               |     | 17.0.13      | librca  |            | 17.0.13-librca      
               |     | 11.0.25.fx   | librca  |            | 11.0.25.fx-librca   
               |     | 11.0.25      | librca  |            | 11.0.25-librca      
               |     | 8.0.432.fx   | librca  |            | 8.0.432.fx-librca   
               |     | 8.0.432      | librca  |            | 8.0.432-librca      
 Liberica NIK  |     | 24.1.1.r23   | nik     |            | 24.1.1.r23-nik      
               |     | 23.1.5.r21   | nik     |            | 23.1.5.r21-nik      
               |     | 23.1.5.fx    | nik     |            | 23.1.5.fx-nik       
               |     | 23.0.6.r17   | nik     |            | 23.0.6.r17-nik      
               |     | 23.0.6.fx    | nik     |            | 23.0.6.fx-nik       
               |     | 22.3.5.r17   | nik     |            | 22.3.5.r17-nik      
               |     | 22.3.5.r11   | nik     |            | 22.3.5.r11-nik      
 Mandrel       |     | 24.1.1.r23   | mandrel |            | 24.1.1.r23-mandrel  
               |     | 24.0.2.r22   | mandrel |            | 24.0.2.r22-mandrel  
               |     | 23.1.5.r21   | mandrel |            | 23.1.5.r21-mandrel  
 Microsoft     |     | 21.0.5       | ms      |            | 21.0.5-ms           
               |     | 17.0.13      | ms      |            | 17.0.13-ms          
               |     | 11.0.25      | ms      |            | 11.0.25-ms          
 Oracle        |     | 23.0.1       | oracle  |            | 23.0.1-oracle       
               |     | 22.0.2       | oracle  |            | 22.0.2-oracle       
               |     | 21.0.5       | oracle  |            | 21.0.5-oracle       
               |     | 17.0.12      | oracle  |            | 17.0.12-oracle      
 SapMachine    |     | 23.0.1       | sapmchn |            | 23.0.1-sapmchn      
               |     | 21.0.5       | sapmchn |            | 21.0.5-sapmchn      
               |     | 17.0.13      | sapmchn |            | 17.0.13-sapmchn     
               |     | 11.0.25      | sapmchn |            | 11.0.25-sapmchn     
 Semeru        |     | 21.0.5       | sem     |            | 21.0.5-sem          
               |     | 17.0.13      | sem     |            | 17.0.13-sem         
               |     | 11.0.25      | sem     |            | 11.0.25-sem         
 Temurin       |     | 23.0.1       | tem     |            | 23.0.1-tem          
               |     | 21.0.5       | tem     |            | 21.0.5-tem          
               |     | 17.0.13      | tem     |            | 17.0.13-tem         
               |     | 11.0.25      | tem     |            | 11.0.25-tem         
 Tencent       |     | 21.0.5       | kona    |            | 21.0.5-kona         
               |     | 17.0.13      | kona    |            | 17.0.13-kona        
               |     | 11.0.25      | kona    |            | 11.0.25-kona        
               |     | 8.0.432      | kona    |            | 8.0.432-kona        
 Zulu          |     | 23.0.1.fx    | zulu    |            | 23.0.1.fx-zulu      
               |     | 23.0.1       | zulu    |            | 23.0.1-zulu         
               |     | 21.0.5.fx    | zulu    |            | 21.0.5.fx-zulu      
               |     | 21.0.5       | zulu    |            | 21.0.5-zulu         
               |     | 17.0.13.fx   | zulu    |            | 17.0.13.fx-zulu     
               |     | 17.0.13      | zulu    |            | 17.0.13-zulu        
               |     | 11.0.25.fx   | zulu    |            | 11.0.25.fx-zulu     
               |     | 11.0.25      | zulu    |            | 11.0.25-zulu        
               |     | 8.0.432.fx   | zulu    |            | 8.0.432.fx-zulu     
               |     | 8.0.432      | zulu    |            | 8.0.432-zulu        
================================================================================
Omit Identifier to install default version 21.0.5-tem:
    $ sdk install java
Use TAB completion to discover available versions
    $ sdk install java [TAB]
Or install a specific version by Identifier:
    $ sdk install java 21.0.5-tem
Hit Q to exit this list view
================================================================================
```

其中 GraalVM 有两个，`GraalVM CE` 是由社区维护，是开源的，基于 OpenJDK 开发；而 `GraalVM Oracle` 是由 Oracle 发布，基于 Oracle JDK 开发，我们这里安装社区版：

```
$ sdk install java 21.0.2-graalce
```

使用 `java -version` 确认安装是否成功：

```
$ java -version
openjdk version "21.0.2" 2024-01-16
OpenJDK Runtime Environment GraalVM CE 21.0.2+13.1 (build 21.0.2+13-jvmci-23.1-b30)
OpenJDK 64-Bit Server VM GraalVM CE 21.0.2+13.1 (build 21.0.2+13-jvmci-23.1-b30, mixed mode, sharing)
```

### Native Image 的基本使用

## 参考

* [Getting Started with Oracle GraalVM](https://www.graalvm.org/latest/getting-started/)
* [Getting Started with Native Image](https://www.graalvm.org/latest/reference-manual/native-image/)
* [GraalVM Documentation](https://www.graalvm.org/latest/docs/)
* [GraalVM User Guides](https://www.graalvm.org/latest/guides/)
* [Java AOT 编译框架 GraalVM 快速入门](https://strongduanmu.com/blog/java-aot-compiler-framework-graalvm-quick-start.html)
* [Create a GraalVM Docker Image](https://www.baeldung.com/java-graalvm-docker-image)
* [如何借助 Graalvm 和 Picocli 构建 Java 编写的原生 CLI 应用](https://www.infoq.cn/article/4RRJuxPRE80h7YsHZJtX)
* [Runtime efficiency with Spring (today and tomorrow)](https://spring.io/blog/2023/10/16/runtime-efficiency-with-spring)
* [GraalVM for JDK 21 is here!](https://medium.com/graalvm/graalvm-for-jdk-21-is-here-ee01177dd12d)
* [GraalVM Native Image Support](https://docs.spring.io/spring-boot/docs/current/reference/html/native-image.html)
* [初步探索GraalVM--云原生时代JVM黑科技-京东云开发者社区](https://developer.jdcloud.com/article/2446)

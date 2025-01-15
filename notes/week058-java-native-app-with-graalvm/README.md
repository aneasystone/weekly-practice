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

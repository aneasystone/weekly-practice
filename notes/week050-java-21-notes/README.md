# WEEK050 - Java 21 初体验

2023 年 9 月 19 日，[Java 21](https://openjdk.org/projects/jdk/21/) 发布正式版本，时隔两年，这是 Java 的又一个 LTS 版本（上一个 LTS 版本是 2021 年 9 月 14 日发布的 [Java 17](https://openjdk.org/projects/jdk/17/)）：

![](./images/jdk-versions.png)

这可能是几年内最为重要的 Java 版本了，它带来了一系列重要的功能和特性，包括 [记录模式](https://openjdk.org/jeps/440)，[`switch` 模式匹配](https://openjdk.org/jeps/441)，[字符串模板](https://openjdk.org/jeps/430)，[分代式 ZGC](https://openjdk.org/jeps/439)，[不需要定义类的 Main 方法](https://openjdk.org/jeps/445)，等等等等，不过其中最重要的一项，当属由 [Loom 项目](https://openjdk.org/projects/loom/) 发展而来的 [虚拟线程](https://openjdk.org/jeps/444)。

Virtual threads and GraalVM native images mean that today, you can write code that delivers performance and scalability on par with the likes of C, Rust, or Go while retaining the robust and familiar ecosystem of the JVM.

转眼间，距离 Java 21 发布已经过去 3 个月了，

## 环境准备

https://docs.docker.com/desktop/dev-environments/

https://hub.docker.com/_/openjdk

## 特性体验

### 字符串模板

## 参考

* [The Arrival of Java 21](https://blogs.oracle.com/java/post/the-arrival-of-java-21)
* [Java 版本历史](https://zh.wikipedia.org/wiki/Java%E7%89%88%E6%9C%AC%E6%AD%B7%E5%8F%B2)
* [JDK11 升级 JDK17 最全实践干货来了 | 京东云技术团队](https://my.oschina.net/u/4090830/blog/10142895)
* [Java 21：下一个LTS版本，提供了虚拟线程、记录模式和模式匹配](https://www.infoq.cn/article/zIiqcmU8hiGhmuSAhzwb)
* [Hello, Java 21](https://spring.io/blog/2023/09/20/hello-java-21/)
* [Runtime efficiency with Spring (today and tomorrow)](https://spring.io/blog/2023/10/16/runtime-efficiency-with-spring)

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
 GraalVM CE    |     | 23.0.1       | graalce |            | 23.0.1-graalce      
               | >>> | 21.0.2       | graalce | installed  | 21.0.2-graalce      
               |     | 17.0.9       | graalce | installed  | 17.0.9-graalce      
 GraalVM Oracle|     | 25.ea.4      | graal   |            | 25.ea.4-graal       
               |     | 24.ea.27     | graal   |            | 24.ea.27-graal      
               |     | 23.0.1       | graal   |            | 23.0.1-graal        
               |     | 21.0.5       | graal   |            | 21.0.5-graal        
               |     | 17.0.12      | graal   |            | 17.0.12-graal       
 Java.net      |     | 25.ea.5      | open    |            | 25.ea.5-open        
               |     | 24.ea.31     | open    |            | 24.ea.31-open       
               |     | 23           | open    |            | 23-open             
               |     | 21.0.2       | open    |            | 21.0.2-open         
 JetBrains     |     | 21.0.5       | jbr     |            | 21.0.5-jbr          
               |     | 17.0.12      | jbr     |            | 17.0.12-jbr         
               |     | 11.0.14.1    | jbr     |            | 11.0.14.1-jbr       
 Liberica      |     | 23.0.1       | librca  |            | 23.0.1-librca       
               |     | 21.0.5       | librca  |            | 21.0.5-librca       
               |     | 17.0.13      | librca  |            | 17.0.13-librca      
               |     | 11.0.25      | librca  |            | 11.0.25-librca      
               |     | 8.0.432      | librca  |            | 8.0.432-librca      
 Liberica NIK  |     | 24.1.1.r23   | nik     |            | 24.1.1.r23-nik      
               |     | 23.1.5.r21   | nik     |            | 23.1.5.r21-nik      
               |     | 22.3.5.r17   | nik     |            | 22.3.5.r17-nik      
 Mandrel       |     | 24.1.1.r23   | mandrel |            | 24.1.1.r23-mandrel  
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
 Zulu          |     | 23.0.1       | zulu    |            | 23.0.1-zulu         
               |     | 21.0.5       | zulu    |            | 21.0.5-zulu         
               |     | 17.0.13      | zulu    |            | 17.0.13-zulu        
               |     | 11.0.25      | zulu    |            | 11.0.25-zulu        
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

接下来，我们将通过最简单的 Hello World 例子了解 Native Image 的基本使用。

首先，我们创建一个 `Hello.java` 文件，如下：

```
class Hello {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

直接使用 `java` 命令运行，确保程序没有错误：

```
$ java Hello.java
Hello
```

然后使用 `javac` 将 `.java` 文件编译成 `.class` 文件：

```
$ javac Hello.java
```

此时，当前目录下会生成一个 `Hello.class` 文件。接下来使用 `native-image` 命令，将 `.class` 文件打包成可执行程序：

```
$ native-image Hello
========================================================================================================================
GraalVM Native Image: Generating 'hello' (executable)...
========================================================================================================================
[1/8] Initializing...                                                                                    (7.2s @ 0.10GB)
 Java version: 21.0.2+13, vendor version: GraalVM CE 21.0.2+13.1
 Graal compiler: optimization level: 2, target machine: armv8-a
 C compiler: cc (apple, arm64, 15.0.0)
 Garbage collector: Serial GC (max heap size: 80% of RAM)
 1 user-specific feature(s):
 - com.oracle.svm.thirdparty.gson.GsonFeature
------------------------------------------------------------------------------------------------------------------------
Build resources:
 - 12.09GB of memory (75.6% of 16.00GB system memory, determined at start)
 - 8 thread(s) (100.0% of 8 available processor(s), determined at start)
[2/8] Performing analysis...  [****]                                                                     (5.6s @ 0.32GB)
    3,225 reachable types   (72.5% of    4,450 total)
    3,810 reachable fields  (50.1% of    7,606 total)
   15,653 reachable methods (45.6% of   34,359 total)
    1,059 types,    87 fields, and   678 methods registered for reflection
       57 types,    57 fields, and    52 methods registered for JNI access
        4 native libraries: -framework Foundation, dl, pthread, z
[3/8] Building universe...                                                                               (1.3s @ 0.29GB)
[4/8] Parsing methods...      [*]                                                                        (0.6s @ 0.29GB)
[5/8] Inlining methods...     [***]                                                                      (0.5s @ 0.46GB)
[6/8] Compiling methods...    [**]                                                                       (4.9s @ 0.34GB)
[7/8] Layouting methods...    [*]                                                                        (0.7s @ 0.50GB)
[8/8] Creating image...       [*]                                                                        (1.5s @ 0.47GB)
   5.08MB (39.25%) for code area:     8,896 compilation units
   7.48MB (57.87%) for image heap:   97,240 objects and 76 resources
 381.68kB ( 2.88%) for other data
  12.93MB in total
------------------------------------------------------------------------------------------------------------------------
Top 10 origins of code area:                                Top 10 object types in image heap:
   3.80MB java.base                                            1.58MB byte[] for code metadata
 936.91kB svm.jar (Native Image)                               1.29MB byte[] for java.lang.String
 108.35kB java.logging                                       976.00kB java.lang.String
  56.84kB org.graalvm.nativeimage.base                       748.94kB java.lang.Class
  43.64kB jdk.proxy1                                         328.26kB byte[] for general heap data
  42.03kB jdk.proxy3                                         277.15kB com.oracle.svm.core.hub.DynamicHubCompanion
  21.98kB org.graalvm.collections                            244.27kB java.util.HashMap$Node
  19.52kB jdk.internal.vm.ci                                 219.04kB java.lang.Object[]
  10.46kB jdk.proxy2                                         184.95kB java.lang.String[]
   8.04kB jdk.internal.vm.compiler                           155.52kB byte[] for reflection metadata
   2.95kB for 2 more packages                                  1.55MB for 905 more object types
------------------------------------------------------------------------------------------------------------------------
Recommendations:
 INIT: Adopt '--strict-image-heap' to prepare for the next GraalVM release.
 HEAP: Set max heap for improved and more predictable memory usage.
 CPU:  Enable more CPU features with '-march=native' for improved performance.
------------------------------------------------------------------------------------------------------------------------
                        1.3s (5.7% of total time) in 115 GCs | Peak RSS: 0.93GB | CPU load: 4.04
------------------------------------------------------------------------------------------------------------------------
Produced artifacts:
 /Users/aneasystone/Codes/github/weekly-practice/notes/week058-java-native-app-with-graalvm/demo/hello (executable)
========================================================================================================================
Finished generating 'hello' in 22.6s.
```

上面可以看到 `native-image` 详情的运行过程，最终生成一个 `hello` 文件，可以直接执行：

```
$ ./hello 
Hello
```

`native-image` 不仅可以将类文件转换为可执行文件，也支持输入 JAR 文件或模块（Java 9 及更高版本），参考 [这里](https://www.graalvm.org/latest/reference-manual/native-image/guides/build-native-executable-from-jar/) 和 [这里](https://www.graalvm.org/latest/reference-manual/native-image/guides/build-java-modules-into-native-executable/)；除了可以编译可执行文件，`native-image` 还可以将类文件 [编译成共享库（native shared library）](https://www.graalvm.org/latest/reference-manual/native-image/guides/build-native-shared-library/)。

## 构建复杂应用

上一节我们演示了如何将单个 Java 文件编译成可执行文件，不过在日常工作中，我们的项目可没这么简单，一般会使用 Maven 来对代码进行组织，在微服务盛行的今天，更多的项目是使用一些微服务框架来开发，如何将这些复杂应用编译成可执行文件也是一个值得学习的课题。

### 一个简单的 Maven 项目

GraalVM 提供了 [Maven 插件](https://graalvm.github.io/native-build-tools/latest/maven-plugin.html)，方便我们在 Maven 项目中使用 Native Image 构建原生应用。

> GraalVM 同时也支持 Gradle 插件，如果你使用的是 Gradle 管理项目，可以参考 [Gradle 插件文档](https://graalvm.github.io/native-build-tools/latest/gradle-plugin.html)。

首先，我们用 `mvn archetype:generate` 生成一个 Maven 项目：

```
$ mvn archetype:generate \
    -DgroupId=com.example \
    -DartifactId=hello \
    -DarchetypeArtifactId=maven-archetype-quickstart \
    -DinteractiveMode=false
```

这里选择的项目脚手架为 `maven-archetype-quickstart`，关于项目脚手架的使用，可以参考我之前写的 [这篇笔记](../week004-creating-spring-project/README.md)。

生成项目的目录结构如下所示：

```
hello
├── pom.xml
└── src
    ├── main
    │   └── java
    │       └── com
    │           └── example
    │               └── App.java
    └── test
        └── java
            └── com
                └── example
                    └── AppTest.java
```

打开 `pom.xml` 文件，添加如下两个 Maven 插件，用于编译和打包：

```
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.12.1</version>
            <configuration>
                <fork>true</fork>
            </configuration>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-jar-plugin</artifactId>
            <version>3.3.0</version>
            <configuration>
                <archive>
                    <manifest>
                        <mainClass>com.example.App</mainClass>
                        <addClasspath>true</addClasspath>
                    </manifest>
                </archive>
            </configuration>
        </plugin>
    </plugins>
</build>
```

此时我们就可以使用 `mvn clean package` 命令，将项目打包成可执行的 JAR 文件了：

```
$ mvn clean package
```

使用 `java -jar` 运行 JAR 文件：

```
$ java -jar ./target/hello-1.0-SNAPSHOT.jar 
Hello World!
```

接下来我们可以使用 `native-image -jar` 将 JAR 文件转换为可执行文件，或者我们可以更进一步，在 `pom.xml` 文件中添加如下配置：

```
<profiles>
    <profile>
        <id>native</id>
        <build>
            <plugins>
                <plugin>
                    <groupId>org.graalvm.buildtools</groupId>
                    <artifactId>native-maven-plugin</artifactId>
                    <version>0.10.4</version>
                    <extensions>true</extensions>
                    <executions>
                        <execution>
                            <id>build-native</id>
                            <goals>
                                <goal>compile-no-fork</goal>
                            </goals>
                            <phase>package</phase>
                        </execution>
                        <execution>
                            <id>test-native</id>
                            <goals>
                                <goal>test</goal>
                            </goals>
                            <phase>test</phase>
                        </execution>
                    </executions>
                </plugin>
            </plugins>
        </build>
    </profile>
</profiles>
```

> 注意，从 JDK 21 开始，Native Image Maven Plugin 改成了 `org.graalvm.buildtools:native-maven-plugin`，之前的版本中使用的是 `org.graalvm.nativeimage:native-image-maven-plugin`，参考 [这里](https://docs.oracle.com/en/graalvm/enterprise/20/docs/reference-manual/native-image/NativeImageMavenPlugin/)。

然后执行如下命令：

```
$ mvn clean package -Pnative -DskipTests=true
```

这样不仅可以将项目打包成 JAR 文件，同时也会生成一个可执行文件：

```
$ ./target/hello 
Hello World!
```

注意在上面的命令中我们加了一个忽略测试的参数 `-DskipTests=true`，如果不加的话，可能会报错：

```
[ERROR] Failed to execute goal org.graalvm.buildtools:native-maven-plugin:0.10.4:test (test-native) on project hello: 
Execution test-native of goal org.graalvm.buildtools:native-maven-plugin:0.10.4:test failed: Test configuration file wasn't found.
```

根据 [Testing support](https://graalvm.github.io/native-build-tools/latest/maven-plugin.html#testing-support) 部分的说明，目前插件只支持 JUnit 5.8.1 以上的版本，而通过 `maven-archetype-quickstart` 脚手架生成的项目里用的是 JUnit 3.8.1，所以我们可以将依赖改为：

```
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-api</artifactId>
    <version>5.10.5</version>
    <scope>test</scope>
</dependency>
```

同时将测试类替换成 JUnit 5 的写法：

```
package com.example;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.*;

public class AppTest
{
    @Test
    public void testApp()
    {
        assertEquals( "hello".length(), 5 );
    }
}
```

这时就可以去掉 `-DskipTests=true` 参数了：

```
$ mvn clean package -Pnative
```

> 注意，从构建输出上可以看出来，单元测试运行了两遍，第一遍是标准的 `surefire:test`，第二遍是 Native Image 的 `native:test`，这两次运行的目的和场景是不一样的，`surefire:test` 在 JVM 上运行，验证代码在 JVM 环境下的正确性，`native:test` 在 Native Image 构建的上下文中运行，验证代码在 Native Image 环境下的正确性。如果你的代码在两种环境下的行为可能不同（如反射、动态类加载等），可能需要都运行，否则只运行 `surefire:test` 即可，可以通过 `-DskipNativeTests=true` 跳过 `native:test`。

### 一个简单的 Spring Boot 项目

这一节将演示如何从 Spring Boot 应用程序构建一个本地可执行文件，[Spring Boot 从 3.0 开始支持原生镜像](https://www.graalvm.org/reference-manual/native-image/guides/build-spring-boot-app-into-native-executable/)，可以更轻松地配置项目，并显著提高 Spring Boot 应用程序的性能。

> 其他主流的微服务框架均已支持 GraalVM 的原生镜像功能，如：[Quarkus](https://quarkus.io/guides/building-native-image)、[Helidon SE](https://helidon.io/docs/v4/se/guides/graalnative)、[Micronaut](https://guides.micronaut.io/latest/micronaut-creating-first-graal-app.html) 等。

首先，我们需要一个测试的 Spring Boot 应用，有很多快速创建 Spring Boot 脚手架的方法，可以参考我之前写的 [这篇笔记](../week004-creating-spring-project/README.md)，我最喜欢的方法有两种：[Spring Initializr](https://start.spring.io/#!dependencies=native,web) 和 [Spring Boot CLI](https://docs.spring.io/spring-boot/installing.html#getting-started.installing.cli)，这里通过 `Spring Boot CLI` 来创建：

可以使用 `SDKMAN!` 安装 `Spring Boot CLI`：

```
$ sdk install springboot
$ spring --version
Spring CLI v3.4.1
```

安装完毕后，执行如下命令生成：

```
$ spring init --name hello \
	--artifact-id hello \
	--group-id com.example \
	--language java \
	--java-version 21 \
	--boot-version 3.4.1 \
	--type maven-project \
	--dependencies web,native \
	hello
```

打开 `pom.xml` 文件可以发现，生成的代码中已经自动为我们加了 `native-maven-plugin` 依赖。

这时，我们可以执行 `mvn clean package` 将程序打成 JAR 包并运行，也可以执行 `mvn spring-boot:run` 直接运行：

```
$ mvn spring-boot:run
...
2025-01-17T08:56:17.206+08:00  INFO 33037 --- [hello] [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port 8080 (http) with context path '/'
2025-01-17T08:56:17.210+08:00  INFO 33037 --- [hello] [           main] com.example.hello.HelloApplication       : Started HelloApplication in 0.548 seconds (process running for 0.662)
```

如果要将程序打包成可执行文件，可以执行如下命令：

```
$ mvn native:compile -Pnative
```

然后运行之：

```
$ ./target/hello
...
2025-01-17T09:02:19.732+08:00  INFO 33935 --- [hello] [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port 8080 (http) with context path '/'
2025-01-17T09:02:19.733+08:00  INFO 33935 --- [hello] [           main] com.example.hello.HelloApplication       : Started HelloApplication in 0.054 seconds (process running for 0.071)
```

可以看到启动速度是 JAR 文件的 10 倍。

## 容器化

在云原生环境下，所有服务都被打包成镜像，这也被称为 **容器化（Containerize）**。我在很早以前写过一篇 [博客](../week011-spring-boot-on-docker/README.md) 介绍了如何编写 Dockerfile 将 Spring Boot 应用构建成 Docker 镜像，针对 GraalVM 原生应用，我们一样可以照葫芦画瓢。

### 将 JAR 打包成镜像

最简单的方式是基于 JDK 基础镜像，直接将 JAR 文件拷贝进去即可，新建 `Dockerfile.jvm` 文件，内容如下：

```
FROM ghcr.io/graalvm/jdk-community:21

EXPOSE 8080
COPY ./target/hello-0.0.1-SNAPSHOT.jar app.jar
CMD ["java","-jar","app.jar"]
```

之前说过 GraalVM 也可以作为普通的 JDK 使用，所以这里直接使用 [GraalVM 的 JDK 镜像](https://www.graalvm.org/latest/getting-started/container-images/)。首先通过 `mvn package` 正常将项目打成 JAR 包，然后执行如下命令构建镜像：

```
$ docker build -f Dockerfile.jvm -t hello:jvm .
```

运行该镜像：

```
$ docker run --rm -p 8080:8080 hello:jvm
```

这种方式虽然简单，但是每次构建镜像之前先得 `mvn package` 一下，可以使用 [多阶段构建（Multi-stage builds）](https://docs.docker.com/build/building/multi-stage/) 的技巧，将两步合成一步。新建 `Dockerfile.jvm.ms` 文件，内容如下：

```
FROM ghcr.io/graalvm/native-image-community:21 AS builder

WORKDIR /build
COPY . /build
RUN ./mvnw --no-transfer-progress package -DskipTests=true

FROM ghcr.io/graalvm/jdk-community:21

EXPOSE 8080
COPY --from=builder /build/target/hello-0.0.1-SNAPSHOT.jar app.jar
CMD ["java","-jar","app.jar"]
```

整个 Dockerfile 分为两个构建阶段，第一阶段使用 `mvn package` 生成 JAR 文件，第二阶段和 `Dockerfile.jvm` 几乎是一样的，只不过是从第一阶段的构建结果中拷贝 JAR 文件。

直接执行如下命令构建镜像：

```
$ docker build -f Dockerfile.jvm.ms -t hello:jvm.ms .
```

运行该镜像：

```
$ docker run --rm -p 8080:8080 hello:jvm.ms
```

### 将二进制文件打包成镜像

有了上面的基础，我们可以更进一步，直接将二进制文件打包成镜像，这样可以省去 JDK，大大减小镜像体积。我们可以基于某个系统镜像，比如 `alpine` 或 `almalinux`，新建 `Dockerfile.native` 文件如下：

```
FROM almalinux:9

EXPOSE 8080
COPY target/hello app
ENTRYPOINT ["/app"]
```

然后执行如下命令构建镜像：

```
$ docker build -f Dockerfile.native -t hello:native .
```

运行该镜像：

```
$ docker run --rm -p 8080:8080 hello:native
```

不过这一次没有那么顺利，运行报错了：

```
exec /app: exec format error
```

这里就不得不提可执行文件格式的概念了。我们知道 GraalVM 的原生镜像功能是将 Java 代码编译成二进制文件，但是要注意的是，这个二进制文件是平台相关的，在不同的操作系统下，可执行文件的格式大相径庭。常见的可执行文件格式有以下几种：

* **ELF 格式（Executable and Linkable Format）**：是一种通用的可执行文件格式，广泛用于类 UNIX 系统，如 Linux 和 BSD；
* **Mach-O 格式（Mach Object）**：是苹果公司开发的可执行文件格式，用于 macOS 和 iOS 系统；
* **PE 格式（Portable Executable）**：Windows 系统下的 `.exe` 文件就是这种格式。

Docker 容器基于 Linux 内核开发，所以只能运行 ELF 格式的文件，而上面的二进制文件是我在 Mac 电脑上构建的，所以复制到容器里无法运行。

如果你使用的是 Linux 开发环境，可能就不会遇到这个问题；但是如果你和我一样，使用的是 Mac 或 Windows 操作系统，建议还是使用多阶段构建的技巧。新建 `Dockerfile.native.ms` 文件如下：

```
FROM ghcr.io/graalvm/native-image-community:21 AS builder

WORKDIR /build
COPY . /build
RUN ./mvnw --no-transfer-progress native:compile -Pnative -DskipTests=true

FROM almalinux:9

EXPOSE 8080
COPY --from=builder /build/target/hello app
ENTRYPOINT ["/app"]
```

构建镜像：

```
$ docker build -f Dockerfile.native.ms -t hello:native.ms .
```

运行镜像：

```
$ docker run --rm -p 8080:8080 hello:native.ms
```

在实验过程中还有一点值得特别注意，那就是 GLIBC 的兼容性问题，可以使用 `ldd --version` 确认构建和运行使用的两个基础镜像中 GLIBC 版本。

查看 `ghcr.io/graalvm/native-image-community:21` 的 GLIBC 版本：

```
$ docker run --rm --entrypoint sh ghcr.io/graalvm/native-image-community:21 ldd --version
ldd (GNU libc) 2.34
Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
Written by Roland McGrath and Ulrich Drepper.
```

查看 `almalinux:9` 的 GLIBC 版本：

```
$ docker run --rm --entrypoint sh almalinux:9 ldd --version
ldd (GNU libc) 2.34
Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
Written by Roland McGrath and Ulrich Drepper.
```

可以看出这两个基础镜像的 GLIBC 是一致的。如果我们将 `almalinux:9` 换成 `centos:7`：

```
$ docker run --rm --entrypoint sh centos:7 ldd --version
ldd (GNU libc) 2.17
Copyright (C) 2012 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
Written by Roland McGrath and Ulrich Drepper.
```

运行时就可能报下面这样的报错：

```
/app: /lib64/libc.so.6: version `GLIBC_2.32' not found (required by /app)
/app: /lib64/libc.so.6: version `GLIBC_2.34' not found (required by /app)
```

### 使用 CNB 构建镜像

[CNB（Cloud Native Buildpacks）](https://buildpacks.io/) 是一种用于构建和打包应用程序的技术，旨在简化应用程序的开发、部署和运行，使用 CNB 开发人员无需编写 Dockerfile 就可以构建容器镜像。它会自动检测应用程序的类型和所需的环境，根据检测结果，下载必要的依赖项，并将它们与应用程序代码打包，最终生成一个符合 OCI 标准的容器镜像。

Spring Boot 的 Maven 插件 `spring-boot-maven-plugin` 已经集成了 CNB，它使用 [Paketo Java Native Image buildpack](https://paketo.io/docs/reference/java-native-image-reference/) 来生成包含本地可执行文件的轻量级容器镜像。

针对上面的 Spring Boot 应用，我们可以直接运行下面的命令：

```
$ mvn spring-boot:build-image -Pnative
...
[INFO] Successfully built image 'docker.io/library/hello:0.0.1-SNAPSHOT'
...
```

> 构建之前，请确保有一个兼容 Docker-API 的容器运行时，比如 [Rancher Desktop](https://docs.rancherdesktop.io/getting-started/installation/)、[Docker](https://www.docker.io/gettingstarted/) 或 [Podman](https://podman.io/docs/installation) 等。

使用 `docker run` 运行：

```
$ docker run --rm -p 8080:8080 hello:0.0.1-SNAPSHOT
```

生成的镜像名默认为 `docker.io/library/${project.artifactId}:${project.version}`，可以通过下面的配置进行修改：

```
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <configuration>
        <image>
            <name>docker.io/library/aneasystone/${project.artifactId}:${project.version}</name>
        </image>
    </configuration>
</plugin>
```

更多构建参数可以参考 Spring Boot 官方文档 [Packaging OCI Images](https://docs.spring.io/spring-boot/maven-plugin/build-image.html)。

## GraalVM 的局限性

软件行业有一句名言：**没有银弹（No Silver Bullet）**，对于 GraalVM 技术也同样如此，它虽然具有镜像体积小、启动速度快、内存消耗低等优势，但是同时它也带来了一些新问题：

* **编译速度慢**：GraalVM 通过 AOT 技术对整个应用程序及其依赖进行静态分析，以确保所有代码路径都被覆盖，这种静态编译方式需要处理更多的复杂性，因而编译速度也更慢；
* **平台相关性**：编译出来的二进制文件是平台相关的，也就是说软件开发人员需要针对不同的平台编译不同的二进制文件，增加了软件分发的复杂性；
* **调试监控难**：由于运行的程序由 Java 程序变成了本地程序，传统面向 Java 程序的调试、监控、Agent 等技术均不再适用，只能使用 GDB 调试；
* **封闭性假设**：这是 AOT 编译的基本原则，即程序在编译期必须掌握运行时所需的所有信息，在运行时不能出现任何编译器未知的内容，这会导致 Java 程序中的很多动态特性无法继续使用，例如：资源、反射、动态类加载、动态代理、JCA 加密机制（内部依赖了反射）、JNI、序列化等。

针对每个新问题也都有对应的解决方案。比如引入 CI/CD 流水线自动化构建，让开发人员降低编译速度慢的感知；比如通过 Docker 容器镜像统一软件的分发方式；GraalVM 目前也在不断优化，增加传统 Java 调试和监控工具的支持，如 [JFR](https://www.graalvm.org/latest/reference-manual/native-image/guides/build-and-run-native-executable-with-jfr/) 和 [JMX](https://www.graalvm.org/latest/reference-manual/native-image/guides/build-and-run-native-executable-with-remote-jmx/) 等；对于程序中的动态特性，也可以通过额外的适配工作来解决。

下面针对最后一个问题进行更进一步的实践。

### 资源文件

资源文件是项目开发中经常遇到的一种场景，但是默认情况下， `native-image` 工具不会将资源文件集成到可执行文件中。首先，我们准备两个文件，`App.java` 为主程序，`app.res` 为资源文件：

```
├── App.java
└── app.res
```

`App.java` 中的代码非常简单，读取并输出 `app.res` 中的内容：

```
public class App {
    
    public static void main( String[] args ) throws IOException {
        String message = readResource("app.res");
        System.out.println(message);
    }

    public static String readResource(String fileName) throws IOException {
        StringBuilder content = new StringBuilder();
        try (
            InputStream inputStream = App.class.getClassLoader().getResourceAsStream(fileName);
            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line).append(System.lineSeparator());
            }
        }
        return content.toString();
    }
}
```

我们使用 `native-image` 生成可执行文件：

```
$ javac App.java && native-image App
```

运行这个文件会抛出如下的空指针异常：

```
$ ./app
Exception in thread "main" java.lang.NullPointerException
        at java.base@21.0.2/java.io.Reader.<init>(Reader.java:168)
        at java.base@21.0.2/java.io.InputStreamReader.<init>(InputStreamReader.java:123)
        at App.readResource(App.java:18)
        at App.main(App.java:10)
```

根据异常信息推断，`getResourceAsStream` 返回了空指针，也就是说没有读到 `app.res` 资源文件，可以看出 `native-image` 确实没有把资源文件集成到可执行文件中。

为了让 `native-image` 知道资源文件的存在，我们新建一个 `META-INF/native-image` 目录，目录下新建一个 `resource-config.json` 文件，目录结构如下所示：

```
├── App.java
├── META-INF
│   └── native-image
│       └── resource-config.json
└── app.res
```

`resource-config.json` 文件的内容如下：

```
{
    "resources": {
        "includes": [
            {
                "pattern": "app.res"
            }
        ]
    },
    "bundles": []
}
```

重新运行 `native-image` 进行构建：

```
$ javac App.java && native-image App
```

`native-image` 会自动扫描 `META-INF/native-image` 目录下的配置文件，将资源文件集成到可执行文件中，此时就可以正常运行这个文件了：

```
$ ./app                             
Hello message from the resource file.
```

### 反射

接下来，我们再看一个反射的例子。反射是 Java 中一项非常重要的特性，可以根据字符串来动态地加载类和方法，`native-image` 如果得不到足够的上下文信息，可能编译时就会缺少这些反射的类和方法。不过 `native-image` 也是足够聪明的，如果在调用某些反射方法时使用了常量，`native-image` 也能自动编译这些常量对应的类和方法，比如：

```
Class.forName("java.lang.Integer")
Class.forName("java.lang.Integer", true, ClassLoader.getSystemClassLoader())
Class.forName("java.lang.Integer").getMethod("equals", Object.class)
Integer.class.getDeclaredMethod("bitCount", int.class)
Integer.class.getConstructor(String.class)
Integer.class.getDeclaredConstructor(int.class)
Integer.class.getField("MAX_VALUE")
Integer.class.getDeclaredField("value")
```

下面我们构造一个 `native-image` 无法推断反射信息的示例，比如根据命令行参数来动态的调用某个类的某个方法：

```
public class App {
    
    public static void main( String[] args ) throws Exception {
        if (args.length != 4) {
            System.out.println("Usage: ./app clz method a b");
            return;
        }
        Integer result = callReflection(args[0], args[1], Integer.parseInt(args[2]), Integer.parseInt(args[3]));
        System.out.println(result);
    }

    public static Integer callReflection(String clz, String method, Integer a, Integer b) throws Exception {
        Class<?> clazz = Class.forName(clz);
        return (Integer) clazz.getMethod(method, Integer.class, Integer.class).invoke(null, a, b);
    }
}
```

我们定义一个 `Calculator` 类，实现加减乘除四则运算：

```
public class Calculator {

    public static Integer add(Integer a, Integer b) {
        return a + b;
    }

    public static Integer sub(Integer a, Integer b) {
        return a - b;
    }

    public static Integer mul(Integer a, Integer b) {
        return a * b;
    }

    public static Integer div(Integer a, Integer b) {
        return a / b;
    }
}
```

然后将两个类编译成 `class` 文件：

```
$ javac App.java Calculator.java
```

运行测试：

```
$ java App Calculator add 2 2
4
$ java App Calculator sub 2 2
0
$ java App Calculator mul 2 2
4
$ java App Calculator div 2 2
1
```

我们使用 `native-image` 生成可执行文件：

```
$ native-image App --no-fallback
```

此时的文件运行会报错：

```
$ ./app Calculator add 2 2
Exception in thread "main" java.lang.ClassNotFoundException: Calculator
        at org.graalvm.nativeimage.builder/com.oracle.svm.core.hub.ClassForNameSupport.forName(ClassForNameSupport.java:122)
        at org.graalvm.nativeimage.builder/com.oracle.svm.core.hub.ClassForNameSupport.forName(ClassForNameSupport.java:86)
        at java.base@21.0.2/java.lang.Class.forName(DynamicHub.java:1356)
        at java.base@21.0.2/java.lang.Class.forName(DynamicHub.java:1319)
        at java.base@21.0.2/java.lang.Class.forName(DynamicHub.java:1312)
        at App.callReflection(App.java:13)
        at App.main(App.java:8)
```

可以看出 `native-image` 通过静态分析，是不知道程序会使用 `Calculator` 类的，所以构建二进制文件时并没有包含在里面。为了让 `native-image` 知道 `Calculator` 类的存在，我们新建一个 `META-INF/native-image/reflect-config.json` 配置文件：

```
[
    {
        "name": "Calculator",
        "methods": [
            {
                "name": "add",
                "parameterTypes": [
                    "java.lang.Integer",
                    "java.lang.Integer"
                ]
            }
        ]
    }
]
```

重新编译后，运行正常：

```
$ ./app Calculator add 2 2      
4
```

由于配置文件里我只加了 `add` 方法，所以运行其他方法时，依然会报错：

```
$ ./app Calculator mul 2 2
Exception in thread "main" java.lang.NoSuchMethodException: Calculator.mul(java.lang.Integer, java.lang.Integer)
        at java.base@21.0.2/java.lang.Class.checkMethod(DynamicHub.java:1075)
        at java.base@21.0.2/java.lang.Class.getMethod(DynamicHub.java:1060)
        at App.callReflection(App.java:14)
        at App.main(App.java:8)
```

将所有方法都加到配置文件中即可。

> 注意这里的 `--no-fallback` 参数，防止 `native-image` 开启回退模式（fallback image）。`native-image` 检测到反射时会自动开启回退模式，生成的可执行文件也是可以执行的，但是必须依赖 JDK：
> 
> ```
> % native-image App 
> ...
> Warning: Reflection method java.lang.Class.getMethod invoked at App.callReflection(App.java:14)
> Warning: Aborting stand-alone image build due to reflection use without configuration.
> ...
> Generating fallback image...
> Warning: Image 'app' is a fallback image that requires a JDK for execution (use --no-fallback to suppress fallback image generation and to print more detailed information why a fallback image was necessary).
> ```

## 参考

* [Getting Started with Oracle GraalVM](https://www.graalvm.org/latest/getting-started/)
* [Getting Started with Native Image](https://www.graalvm.org/latest/reference-manual/native-image/)
* [GraalVM Documentation](https://www.graalvm.org/latest/docs/)
* [GraalVM User Guides](https://www.graalvm.org/latest/guides/)
* [How to Build Java Apps with Paketo Buildpacks](https://paketo.io/docs/howto/java/)
* [Containerize a Native Executable and Run in a Container](https://www.graalvm.org/latest/reference-manual/native-image/guides/containerise-native-executable-and-run-in-docker-container/)
* [Include Resources in a Native Executable](https://www.graalvm.org/latest/reference-manual/native-image/guides/include-resources/)
* [Java AOT 编译框架 GraalVM 快速入门](https://strongduanmu.com/blog/java-aot-compiler-framework-graalvm-quick-start.html)
* [Create a GraalVM Docker Image](https://www.baeldung.com/java-graalvm-docker-image)
* [如何借助 Graalvm 和 Picocli 构建 Java 编写的原生 CLI 应用](https://www.infoq.cn/article/4RRJuxPRE80h7YsHZJtX)
* [Runtime efficiency with Spring (today and tomorrow)](https://spring.io/blog/2023/10/16/runtime-efficiency-with-spring)
* [GraalVM for JDK 21 is here!](https://medium.com/graalvm/graalvm-for-jdk-21-is-here-ee01177dd12d)
* [GraalVM Native Image Support](https://docs.spring.io/spring-boot/docs/current/reference/html/native-image.html)
* [初步探索GraalVM--云原生时代JVM黑科技-京东云开发者社区](https://developer.jdcloud.com/article/2446)
* [不同操作系统可执行文件格式](https://www.cnblogs.com/sooooooul/p/17435401.html)

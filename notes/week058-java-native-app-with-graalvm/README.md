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

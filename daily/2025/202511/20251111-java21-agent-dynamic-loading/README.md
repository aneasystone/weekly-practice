# 重温 Java 21 之禁用代理的动态加载

Java Agent 通常被直译为 Java 代理，它是一个 jar 包，这个 jar 包很特别，不能独立运行，而是要依附到我们的目标 JVM 进程中。它利用 JVM 提供的 [Instrumentation API](https://docs.oracle.com/en/java/javase/21/docs/api/java.instrument/java/lang/instrument/Instrumentation.html) 来修改已加载到 JVM 中的字节码，从而实现很多高级功能，比如：

* Eclipse、IntelliJ 等 IDE 的调试功能；
* [JRebel](https://www.jrebel.com/products/jrebel)、[spring-loaded](https://github.com/spring-projects/spring-loaded) 等工具的热加载功能；
* [Arthas](https://arthas.aliyun.com/)、[Btrace](https://github.com/btraceio/btrace)、[Greys](https://github.com/oldmanpushcart/greys-anatomy) 等工具的线上诊断功能；
* [Visual VM](https://visualvm.github.io/)、[JConsole](https://openjdk.org/tools/svc/jconsole/) 等工具的性能分析功能；
* 此外，[SkyWalking](https://skywalking.apache.org/)、[Pinpoint](https://github.com/pinpoint-apm/pinpoint) 等 APM 系统也是基于 Java Agent 实现的；

## Java Agent 简单示例

为了对 Java Agent 的概念有一个更直观的认识，我们从一个简单的示例入手，从零开始实现一个 Java Agent。先创建如下目录结构：

```
├── pom.xml
└── src
  └── main
    ├── java
    │   └── com
    │     └── example
    │       └── AgentDemo.java
    └── resources
      └── META-INF
        └── MANIFEST.MF
```

包含三个主要文件：

* `pom.xml` - Maven 项目的配置文件
* `AgentDemo.java` - Java Agent 的入口类
* `MANIFEST.MF` - 元数据文件，用于描述打包的 JAR 文件中的各种属性和信息

Java Agent 的入口类定义如下：

```java
package com.example;

import java.lang.instrument.Instrumentation;

public class AgentDemo {

  public static void premain(String agentArgs, Instrumentation inst) {
    System.out.println("premain");
  }
}
```

我们知道，常规 Java 程序的入口方法是 `main` 函数，而 Java Agent 的入口方法是 `premain` 函数。其中，`String agentArgs` 是传递给 Agent 的参数，比如当我们运行 `java -javaagent:agent-demo.jar=some-args app.jar` 命名时，参数 `agentArgs` 的值就是字符串 `some-args`；另一个参数 `Instrumentation inst` 是 JVM 提供的修改字节码的接口，我们可以通过这个接口定位到希望修改的类并做出修改。

> **Instrumentation API** 是 Java Agent 的核心，它可以在加载 class 文件之前做拦截，对字节码做修改（`addTransformer`），也可以在运行时对已经加载的类的字节码做变更（`retransformClasses` 或 `redefineClasses`）；Instrumentation 的英文释义是插桩或植入，所以这个操作又被称为 **字节码插桩**，由于这个操作非常的底层，一般会配合一些字节码修改的库，比如 [ASM](https://asm.ow2.io/)、[Javassist](https://www.javassist.org/)、[Byte Buddy](https://bytebuddy.net/) 等。关于 Instrumentation API 是一个较为艰深复杂的话题，本文为简单起见，没有深入展开，感兴趣的同学可以自行查找相关资料。

有了 Java Agent 的入口类之后，我们还需要告诉 JVM 这个入口类的位置，可以在 `MANIFEST.MF` 元数据文件中通过 `Premain-Class` 参数来描述：

```
Premain-Class: com.example.AgentDemo
```

打包的时候，要注意将 `MANIFEST.MF` 文件一起打到 jar 包里，这可以通过打包插件 `maven-assembly-plugin` 来实现：

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-assembly-plugin</artifactId>
  <version>3.6.0</version>
  <configuration>
    <descriptorRefs>
      <descriptorRef>jar-with-dependencies</descriptorRef>
    </descriptorRefs>
    <archive>
      <manifestFile>src/main/resources/META-INF/MANIFEST.MF</manifestFile>
    </archive>
  </configuration>
  <executions>
    <execution>
      <phase>package</phase>
      <goals>
        <goal>single</goal>
      </goals>
    </execution>
  </executions>
</plugin>
```

最后，执行 `mvn clean package` 打包命令，生成 `target/agent-demo-1.0-SNAPSHOT-jar-with-dependencies.jar` 文件，我们就得到了一个最简单的 Java Agent 了。

## Java Agent 的两种加载方式

Java Agent 最常见的使用方式是在运行 `java` 命令时通过 `-javaagent` 参数指定要加载的 Agent 文件：

```
$ java -javaagent:agent-demo-1.0-SNAPSHOT-jar-with-dependencies.jar Hello.java
```

这种方式被称为 **静态加载（static loading）**。在这种情况下，Java Agent 和应用程序一起启动，并在运行主程序的 `main` 方法之前先调用 Java Agent 的 `premain` 方法，下面是程序的运行结果：

```
premain
Hello
```

既然有静态加载，自然就有动态加载。**动态加载（dynamic loading）** 指的是将 Java Agent 动态地加载到已运行的 JVM 进程中，当我们不希望中断生产环境中已经运行的应用程序时，这个特性非常有用。

我们先正常启动一个 Java 应用程序：

```
$ java Hello.java
Hello
```

通过 `jps` 得到该程序的 PID，然后使用 Java 的 [Attach API](https://docs.oracle.com/en/java/javase/21/docs/api/jdk.attach/com/sun/tools/attach/VirtualMachine.html) **附加（attach）** 到该程序上：

```java
String pidOfOtherJVM = "3378";
VirtualMachine vm = VirtualMachine.attach(pidOfOtherJVM);
```

附加成功后得到 `VirtualMachine` 实例，`VirtualMachine` 提供了一个 `loadAgent()` 方法用于动态加载 Java Agent：

```java
File agentJar = new File("/com.docker.devenvironments.code/agent-demo-1.0-SNAPSHOT-jar-with-dependencies.jar");
vm.loadAgent(agentJar.getAbsolutePath());

// do other works

vm.detach();
```

查看应用程序的日志，可以发现如下报错：

```
Failed to find Agent-Class manifest attribute from /com.docker.devenvironments.code/agent-demo.jar
```

这是因为目前我们这个 Java Agent 还不支持动态加载，动态加载的入口并不是 `premain` 函数，而是 `agentmain` 函数，我们在 `AgentDemo` 类中新增代码如下：

```java
...
  public static void agentmain(String agentArgs, Instrumentation inst) {
    System.out.println("agentmain");
  }
...
```

并在 `MANIFEST.MF` 文件中新增 `Agent-Class` 参数：

```
Agent-Class: com.example.AgentDemo
```

重新打包，并再次动态加载，可以在应用程序中看到日志如下：

```
WARNING: A Java agent has been loaded dynamically (/com.docker.devenvironments.code/agent-demo-1.0-SNAPSHOT-jar-with-dependencies.jar)
WARNING: If a serviceability tool is in use, please run with -XX:+EnableDynamicAgentLoading to hide this warning
WARNING: If a serviceability tool is not in use, please run with -Djdk.instrument.traceUsage for more information
WARNING: Dynamic loading of agents will be disallowed by default in a future release
agentmain
```

可以看到 `agentmain` 函数被成功执行，动态加载生效了。

## 禁用 Java Agent 的动态加载

在上面的应用程序日志中，我们可以看到几行 WARNING 提示，这其实就是 Java 21 引入的新内容了，当 JVM 检测到有 Java Agent 被动态加载，就会打印这几行警告信息，告知用户动态加载机制将在未来的版本中默认禁用。如果不想看到这样的日志，可以在启动应用程序时加上 `-XX:+EnableDynamicAgentLoading` 选项：

```
$ java -XX:+EnableDynamicAgentLoading Hello.java
```

那么 Java 21 为什么要禁用 Java Agent 的动态加载呢？这就要提到 Java 所追求的 [Integrity by Default](https://openjdk.org/jeps/8305968) 原则了。Integrity 一般被翻译为 **完整性**，片面的理解就是要保证我们程序中的任何内容，包括数据或代码都是完整的、没有被篡改的。而 Instrumentation API 通过修改已加载到 JVM 中的字节码来改变现有应用程序，在不更改源代码的情况下改变应用程序的行为。当我们静态加载 Java Agent 时，这并不是什么大问题，因为这是用户明确且有意的使用；然而，动态加载则是间接的，它超出了用户的控制范围，可能对用户的应用程序造成严重破坏，很显然并不符合完整性原则。

因此，作为应用程序的所有者，必须有意识地、明确地决定允许和加载哪些 Java Agent：要么使用静态加载，要么通过 `-XX:+EnableDynamicAgentLoading` 选项允许动态加载。

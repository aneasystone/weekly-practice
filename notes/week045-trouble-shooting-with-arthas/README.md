# WEEK045 - 使用 Arthas 排查线上问题

[Arthas](https://arthas.aliyun.com/) 是阿里开源的一款 Java 应用诊断工具，可以在线排查问题，动态跟踪 Java 代码，以及实时监控 JVM 状态。这个工具的大名我早有耳闻，之前一直听别人推荐，却没有使用过。最近在线上遇到了一个问题，由于开发人员在异常处理时没有将线程堆栈打印出来，只是简单地抛出了一个系统错误，导致无法确定异常的具体来源；因为是线上环境，如果要修改代码重新发布，流程会非常漫长，所以只能通过分析代码来定位，正当我看着繁复的代码一筹莫展的时候，突然想到了 Arthas 这个神器，于是尝试着使用 Arthas 来排查这个问题，没想到轻松几步就定位到了原因，上手非常简单，着实让我很吃惊。正所谓 “工欲善其事，必先利其器”，这话果真不假，于是事后花了点时间对 Arthas 的各种用法学习了一番，此为总结。

## 快速入门

如果你处于联网环境，可以直接使用下面的命令下载并运行 Arthas：

```
$ wget https://arthas.aliyun.com/arthas-boot.jar
$ java -jar arthas-boot.jar
```

程序会显示出系统中所有正在运行的 Java 进程，Arthas 为每个进程分配了一个序号：

```
[INFO] JAVA_HOME: C:\Program Files\Java\jdk1.8.0_351\jre
[INFO] arthas-boot version: 3.7.1
[INFO] Found existing java process, please choose one and input the serial number of the process, eg : 1. Then hit ENTER.
* [1]: 9400 .\target\demo-0.0.1-SNAPSHOT.jar
  [2]: 13964 org.eclipse.equinox.launcher_1.6.500.v20230717-2134.jar
  [3]: 6796 org.springframework.ide.vscode.boot.app.BootLanguageServerBootApp
```

从这个列表中找到出问题的那个 Java 进程，并输入相应的序号，比如这里我输入 `1`，然后按下回车，Arthas 就会自动下载完整的包，并 Attach 到目标进程，输出如下：

```
[INFO] Start download arthas from remote server: https://arthas.aliyun.com/download/3.7.1?mirror=aliyun
[INFO] Download arthas success.
[INFO] arthas home: C:\Users\aneasystone\.arthas\lib\3.7.1\arthas
[INFO] Try to attach process 9400
[INFO] Attach process 9400 success.
[INFO] arthas-client connect 127.0.0.1 3658
  ,---.  ,------. ,--------.,--.  ,--.  ,---.   ,---.  
 /  O  \ |  .--. ''--.  .--'|  '--'  | /  O  \ '   .-' 
|  .-.  ||  '--'.'   |  |   |  .--.  ||  .-.  |`.  `-. 
|  | |  ||  |\  \    |  |   |  |  |  ||  | |  |.-'    |
`--' `--'`--' '--'   `--'   `--'  `--'`--' `--'`-----' 

wiki       https://arthas.aliyun.com/doc
tutorials  https://arthas.aliyun.com/doc/arthas-tutorials.html
version    3.7.1
main_class
pid        9400                                                                 
time       2023-09-06 07:16:31

[arthas@9400]$
```

> 下载的 Arthas 包位于 `~/.arthas` 目录，如果你没有联网，需要提前下载完整的包。

> Arthas 偶尔会出现 Attach 不上目标进程的情况，可以查看 `~/logs/arthas` 目录下的日志进行排查。

### 查看所有命令

使用 `help` 可以查看 Arthas 支持的 [所有子命令](https://arthas.aliyun.com/doc/commands.html)：

```
[arthas@9400]$ help
 NAME         DESCRIPTION
 help         Display Arthas Help
 auth         Authenticates the current session
 keymap       Display all the available keymap for the specified connection.
 sc           Search all the classes loaded by JVM
 sm           Search the method of classes loaded by JVM
 classloader  Show classloader info
 jad          Decompile class
 getstatic    Show the static field of a class
 monitor      Monitor method execution statistics, e.g. total/success/failure count, average rt, fail rate, etc.
 stack        Display the stack trace for the specified class and method
 thread       Display thread info, thread stack
 trace        Trace the execution time of specified method invocation.
 watch        Display the input/output parameter, return object, and thrown exception of specified method invocation
 tt           Time Tunnel
 jvm          Display the target JVM information
 memory       Display jvm memory info.
 perfcounter  Display the perf counter information.
 ognl         Execute ognl expression.
 mc           Memory compiler, compiles java files into bytecode and class files in memory.
 redefine     Redefine classes. @see Instrumentation#redefineClasses(ClassDefinition...)
 retransform  Retransform classes. @see Instrumentation#retransformClasses(Class...)
 dashboard    Overview of target jvm's thread, memory, gc, vm, tomcat info.
 dump         Dump class byte array from JVM
 heapdump     Heap dump
 options      View and change various Arthas options
 cls          Clear the screen
 reset        Reset all the enhanced classes
 version      Display Arthas version
 session      Display current session information
 sysprop      Display and change the system properties.
 sysenv       Display the system env.
 vmoption     Display, and update the vm diagnostic options.
 logger       Print logger info, and update the logger level
 history      Display command history
 cat          Concatenate and print files
 base64       Encode and decode using Base64 representation
 echo         write arguments to the standard output
 pwd          Return working directory name
 mbean        Display the mbean information
 grep         grep command for pipes.
 tee          tee command for pipes.
 profiler     Async Profiler. https://github.com/jvm-profiling-tools/async-profiler
 vmtool       jvm tool
 stop         Stop/Shutdown Arthas server and exit the console.
```

这些命令根据功能大抵可以分为以下几类：

* 与 JVM 相关的命令
* 与类加载、类、方法相关的命令
* 统计和观测命令
* 类 Linux 命令
* 其他命令

### 与 JVM 相关的命令

这些命令主要与 JVM 相关，用于查看或修改 JVM 的相关属性，查看 JVM 线程、内存、CPU、GC 等信息：

* [jvm](https://arthas.aliyun.com/doc/jvm.html) - 查看当前 JVM 的信息；
* [sysenv](https://arthas.aliyun.com/doc/sysenv.html) - 查看 JVM 的环境变量；
* [sysprop](https://arthas.aliyun.com/doc/sysprop.html) - 查看 JVM 的系统属性；
* [vmoption](https://arthas.aliyun.com/doc/vmoption.html) - 查看或修改 JVM 诊断相关的参数；
* [memory](https://arthas.aliyun.com/doc/memory.html) - 查看 JVM 的内存信息；
* [heapdump](https://arthas.aliyun.com/doc/heapdump.html) - 将 Java 进程的堆快照导出到某个文件中，方便我们对堆内存进行分析；
* [thread](https://arthas.aliyun.com/doc/thread.html) - 查看所有线程的信息，包括线程名称、线程组、优先级、线程状态、CPU 使用率、堆栈信息等；
* [dashboard](https://arthas.aliyun.com/doc/dashboard.html) - 查看当前系统的实时数据面板，包括了线程、内存、GC 和 Runtime 等信息；可以把它看成是 `thread`、`memory`、`jvm`、`sysenv`、`sysprop` 几个命令的综合体；
* [perfcounter](https://arthas.aliyun.com/doc/perfcounter.html) - 查看当前 JVM 的 Perf Counter 信息； 
* [logger](https://arthas.aliyun.com/doc/logger.html) - 查看应用日志信息，支持动态更新日志级别；
* [mbean](https://arthas.aliyun.com/doc/mbean.html) - 查看或实时监控 Mbean 的信息；
* [vmtool](https://arthas.aliyun.com/doc/vmtool.html) - 利用 JVMTI 接口，实现查询内存对象，强制 GC 等功能；

### 与类加载、类、方法相关的命令

这些命令主要与类加载、类或方法相关，比如在 JVM 中搜索类或类的方法，查看类的静态属性，编译或反编译，对类进行热更新等：

* [classloader](https://arthas.aliyun.com/doc/classloader.html) - 查看 JVM 中所有的 Classloader 信息；
* [dump](https://arthas.aliyun.com/doc/dump.html) - 将指定类导出成 `.class` 字节码文件；
* [jad](https://arthas.aliyun.com/doc/jad.html) - 将指定类反编译成 Java 源码；
* [mc](https://arthas.aliyun.com/doc/mc.html) - 内存编译器，将 Java 源码编译成 `.class` 字节码文件；
* [redefine](https://arthas.aliyun.com/doc/redefine.html) / [retransform](https://arthas.aliyun.com/doc/retransform.html) - 这两个命令都可以对已加载的类进行热更新，但是 `redefine` 和 `jad` / `watch` / `trace` / `monitor` / `tt` 等命令会冲突，而且 `redefine` 后的原来的类不能恢复，所以推荐使用 `retransform` 命令，关于 JDK 中 Redefine 和 Retransform 机制的区别可以参考 [这里](https://lsieun.github.io/java-agent/s01ch03/redefine-vs-retransform.html)；
* [sc](https://arthas.aliyun.com/doc/sc.html) - Search Class，搜索 JVM 中的类；
* [sm](https://arthas.aliyun.com/doc/sm.html) - Search Method，搜索 JVM 中的类的方法；
* [getstatic](https://arthas.aliyun.com/doc/getstatic.html) - 查看类的静态属性；
* [ognl](https://arthas.aliyun.com/doc/ognl.html) - 执行 ognl 表达式；ognl 非常灵活，可以实现很多功能，比如上面的查看或修改系统属性，查看类的静态属性都可以通过 ognl 实现；

### 统计和观测

这些命令可以对类方法的执行情况进行统计和监控，是排查线上问题的利器：

* [monitor](https://arthas.aliyun.com/doc/monitor.html) - 对给定的类方法进行监控，统计其调用次数，调用耗时以及成功率等；
* [stack](https://arthas.aliyun.com/doc/stack.html) - 查看一个方法的执行调用堆栈；
* [trace](https://arthas.aliyun.com/doc/trace.html) - 对给定的类方法进行监控，输出该方法的调用耗时，和 `monitor` 的区别在于，它还能跟踪一级方法的调用链路和耗时，帮助快速定位性能问题；
* [watch](https://arthas.aliyun.com/doc/watch.html) - 观测指定方法的执行数据，包括方法的入参、返回值、抛出的异常等；
* [tt](https://arthas.aliyun.com/doc/tt.html) - 和 `watch` 命令一样，`tt` 也可以观测指定方法的执行数据，但 `tt` 是将每次的执行情况都记录下来，然后再针对每次调用进行排查和分析，所以叫做 Time Tunnel；
* [reset](https://arthas.aliyun.com/doc/reset.html) - 上面这些与统计观测相关的命令都是通过 **字节码增强技术** 来实现的，会在指定类的方法中插入一些切面代码，因此在生产环境诊断结束后，记得执行 `reset` 命令重置增强过的类（或执行 `stop` 命令）；
* [profiler](https://arthas.aliyun.com/doc/profiler.html) - 使用 [async-profiler](https://github.com/async-profiler/async-profiler) 对应用采样，并将采样结果生成火焰图；
* [jfr](https://arthas.aliyun.com/doc/jfr.html) - 动态开启关闭 JFR 记录，生成的 jfr 文件可以通过 [JDK Mission Control](https://www.oracle.com/javase/jmc/) 进行分析；

### Arthas 命令与 JDK 工具的对比

在 [week028-jvm-diagnostic-tools](../week028-jvm-diagnostic-tools/README.md) 这篇笔记中我总结了很多 JDK 自带的诊断工具，其实有很多 Arthas 命令和那些 JDK 工具的功能是类似的，只是 Arthas 在输出格式上做了优化，让输出的内容更加美观和易读，而且在功能上做了增强。

| Arthas 命令 | JDK 工具 | 对比 |
| ---------- | -------- | ---- |
| `sysprop` | `jinfo -sysprops` | 都可以查看 JVM 的系统属性，但是 `sysprop` 比 `jinfo` 强的是，它还能修改系统属性 |
| `vmoption` | `jinfo -flag` | 都可以查看 JVM 参数，但是 `vmoption` 只显示诊断相关的参数，比如 `HeapDumpOnOutOfMemoryError`、`PrintGC` 等 |
| `memory` | `jmap -heap` | 都可以查看 JVM 的内存信息，但是 `memory` 以表格形式显示，方便用户阅读 |
| `heapdump` | `jmap -dump` | 都可以导出进程的堆内存，只是它在使用上更加简洁 |
| `thread` | `jstack` | 都可以列出 JVM 的所有线程，但是 `thread` 以表格形式显示，方便用户阅读，而且增加了 CPU 使用率的功能，可以方便我们快速找出当前最忙的线程 |
| `perfcounter` | `jcmd PerfCounter.print` | 都可以查看 JVM 进程的性能统计信息 |
| `classloader` | `jmap -clstats` | 都可以查看 JVM 的 Classloader 统计信息，但是 `classloader` 命令还支持以树的形式查看，另外它还支持查看每个 Classloader 实际的 URL，通过 Classloader 查找资源等 |
| `jfr` | `jcmd JFR.start` | 都可以开启或关闭 JFR 记录，并生成的 jfr 文件 |

### 类 Linux 命令

除了上面那些用于问题诊断的命令，Arthas 还提供了一些类 Linux 命令，方便我们在 Arthas 终端中使用，比如：

* [base64](https://arthas.aliyun.com/doc/base64.html) - 执行 base64 编码和解码；
* [cat](https://arthas.aliyun.com/doc/cat.html) - 打印文件内容；
* [cls](https://arthas.aliyun.com/doc/cls.html) - 清空当前屏幕区域；
* [echo](https://arthas.aliyun.com/doc/echo.html) - 打印参数；
* [grep](https://arthas.aliyun.com/doc/grep.html) - 使用字符串或正则表达式搜索文本，并输出匹配的行；
* [history](https://arthas.aliyun.com/doc/history.html) - 输出历史命令；
* [pwd](https://arthas.aliyun.com/doc/pwd.html) - 输出当前的工作目录；
* [tee](https://arthas.aliyun.com/doc/tee.html) - 从 stdin 读取数据，并同时输出到 stdout 和文件；
* `wc` - 暂时只支持 `wc -l`，统计输出的行数；

此外，Arthas 还支持在后台运行任务，仿照 Linux 中的相关命令，我们可以使用 `&` 在后台运行任务，使用 `jobs` 列出所有后台任务，使用 `Ctrl + Z` 暂停任务，使用 `bg` 和 `fg` 将暂停的任务转到后台或前台继续运行，使用 `kill` 终止任务。具体内容可以参考 [Arthas 后台异步任务](https://arthas.aliyun.com/doc/async.html)。

### 其他命令

还有一些与 Arthas 本身相关的命令，比如查看 Arthas 的版本号、配置、会话等信息：

* [version](https://arthas.aliyun.com/doc/version.html) - 查看 Arthas 版本号；
* [options](https://arthas.aliyun.com/doc/options.html) - 查看或修改 Arthas 全局配置；
* [keymap](https://arthas.aliyun.com/doc/keymap.html) - 查看当前所有绑定的快捷键，可以通过 `~/.arthas/conf/inputrc` 文件自定义快捷键；
* [session](https://arthas.aliyun.com/doc/session.html) - 查看当前会话信息；
* [auth](https://arthas.aliyun.com/doc/auth.html) - 验证当前会话；
* [quit](https://arthas.aliyun.com/doc/quit.html) - 退出当前 Arthas 客户端，其他 Arthas 客户端不受影响；
* [stop](https://arthas.aliyun.com/doc/stop.html) - 关闭 Arthas 服务端，所有 Arthas 客户端全部退出；这个命令会重置掉所有的增强类（除了 `redefine` 的类）；

## 线上问题排查

### 使用 `watch` 监听函数出入参和异常

```
$ curl -X POST -H "Content-Type: application/json" -d '{"x":1,"y":2}' http://localhost:8080/add
3
```

```
$ curl -X POST -H "Content-Type: application/json" -d '{"x":1}' http://localhost:8080/add
系统错误！
```


### 使用 `jad/sc/redefine` 热更新代码

### 使用 `logger` 动态更新日志级别

### 使用 `ognl` 调用 Spring Bean

https://github.com/alibaba/arthas/issues/482

### 排查类冲突问题

### 使用 `trace` 排查性能问题

## 参考

* [Arthas 文档](https://arthas.aliyun.com/doc/)
* [OGNL 参考文档](https://commons.apache.org/proper/commons-ognl/language-guide.html)
* [Arthas 在线教程 - Killercoda](https://killercoda.com/arthas/course/arthas-tutorials-cn)
* [redefine VS. retransform](https://lsieun.github.io/java-agent/s01ch03/redefine-vs-retransform.html)

## 更多

### 深入 Arthas 实现原理

* [谈谈阿里arthas背后的原理](https://developer.aliyun.com/article/1004682)
* [Arthas运行原理](https://zhuanlan.zhihu.com/p/115127052)
* [Arthas原理系列(五)：watch命令的实现原理](https://juejin.cn/post/6908874607474769934)
* [Arthas原理：如何做到与应用代码隔离？](https://yeas.fun/archives/arthas-isolation)

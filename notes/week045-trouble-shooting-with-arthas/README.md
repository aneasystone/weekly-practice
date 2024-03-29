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

了解了 Arthas 的命令之后，接下来总结一些使用 Arthas 对常见问题的排查思路。

### 使用 `watch` 监听方法出入参和异常

相信不少人见过类似下面这样的代码，在遇到异常情况时直接返回系统错误，而没有将异常信息和堆栈打印出来：

```
@PostMapping("/add")
public String add(@RequestBody DemoAdd demoAdd) {
  try {
    Integer result = demoService.add(demoAdd);
    return String.valueOf(result);
  } catch (Exception e) {
    return "系统错误！";
  }
}
```

有时候只打印了异常信息 `e.getMessage()`，但是一看日志全是 `NullPointerException`，一旦出现异常，根本不知道是哪行代码出了问题。这时，Arthas 的 `watch` 命令就可以派上用场了：

```
$ watch com.example.demo.service.DemoService add -x 2
Press Q or Ctrl+C to abort.
Affect(class count: 1 , method count: 1) cost in 143 ms, listenerId: 1
```

我们对 `demoService.add()` 方法进行监听，当遇到正常请求时：

```
$ curl -X POST -H "Content-Type: application/json" -d '{"x":1,"y":2}' http://localhost:8080/add
3
```

`watch` 的输出如下：

```
method=com.example.demo.service.DemoService.add location=AtExit
ts=2023-09-11 08:00:46; [cost=1.4054ms] result=@ArrayList[
    @Object[][
        @DemoAdd[DemoAdd(x=1, y=2)],
    ],
    @DemoService[
    ],
    @Integer[3],
]
```

`location=AtExit` 表示这个方法正常结束，`result` 表示方法在结束时的变量值，默认只监听方法的入参、方法所在的实例对象、以及方法的返回值。

当遇到异常请求时：

```
$ curl -X POST -H "Content-Type: application/json" -d '{"x":1}' http://localhost:8080/add
系统错误！
```

`watch` 的输出如下：

```
method=com.example.demo.service.DemoService.add location=AtExceptionExit
ts=2023-09-11 08:05:20; [cost=0.1402ms] result=@ArrayList[
    @Object[][
        @DemoAdd[DemoAdd(x=1, y=null)],
    ],
    @DemoService[
    ],
    null,
]
```

可以看到 `location=AtExceptionExit` 表示这个方法抛出了异常，同样地，`result` 默认只监听方法的入参、方法所在的实例对象、以及方法的返回值。那么能不能拿到具体的异常信息呢？当然可以，通过自定义观察表达式可以轻松实现。

默认情况下，`watch` 命令使用的观察表达式为 `{params, target, returnObj}`，所以输出结果里并没有异常信息，我们将观察表达式改为 `{params, target, returnObj, throwExp}` 重新监听：

```
$ watch com.example.demo.service.DemoService add "{params, target, returnObj, throwExp}" -x 2
```

此时就可以输出具体的异常信息了：

```
method=com.example.demo.service.DemoService.add location=AtExceptionExit
ts=2023-09-11 08:11:19; [cost=0.0961ms] result=@ArrayList[
    @Object[][
        @DemoAdd[DemoAdd(x=1, y=null)],
    ],
    @DemoService[
    ],
    null,
    java.lang.NullPointerException
        at com.example.demo.service.DemoService.add(DemoService.java:11)
        at com.example.demo.controller.DemoController.add(DemoController.java:20)
    ,
]
```

> 观察表达式其实是一个 ognl 表达式，可以观察的维度也比较多，参考 [表达式核心变量](https://arthas.aliyun.com/doc/advice-class.html)。

从上面的例子可以看到，使用 `watch` 命令有一个很不方便的地方，我们需要提前写好观察表达式，当忘记写表达式或表达式写得不对时，就有可能没有监听到我们的调用，或者虽然监听到调用却没有得到我们想要的内容，这样我们就得反复调试。所以 Arthas 又推出了一个 `tt` 命令，名为 **时空隧道（Time Tunnel）**。

使用 `tt` 命令时大多数情况下不用太关注观察表达式，直接监听类方法即可：

```
$ tt -t com.example.demo.service.DemoService add
```

`tt` 会自动地将所有调用都保存下来，直到用户按下 `Ctrl+C` 结束监听；注意如果方法的调用非常频繁，记得用 `-n` 参数限制记录的次数，防止记录太多导致内存爆炸：

```
$ tt -t com.example.demo.service.DemoService add -n 10
```

当监听结束后，使用 `-l` 参数查看记录列表：

```
$ tt -l
 INDEX  TIMESTAMP            COST(ms)  IS-RET  IS-EXP  OBJECT       CLASS                    METHOD                   
------------------------------------------------------------------------------------------------------------
 1000   2023-09-15 07:51:10  0.8111     true   false  0x62726348   DemoService              add
 1001   2023-09-15 07:51:16  0.1017     false  true   0x62726348   DemoService              add
```

其中 `INDEX` 列非常重要，我们可以使用 `-i` 参数指定某条记录查看它的详情：

```
$ tt -i 1000
 INDEX          1000
 GMT-CREATE     2023-09-15 07:51:10
 COST(ms)       0.8111
 OBJECT         0x62726348
 CLASS          com.example.demo.service.DemoService
 METHOD         add
 IS-RETURN      true
 IS-EXCEPTION   false
 PARAMETERS[0]  @DemoAdd[
                    x=@Integer[1],
                    y=@Integer[2],
                ]
 RETURN-OBJ     @Integer[3]
Affect(row-cnt:1) cost in 0 ms.
```

从输出中可以看到方法的入参和返回值，如果方法有异常，异常信息也不会丢了：

```
$ tt -i 1001
 INDEX            1001                                                                                      
 GMT-CREATE       2023-09-15 07:51:16
 COST(ms)         0.1017
 OBJECT           0x62726348
 CLASS            com.example.demo.service.DemoService                                                      
 METHOD           add
 IS-RETURN        false
 IS-EXCEPTION     true
 PARAMETERS[0]    @DemoAdd[
                      x=@Integer[1],                                                                        
                      y=null,
                  ]
                        at com.example.demo.service.DemoService.add(DemoService.java:21)
                        at com.example.demo.controller.DemoController.add(DemoController.java:21)
                        ...
Affect(row-cnt:1) cost in 13 ms.
```

`tt` 命令记录了所有的方法调用，方便我们回溯，所以被称为时空隧道，而且，由于它保存了当时调用的所有现场信息，所以我们还可以主动地对一条历史记录进行重做，这在复现某些不常见的 BUG 时非常有用：

```
$ tt -i 1000 -p
 RE-INDEX       1000
 GMT-REPLAY     2023-09-15 07:52:31
 OBJECT         0x62726348
 CLASS          com.example.demo.service.DemoService
 METHOD         add
 PARAMETERS[0]  @DemoAdd[
                    x=@Integer[1],
                    y=@Integer[2],
                ]
 IS-RETURN      true
 IS-EXCEPTION   false
 COST(ms)       0.1341
 RETURN-OBJ     @Integer[3]
Time fragment[1000] successfully replayed 1 times.
```

另外，由于 `tt` 保存了当前环境的对象引用，所以我们甚至可以通过这个对象引用来调用它的方法：

```
$ tt -i 1000 -w 'target.properties()' -x 2
@DemoProperties[
    title=@String[demo title],
]
Affect(row-cnt:1) cost in 148 ms.
```

### 使用 `logger` 动态更新日志级别

在 [week014-spring-boot-actuator](../week014-spring-boot-actuator/README.md) 这篇笔记中，我们学习过 Spring Boot Actuator 内置了一个 `/loggers` 端点，可以查看或修改 logger 的日志等级，比如下面这个 POST 请求将 `com.example.demo` 的日志等级改为 `DEBUG`：

```
$ curl -s -X POST -d '{"configuredLevel": "DEBUG"}' \
  -H "Content-Type: application/json" \
  http://localhost:8080/actuator/loggers/com.example.demo
```

使用这种方法修改日志级别可以不重启目标程序，这在线上问题排查时非常有用，但是有时候我们会遇到一些没有开启 Actuator 功能的 Java 程序，这时就可以使用 Arthas 的 `logger` 命令，实现类似的效果。

直接输入 `logger` 命令，查看程序所有的 logger 信息：

```
$ logger
 name                    ROOT
 class                   ch.qos.logback.classic.Logger
 classLoader             org.springframework.boot.loader.LaunchedURLClassLoader@6433a2
 classLoaderHash         6433a2
 level                   INFO
 effectiveLevel          INFO
 additivity              true
 codeSource              jar:file:/D:/demo/target/demo-0.0.1-SNAPSHOT.jar!/BOOT
                         -INF/lib/logback-classic-1.2.10.jar!/
 appenders               name            CONSOLE
                         class           ch.qos.logback.core.ConsoleAppender
                         classLoader     org.springframework.boot.loader.LaunchedURLClassLoader@6433a2
                         classLoaderHash 6433a2
                         target          System.out
```

默认情况下只会打印有 appender 的 logger 信息，可以加上 `--include-no-appender` 参数打印所有的 logger 信息，不过这个输出会很长，通常使用 `-n` 参数打印指定 logger 的信息：

```
$ logger -n com.example.demo
 name                    com.example.demo
 class                   ch.qos.logback.classic.Logger
 classLoader             org.springframework.boot.loader.LaunchedURLClassLoader@6433a2
 classLoaderHash         6433a2
 level                   null
 effectiveLevel          INFO
 additivity              true
 codeSource              jar:file:/D:/demo/target/demo-0.0.1-SNAPSHOT.jar!/BOOT 
                         -INF/lib/logback-classic-1.2.10.jar!/
```

可以看到 `com.example.demo` 的日志级别是 `null`，说明并没有设置，我们可以使用 `-l` 参数来修改它：

```
$ logger -n com.example.demo -l debug
Update logger level fail. Try to specify the classloader with the -c option. 
Use `sc -d CLASSNAME` to find out the classloader hashcode.
```

需要注意的是，默认情况下，`logger` 命令会在 `SystemClassloader` 下执行，如果应用是传统的 war 应用，或者是 Spring Boot 的 fat jar 应用，那么需要指定 classloader。在上面执行 `logger -n` 时，输出中的 classLoader 和 classLoaderHash 这两行很重要，我们可以使用 `-c <classLoaderHash>` 来指定 classloader：

```
$ logger -n com.example.demo -l debug -c 6433a2
Update logger level success.
```

也可以直接使用 `--classLoaderClass <classLoader>` 来指定 classloader：

```
$ logger -n com.example.demo -l debug --classLoaderClass org.springframework.boot.loader.LaunchedURLClassLoader
Update logger level success.
```

### 使用 `ognl` 查看系统属性和应用配置

有时候我们会在线上环境遇到一些莫名奇妙的问题：比如明明数据库地址配置得好好的，但是程序却报数据库连接错误；又或者明明在配置中心对配置进行了修改，但是程序中却似乎始终不生效；这时我们不确定到底是程序本身逻辑的问题，还是程序没有加载到正确的配置，如果能将程序加载的配置信息打印出来，这个问题就很容易排查了。

如果程序使用了 `System.getenv()` 来获取环境变量，我们可以使用 `sysenv` 来进行确认：

```
$ sysenv JAVA_HOME
 KEY                          VALUE 
---------------------------------------------------------------
 JAVA_HOME                    C:\Program Files\Java\jdk1.8.0_351
```

如果程序使用了 `System.getProperties()` 来获取系统属性，我们可以使用 `sysprop` 来进行确认：

```
$ sysprop file.encoding
 KEY                          VALUE  
-----------------------------------
 file.encoding                GBK
```

如果发现系统属性的值有问题，可以使用 `sysprop` 对其动态修改：

```
$ sysprop file.encoding UTF-8
Successfully changed the system property.
 KEY                          VALUE  
-----------------------------------
 file.encoding                UTF-8
```

实际上，无论是 `sysenv` 还是 `sysprop`，我们都可以使用 `ognl` 命令实现：

```
$ ognl '@System@getenv("JAVA_HOME")'
@String[C:\Program Files\Java\jdk1.8.0_351]
$ 
$ ognl '@System@getProperty("file.encoding")'
@String[UTF-8]
```

[OGNL](https://en.wikipedia.org/wiki/OGNL) 是 Object Graphic Navigation Language 的缩写，表示对象图导航语言，它是一种表达式语言，用于访问对象属性、调用对象方法等，它被广泛集成在各大框架中，如 Struts2、MyBatis、Thymeleaf、Spring Web Flow 等。

除了环境变量和系统属性，应用程序本身的配置文件也常常需要排查，在 Spring Boot 程序中，应用配置非常灵活，当存在多个配置文件时，往往搞不清配置是否生效了。这时我们也可以通过 `ognl` 命令来查看配置，不过使用 `ognl` 有一个限制，它只能访问静态方法，所以我们在代码中要实现一个 `SpringUtils.getBean()` 静态方法，这个方法通过 `ApplicationContext` 来获取 Spring Bean：

```
@Component
public class SpringUtils implements ApplicationContextAware {

    private static ApplicationContext CONTEXT;

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        CONTEXT = applicationContext;
    }
    
    public static Object getBean(String beanName) {
        return CONTEXT.getBean(beanName);
    }
}
```

这样我们就可以通过 `ognl` 来查看应用程序的配置类了：

```
$ ognl '@com.example.demo.utils.SpringUtils@getBean("demoProperties")'
@DemoProperties[
    title=@String[demo title],
]
```

那么如果我们的代码中没有 `SpringUtils.getBean()` 这样的静态方法怎么办呢？

在上面我们学到 Arthas 里有一个 `tt` 命令，可以记录方法调用的所有现场信息，并可以使用 `ognl` 表达式对现场信息进行查看；这也就意味着我们可以调用监听目标对象的方法，如果监听目标对象有类似于 `getBean()` 或 `getApplicationContext()` 这样的方法，那么我们就可以间接地获取到 Spring Bean。在 Spring MVC 程序中，`RequestMappingHandlerAdapter` 就是这样绝佳的一个监听对象，每次处理请求时都会调用它的 `invokeHandlerMethod()` 方法，我们对这个方法进行监听：

```
$ tt -t org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter invokeHandlerMethod
Press Q or Ctrl+C to abort.
Affect(class count: 1 , method count: 1) cost in 43 ms, listenerId: 2
 INDEX  TIMESTAMP            COST(ms)  IS-RET  IS-EXP  OBJECT       CLASS                    METHOD
------------------------------------------------------------------------------------------------------------
 1002   2023-09-15 07:59:27  3.5448     true   false   0x57023e7    RequestMappingHandlerAd  invokeHandlerMethod
```

因为这个对象有 `getApplicationContext()` 方法，所以可以通过 `tt -w` 来调用它，从而获取配置 Bean 的内容：

```
$ tt -i 1002 -w 'target.getApplicationContext().getBean("demoProperties")'
@DemoProperties[
    title=@String[demo title],
]
Affect(row-cnt:1) cost in 3 ms.
```

### 使用 `jad/sc/retransform` 热更新代码

有时候我们排查出问题原因后，发现只需一个小小的改动就可以修复问题，可能是加一行判空处理，或者是修复一处逻辑错误；又或者问题太复杂一时排查不出结果，需要加几行调试代码来方便问题的定位；如果修改代码，再重新发布到生产环境，耗时会非常长，而且重启服务也可能会影响到当前的用户。在比较紧急的情况下，热更新功能就可以排上用场了，不用重启服务就能在线修改代码逻辑。

热更新代码一般分为下面四个步骤：

第一步，使用 `jad` 命令将要修改的类反编译成 `.java` 文件：

```
$ jad --source-only com.example.demo.service.DemoService > /tmp/DemoService.java
```

第二步，修改代码：

```
$ vi /tmp/DemoService.java
```

比如我们在 `add()` 方法中加入判空处理：

```
           public Integer add(DemoAdd demoAdd) {
                if (demoAdd.getX() == null) {
                    demoAdd.setX(0);
                }
                if (demoAdd.getY() == null) {
                    demoAdd.setY(0);
                }
/*20*/         log.debug("x = {}, y = {}", (Object)demoAdd.getX(), (Object)demoAdd.getY());
/*21*/         return demoAdd.getX() + demoAdd.getY();
           }
```

第三步，使用 `mc` 命令将修改后的 `.java` 文件编译成 `.class` 字节码文件：

```
$ mc /tmp/DemoService.java -d /tmp
Memory compiler output:
D:\tmp\com\example\demo\service\DemoService.class
Affect(row-cnt:1) cost in 1312 ms.
```

> `mc` 命令有时会失败，这时我们可以在本地开发环境修改代码，并编译成 `.class` 文件，再上传到服务器上。

最后一步，使用 `redefine` 或 `retransform` 对类进行热更新：

```
$ retransform /tmp/com/example/demo/service/DemoService.class
retransform success, size: 1, classes:
com.example.demo.service.DemoService
```

`redefine` 和 `retransform` 都可以热更新，但是 `redefine` 和 `jad` / `watch` / `trace` / `monitor` / `tt` 等命令冲突，所以推荐使用 `retransform` 命令。热更新成功后，使用异常请求再请求一次，现在不会报系统错误了：

```
$ curl -X POST -H "Content-Type: application/json" -d '{"x":1}' http://localhost:8080/add
1
```

如果要还原所做的修改，那么只需要删除这个类对应的 `retransform entry`，然后再重新触发 `retransform` 即可：

```
$ retransform --deleteAll
$ retransform --classPattern com.example.demo.service.DemoService
```

> 不过要注意的是，Arthas 的热更新也并非无所不能，它也有一些限制，比如不能修改、添加、删除类的字段和方法，只能在原来的方法上修改逻辑。

> 另外，在生产环境热更新代码并不是很好的行为，而且还非常危险，一定要严格地控制，上线规范也同样重要。

### 其他使用场景

Arthas 的使用非常灵活，有时候甚至还会有一些意想不到的功能，除了上面这些使用场景，Arthas 的 Issues 中还收集了一些 [用户案例](https://github.com/alibaba/arthas/issues?q=label%3Auser-case)，其中有几个案例对我印象很深，非常有启发性，可供参考。

* [使用 `stack` 命令定位 `System.exit/System.gc` 的调用来源](https://github.com/alibaba/arthas/issues/20)
* [使用 `sc` 和 `jad` 排查 `NoSuchMethodError` 问题](https://github.com/alibaba/arthas/issues/160)
* [使用 `redefine` 修改 `StringBuilder.toString()` 定位未知的日志来源](https://github.com/alibaba/arthas/issues/263)
* [使用 `trace javax.servlet.Servlet/Filter` 排查 Spring Boot 应用 404/401 问题](https://github.com/alibaba/arthas/issues/429)
* [使用 `tt` 定位 Java 应用 CPU 负载过高问题](https://github.com/alibaba/arthas/issues/1202)
* [使用 `profiler` 做复杂链路分析，排查性能问题](https://github.com/alibaba/arthas/issues/1416)
* [使用 `trace` 命令将接口性能优化十倍](https://github.com/alibaba/arthas/issues/1892)

## 参考

* [Arthas 文档](https://arthas.aliyun.com/doc/)
* [OGNL 参考文档](https://commons.apache.org/proper/commons-ognl/language-guide.html)
* [Arthas 在线教程 - Killercoda](https://killercoda.com/arthas/course/arthas-tutorials-cn)
* [redefine VS. retransform](https://lsieun.github.io/java-agent/s01ch03/redefine-vs-retransform.html)
* [Alibaba Arthas实践--获取到Spring Context，然后为所欲为](https://github.com/alibaba/arthas/issues/482)
* [Arthas 用户案例](https://github.com/alibaba/arthas/issues?q=label%3Auser-case)
* [使用 SkyWalking & Arthas 优化微服务性能](https://github.com/alibaba/arthas/issues/1653)

## 更多

### 深入 Arthas 实现原理

* [谈谈阿里arthas背后的原理](https://developer.aliyun.com/article/1004682)
* [Arthas运行原理](https://zhuanlan.zhihu.com/p/115127052)
* [Arthas原理系列(五)：watch命令的实现原理](https://juejin.cn/post/6908874607474769934)
* [Arthas原理：如何做到与应用代码隔离？](https://yeas.fun/archives/arthas-isolation)

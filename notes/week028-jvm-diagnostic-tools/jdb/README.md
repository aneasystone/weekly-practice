## jdb - The Java Debugger

在软件开发的过程中，可以说调试是一项基本技能。调试的英文单词为 `debug` ，顾名思义，**就是去除 bug 的意思**。俗话说得好，编程就是制造 bug 的过程，所以 debug 的重要性毋庸置疑，如果能熟练掌握调试技能，也就可以很快地定位出代码中的 bug。要知道，看得懂代码不一定写得出代码，写得出代码不一定能调试好代码，为了能写出没有 bug 的代码，我们必须得掌握一些基本的调试技巧。

工欲善其事，必先利其器。无论你的开发工具是 `IntelliJ IDEA`、`Eclipse` 还是 `VS Code`，调试器都是标配。在遇到有问题的程序时，合理地利用调试器的跟踪和断点技巧，可以很快地定位出问题原因。虽然说合理利用日志也可以方便定位线上问题，但是日志并不是调试工具，不要在开发环境把 `System.out.println` 当作调试手段，掌握调试器自带的调试技能才是正道。

相信很多人都听过 `gdb`，这可以说是调试界的鼻祖，以前在学习 C/C++ 的时候，就是使用它来调试程序的。和 `gdb` 一样，`jdb` 也是一个命令行版的调试器，用于调试 Java 程序，而且 `jdb` 不需要安装下载，它是 JDK 自带的工具（在 JDK 的 bin 目录中，JRE 中没有）。

### `jdb` 基本命令

在 `jdb` 中调试 Java 程序非常简单，如果 `classpath` 是当前目录，我们直接使用 `jdb MainClass` 命令加载程序即可，如果 `classpath` 不是当前目录，需要通过 `-classpath` 参数来指定。另外，还可以通过 `-sourcepath` 参数来指定源码目录，这样方便我们对照着源码来进行调试。对于 Maven 项目来说，`classpath` 就是 `.\target\classes\` 目录，`sourcepath` 就是 `.\src\main\java\` 目录：

```
$ jdb -classpath .\target\classes\ -sourcepath .\src\main\java\ com.example.DemoApp
```

`classpath` 也可以设置成我们构建的 jar 包：

```
$ jdb -classpath .\target\demo-1.0-SNAPSHOT.jar -sourcepath .\src\main\java\ com.example.DemoApp
```

执行 `jdb` 命令之后，程序这时并没有运行起来，而是停在那里等待进一步的命令。这个时候我们可以想好在哪里下个断点，譬如使用 `stop in` 在 `main()` 函数处下个断点，然后再使用 `run` 命令运行程序：

```
> stop in com.example.DemoApp.main
正在延迟断点com.example.DemoApp.main。
将在加载类后设置。
> run
运行com.example.DemoApp
设置未捕获的java.lang.Throwable
设置延迟的未捕获的java.lang.Throwable
>
VM 已启动: 设置延迟的断点com.example.DemoApp.main

断点命中: "线程=main", com.example.DemoApp.main(), 行=12 bci=0
12            Thread threada = new Thread(() -> {

main[1]
```

可以看出在执行 `run` 命令之前，程序都还没有开始运行，这个时候的断点叫做 **延迟断点**，当程序真正运行起来时，也就是 JVM 启动的时候，才将断点设置上。除了 `stop in Class.Method` 命令，还可以使用 `stop at Class:LineNumber` 的方式来设置断点：

```
main[1] stop at com.example.DemoApp:46
设置断点com.example.DemoApp:46
```

使用 `cont` 命令继续执行代码：

```
main[1] cont
> 
断点命中: "线程=main", com.example.DemoApp.main(), 行=46 bci=26
46            threada.setName("Thread-A");
```

在断点处，可以使用 `list` 命令查看断点附近的代码：

```
main[1] list
42                    lock1.unlock();
43                    System.out.println("[Thread-B] lock2 and lock1 is unlocked");
44                }
45            });
46 =>         threada.setName("Thread-A");
47            threada.start();
48            threadb.setName("Thread-B");
49            threadb.start();
50        }
51    }
```

使用 `print` 命令打印变量或表达式的值：

```
main[1] print threada
 threada = "Thread[Thread-0,5,main]"
```

使用 `dump` 命令打印对象类型的变量：

```
main[1] dump threada
 threada = {        
    name: "Thread-0"
    priority: 5     
    threadQ: null   
    eetop: 0
    single_step: false
    daemon: false
    stillborn: false
    target: instance of com.example.DemoApp$$Lambda$1.401424608(id=648)
    group: instance of java.lang.ThreadGroup(name='main', id=649)
    contextClassLoader: instance of sun.misc.Launcher$AppClassLoader(id=650)
    inheritedAccessControlContext: instance of java.security.AccessControlContext(id=651)
    threadInitNumber: 2
    threadLocals: null
    inheritableThreadLocals: null
    stackSize: 0
    nativeParkEventPointer: 0
    tid: 14
    threadSeqNumber: 15
    threadStatus: 0
    parkBlocker: null
    blocker: null
    blockerLock: instance of java.lang.Object(id=652)
    MIN_PRIORITY: 1
    NORM_PRIORITY: 5
    MAX_PRIORITY: 10
    EMPTY_STACK_TRACE: instance of java.lang.StackTraceElement[0] (id=653)
    SUBCLASS_IMPLEMENTATION_PERMISSION: instance of java.lang.RuntimePermission(id=654)
    uncaughtExceptionHandler: null
    defaultUncaughtExceptionHandler: null
    threadLocalRandomSeed: 0
    threadLocalRandomProbe: 0
    threadLocalRandomSecondarySeed: 0
}
```

`locals` 命令查看当前方法中的所有变量：

```
main[1] locals
方法参数:
args = instance of java.lang.String[0] (id=655)
本地变量:
threada = instance of java.lang.Thread(name='Thread-0', id=645)
threadb = instance of java.lang.Thread(name='Thread-1', id=656)
```

或者使用 `step` 命令单步执行，`cont` 命令继续执行代码，可以使用 `help` 查看所有的命令清单，或者参考 [jdb 的官方文档](http://docs.oracle.com/javase/7/docs/technotes/tools/windows/jdb.html)。

> 如果没有源码，虽然在 jdb 里也可以用 step 来单步，但是没有办法显示当前正在运行的代码，这简直就是盲调。这个时候只能使用字节码调试工具了，常见的字节码调试器有：[Bytecode Visualizer](http://www.drgarbage.com/bytecode-visualizer/)、[JSwat Debugger](https://github.com/nlfiedler/jswat)、[Java ByteCode Debugger (JBCD)](http://sourceforge.net/projects/jbcd/) 等等，参考[这里](https://reverseengineering.stackexchange.com/questions/7991/java-class-bytecode-debugger)。
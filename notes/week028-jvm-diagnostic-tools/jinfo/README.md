## jinfo - JVM Configuration Info

`jinfo` 命令用于查看 Java 应用的 JVM 参数，它和 `jps -v` 的作用类似，但是不同的是，`jps` 只能看到显式指定的参数，而 `jinfo` 可以看到未被显式指定的参数。在很多情况下，我们启动 Java 应用时不会指定所有的 JVM 参数，未指定的 JVM 参数会采用默认值，但是默认值是多少，我们不得不去翻阅官方文档，有了 `jinfo` 我们就可以很方便地知道某个 JVM 参数的默认值了。另外，`jinfo` 还支持在运行时动态地修改某些 JVM 参数。

它的命令格式如下：

```
$ jinfo -help
Usage:
    jinfo [option] <pid>
        (to connect to running process)
    jinfo [option] <executable <core>
        (to connect to a core file)
    jinfo [option] [server_id@]<remote server IP or hostname>
        (to connect to remote debug server)

where <option> is one of:
    -flag <name>         to print the value of the named VM flag
    -flag [+|-]<name>    to enable or disable the named VM flag
    -flag <name>=<value> to set the named VM flag to the given value
    -flags               to print VM flags
    -sysprops            to print Java system properties
    <no option>          to print both of the above
    -h | -help           to print this help message
```

### `jinfo -flags <pid>`

`-flags` 参数用于显示所有 JVM 参数。

```
$ jinfo -flags 3452
Non-default VM flags: -XX:CICompilerCount=4 -XX:InitialHeapSize=104857600 -XX:MaxHeapSize=524288000 -XX:MaxNewSize=174587904 -XX:MinHeapDeltaBytes=524288 -XX:NewSize=34603008 -XX:OldSize=70254592 -XX:+UseCompressedClassPointers -XX:+UseCompressedOops -XX:+UseFastUnorderedTimeStamps -XX:-UseLargePagesIndividualAllocation -XX:+UseParallelGC
Command line:  -agentlib:jdwp=transport=dt_socket,server=n,suspend=y,address=localhost:52443 -Xms100M -Xmx500M
```

可以看到我们启动应用时只指定了 `-Xms100M -Xmx500M`，也就是 `-XX:InitialHeapSize=104857600 -XX:MaxHeapSize=524288000` 这两个参数，但是 `jinfo -flags` 输出了很多其他的参数值（并不是所有的参数）。

### `jinfo -flag <name> <pid>`

`-flag` 参数用于显示某个 JVM 参数的值。比如查看启动时指定的参数 `InitialHeapSize`：

```
$ jinfo -flag InitialHeapSize 3452
-XX:InitialHeapSize=104857600
```

查看启动时未指定的参数 `MaxTenuringThreshold`：

```
$ jinfo -flag MaxTenuringThreshold 3452
-XX:MaxTenuringThreshold=15
```

如果参数值是布尔类型，会在参数前用 `+/-` 表示：

```
$ jinfo -flag PrintGC 3452
-XX:-PrintGC

$ jinfo -flag UseParallelGC 3452
-XX:+UseParallelGC
```

> 完整的 JVM 参数列表可以参考 [Java 官方文档](https://docs.oracle.com/javase/8/docs/technotes/tools/windows/java.html)。

### `jinfo -flag [+|-]<name> <pid>` 和 `jinfo -flag <name>=<value> <pid>`

用于动态地修改某个参数的值，如果是布尔类型参数，在参数前加上 `+/-` 表示 `true/false`：

```
$ jinfo -flag +PrintGC 3452
$ jinfo -flag PrintGC 3452
-XX:+PrintGC
```

> 仅有部分参数支持动态修改，如下（[参考链接](https://knowledge.informatica.com/s/article/528321?language=en_US)）：
>
> * CMSTriggerInterval
> * CMSWaitDuration
> * HeapDumpAfterFullGC
> * HeapDumpBeforeFullGC
> * HeapDumpOnOutOfMemoryError
> * HeapDumpPath
> * MaxHeapFreeRatio
> * MinHeapFreeRatio
> * PrintClassHistogram
> * PrintClassHistogramAfterFullGC
> * PrintClassHistogramBeforeFullGC
> * PrintConcurrentLocks
> * PrintGC
> * PrintGCDateStamps
> * PrintGCDetails
> * PrintGCID
> * PrintGCTimeStamps

### `jinfo -sysprops <pid>`

`-sysprops` 参数用于显示所有的系统属性，等同于 `System.getProperties()`。

```
$ jinfo -sysprops 3452
java.runtime.name = Java(TM) SE Runtime Environment
java.vm.version = 25.351-b10
sun.boot.library.path = C:\Program Files\Java\jdk1.8.0_351\jre\bin
java.vendor.url = http://java.oracle.com/
java.vm.vendor = Oracle Corporation
path.separator = ;
file.encoding.pkg = sun.io
java.vm.name = Java HotSpot(TM) 64-Bit Server VM
sun.os.patch.level =
sun.java.launcher = SUN_STANDARD
user.script =
user.country = CN
user.dir = D:\code\weekly-practice\notes\week028-jvm-diagnostic-tools\demo
java.vm.specification.name = Java Virtual Machine Specification
PID = 3452
java.runtime.version = 1.8.0_351-b10
java.awt.graphicsenv = sun.awt.Win32GraphicsEnvironment
os.arch = amd64
java.endorsed.dirs = C:\Program Files\Java\jdk1.8.0_351\jre\lib\endorsed
CONSOLE_LOG_CHARSET = GBK
line.separator =

java.io.tmpdir = C:\Users\ANEASY~1\AppData\Local\Temp\
java.vm.specification.vendor = Oracle Corporation
user.variant =
os.name = Windows 10
FILE_LOG_CHARSET = GBK
sun.jnu.encoding = GBK
java.library.path = C:\Program Files\Java\jdk1.8.0_351\bin;C:\Windows\Sun\Java\bin;C:\Windows\system32;C:\Windows;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Windows\System32\OpenSSH\;C:\Program Files\Git\cmd;C:\Program Files\TortoiseGit\bin;C:\Program Files\Java\jdk1.8.0_351\bin;;.
spring.beaninfo.ignore = true
java.class.version = 52.0
java.specification.name = Java Platform API Specification
sun.management.compiler = HotSpot 64-Bit Tiered Compilers
os.version = 10.0
user.home = C:\Users\aneasystone
user.timezone = Asia/Shanghai
catalina.useNaming = false
java.awt.printerjob = sun.awt.windows.WPrinterJob
file.encoding = GBK
java.specification.version = 1.8
catalina.home = C:\Users\aneasystone\AppData\Local\Temp\tomcat.8080.2731142439368397626
user.name = aneasystone
java.class.path = C:\Users\ANEASY~1\AppData\Local\Temp\cp_8yo4m2rw35c8uckdakai417ak.jar
java.vm.specification.version = 1.8
sun.arch.data.model = 64
sun.java.command = com.example.demo.DemoApplication
java.home = C:\Program Files\Java\jdk1.8.0_351\jre
user.language = zh
java.specification.vendor = Oracle Corporation
awt.toolkit = sun.awt.windows.WToolkit
java.vm.info = mixed mode
java.version = 1.8.0_351
java.ext.dirs = C:\Program Files\Java\jdk1.8.0_351\jre\lib\ext;C:\Windows\Sun\Java\lib\ext
sun.boot.class.path = C:\Program Files\Java\jdk1.8.0_351\jre\lib\resources.jar;C:\Program Files\Java\jdk1.8.0_351\jre\lib\rt.jar;C:\Program Files\Java\jdk1.8.0_351\jre\lib\jsse.jar;C:\Program Files\Java\jdk1.8.0_351\jre\lib\jce.jar;C:\Program Files\Java\jdk1.8.0_351\jre\lib\charsets.jar;C:\Program Files\Java\jdk1.8.0_351\jre\lib\jfr.jar;C:\Program Files\Java\jdk1.8.0_351\jre\classes
java.awt.headless = true
java.vendor = Oracle Corporation
sun.stderr.encoding = ms936
catalina.base = C:\Users\aneasystone\AppData\Local\Temp\tomcat.8080.2731142439368397626
java.specification.maintenance.version = 4
file.separator = \
java.vendor.url.bug = http://bugreport.sun.com/bugreport/
sun.io.unicode.encoding = UnicodeLittle
sun.cpu.endian = little
sun.stdout.encoding = ms936
sun.desktop = windows
sun.cpu.isalist = amd64
```

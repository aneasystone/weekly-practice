## jmap - Memory Map for Java

`jmap` 是一款强大的 JVM 内存分析的命令行工具，它可以用于生成 Java 程序的 Heap Dump 文件，或者对堆中的对象实例进行统计，还可以查看 ClassLoader 信息以及 finalizer 执行队列等。

它的命令格式如下：

```
$ jmap -help
Usage:
        (to connect to running process)
    jmap [option] <executable <core>
        (to connect to a core file)
    jmap [option] [server_id@]<remote server IP or hostname>
        (to connect to remote debug server)

where <option> is one of:
    <none>               to print same info as Solaris pmap
    -heap                to print java heap summary
    -histo[:live]        to print histogram of java object heap; if the "live"
                         suboption is specified, only count live objects
    -clstats             to print class loader statistics
    -finalizerinfo       to print information on objects awaiting finalization
    -dump:<dump-options> to dump java heap in hprof binary format
                         dump-options:
                           live         dump only live objects; if not specified,
                                        all objects in the heap are dumped.
                           format=b     binary format
                           file=<file>  dump heap to <file>
                         Example: jmap -dump:live,format=b,file=heap.bin <pid>
    -F                   force. Use with -dump:<dump-options> <pid> or -histo
                         to force a heap dump or histogram when <pid> does not
                         respond. The "live" suboption is not supported
                         in this mode.
    -h | -help           to print this help message
    -J<flag>             to pass <flag> directly to the runtime system
```

### `jmap <pid>`

不带任何参数的 `jmap` 命令和 Linux 下的 `pmap` 命令一样，用于输出进程的内存映射关系：

```
$ jmap 13952
0x0000000055cb0000      8580K   C:\Program Files\Java\jdk1.8.0_351\jre\bin\server\jvm.dll
0x00007ff744cc0000      284K    C:\Program Files\Java\jdk1.8.0_351\bin\java.exe
0x00007fff901e0000      144K    C:\Program Files\Java\jdk1.8.0_351\jre\bin\sunec.dll
0x00007fff90210000      620K    C:\Program Files\Java\jdk1.8.0_351\jre\bin\msvcp140.dll
0x00007fff9c830000      216K    C:\Program Files\Java\jdk1.8.0_351\jre\bin\jdwp.dll
0x00007fff9e790000      96K     C:\Program Files\Java\jdk1.8.0_351\jre\bin\zip.dll
0x00007fffa1a10000      52K     C:\Program Files\Java\jdk1.8.0_351\jre\bin\sunmscapi.dll
0x00007fffa1a20000      172K    C:\Program Files\Java\jdk1.8.0_351\jre\bin\java.dll
0x00007fffa4bd0000      40K     C:\Program Files\Java\jdk1.8.0_351\jre\bin\dt_socket.dll
...
0x00007fffc2990000      200K    C:\Windows\System32\IMM32.DLL
0x00007fffc2a30000      2016K   C:\Windows\SYSTEM32\ntdll.dll
```

这个命令实际用处并不大，从输出结果可以看到这实际上是 `java.exe` 进程的内存信息。

### `jmap -histo <pid>`

`-histo` 选项用于输出堆中对象的统计信息：

```
> jmap -histo 10712

 num     #instances         #bytes  class name
----------------------------------------------
   1:           435        1740328  [I
   2:          4236         651528  [C
   3:          2817          67608  java.lang.String
   4:           486          55744  java.lang.Class
   5:           113          42264  [B
   6:           547          38256  [Ljava.lang.Object;
   7:           792          31680  java.util.TreeMap$Entry
   8:           591          14184  java.lang.StringBuilder
   9:           450          10800  com.example.DemoApp$Person
  10:           213           9440  [Ljava.lang.String;
...
 227:             1             16  sun.misc.PostVMInitHook$2
 228:             1             16  sun.misc.Unsafe
 229:             1             16  sun.net.www.protocol.file.Handler
 230:             1             16  sun.reflect.ReflectionFactory
 231:             1             16  sun.usagetracker.UsageTrackerClient
Total         12426        2734544
```

从统计结果中可以看到，这个 Java 程序当前共有 231 个不同的类，以及每个类的类名、实例数和占用内存大小。在输出的最后一行，还对实例数和内存进行了汇总。

### `jmap -heap <pid>`

`-heap` 选项用于显示堆的详细信息：

```
$ jmap -heap 9740
using thread-local object allocation.
Parallel GC with 8 thread(s)

Heap Configuration:
   MinHeapFreeRatio         = 0
   MaxHeapFreeRatio         = 100
   MaxHeapSize              = 209715200 (200.0MB)
   NewSize                  = 34603008 (33.0MB)
   MaxNewSize               = 69730304 (66.5MB)
   OldSize                  = 70254592 (67.0MB)
   NewRatio                 = 2
   SurvivorRatio            = 8
   MetaspaceSize            = 21807104 (20.796875MB)
   CompressedClassSpaceSize = 1073741824 (1024.0MB)
   MaxMetaspaceSize         = 17592186044415 MB
   G1HeapRegionSize         = 0 (0.0MB)

Heap Usage:
PS Young Generation
Eden Space:
   capacity = 26214400 (25.0MB)
   used     = 2097616 (2.0004425048828125MB)
   free     = 24116784 (22.999557495117188MB)
   8.00177001953125% used
From Space:
   capacity = 4194304 (4.0MB)
   used     = 0 (0.0MB)
   free     = 4194304 (4.0MB)
   0.0% used
To Space:
   capacity = 4194304 (4.0MB)
   used     = 0 (0.0MB)
   free     = 4194304 (4.0MB)
   0.0% used
PS Old Generation
   capacity = 70254592 (67.0MB)
   used     = 0 (0.0MB)
   free     = 70254592 (67.0MB)
   0.0% used

1617 interned Strings occupying 149584 bytes.
```

输出结果中包含了堆的配置信息和使用情况，这和命令 `jstat -gc` 或 `jstat -gcutil` 是类似的，不过这里以汇总的形式显示，看起来更直观和友好。 

注意这里的两个参数：

* `NewRatio=2` 表示年轻代的大小是老年代大小的 1/2，年轻代大小为 25+4+4 = 33MB，老年代大小为 67MB
* `SurvivorRatio=8` 表示年轻代的 Eden 区与 Survivor 区的比例为 8:1:1，所以 From 区和 To 区的大小为 33/10 = 3.3 ≈ 4MB，Eden 区大小为 33-8 = 25MB

### `jmap -clstats <pid>`

`-clstats` 选项用于输出 Java 程序中 ClassLoader 的统计信息：

```
$ jmap -clstats 16448
finding class loader instances ..done.
computing per loader stat ..done.
please wait.. computing liveness.........................done.
class_loader    classes bytes   parent_loader   alive?  type

<bootstrap>     417     808334    null          live    <internal>
0x00000000fbe370e8      0       0         null          live    sun/misc/Launcher$ExtClassLoader@0x000000010000fad8
0x00000000fbe43bd8      2       1843    0x00000000fbe370e8      live    sun/misc/Launcher$AppClassLoader@0x000000010000f730

total = 3       419     810177      N/A         alive=3, dead=0     N/A
```

从上面的输出中可以看到，该 Java 进程创建了三个 ClassLoader，以及它们的父子关系，同时显示了每个 ClassLoader 加载的类的数量和大小。这三个 ClassLoader 分别是：

* `Bootstrap ClassLoader` - 启动类加载器
* `Extension ClassLoader` - 扩展类加载器
* `App ClassLoader` - 应用类加载器，也被称为系统类加载器

### `jmap -finalizerinfo <pid>`

不恰当的 `finalize()` 方法可能导致对象堆积在 finalizer 队列中，通过 `-finalizerinfo` 选项可以统计堆积在 finalizer 队列中的对象：

```
$ jmap -finalizerinfo 16448
Number of objects pending for finalization: 0
```

### `jmap -dump <pid>`

`jmap` 命令的一个重要功能就是将 Java 进程的堆快照导出到某个文件中，方便我们对堆内存进行分析：

```
$ jmap -dump:live,format=b,file=heap.hprof 16448
Dumping heap to C:\Users\aneasystone\heap.hprof ...
Heap dump file created
```

上面的命令将应用程序的堆快照导出到当前目录下的 `heap.hprof` 文件中，有很多不同的工具可以分析该堆文件，比如：jhat、Visual VM、MAT 等。

另外，我们可以在启动 Java 进程时指定 `-XX:+HeapDumpOnOutOfMemoryError` 参数，这样可以在发生 OOM 时自动生成堆快照。

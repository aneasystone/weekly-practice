## jstat - JVM Statistics Monitoring

`jstat` 命令用于监视虚拟机运行时状态信息，可以显示出虚拟机进程中的类装载、内存、垃圾收集、JIT 编译等运行数据。

它的命令格式如下：

```
$ jstat -help
Usage: jstat -help|-options
       jstat -<option> [-t] [-h<lines>] <vmid> [<interval> [<count>]]

Definitions:
  <option>      An option reported by the -options option
  <vmid>        Virtual Machine Identifier. A vmid takes the following form:
                     <lvmid>[@<hostname>[:<port>]]
                Where <lvmid> is the local vm identifier for the target
                Java virtual machine, typically a process id; <hostname> is
                the name of the host running the target Java virtual machine;
                and <port> is the port number for the rmiregistry on the
                target host. See the jvmstat documentation for a more complete
                description of the Virtual Machine Identifier.
  <lines>       Number of samples between header lines.
  <interval>    Sampling interval. The following forms are allowed:
                    <n>["ms"|"s"]
                Where <n> is an integer and the suffix specifies the units as
                milliseconds("ms") or seconds("s"). The default units are "ms".
  <count>       Number of samples to take before terminating.
  -J<flag>      Pass <flag> directly to the runtime system.
```

其中支持的 `option` 选项如下：

```
$ jstat -options
-class
-compiler
-gc
-gccapacity
-gccause
-gcmetacapacity
-gcnew
-gcnewcapacity
-gcold
-gcoldcapacity
-gcutil
-printcompilation
```

### `jstat -class <pid>`

`-class` 选项用于输出 ClassLoader 相关的统计信息。

```
$ jstat -class 13348
Loaded  Bytes  Unloaded  Bytes     Time
  6460 11747.3       45   61.0     12.25
```

其中，每一列的含义如下：

* `Loaded` - 已加载类的数量
* `Bytes` - 已加载类的大小
* `Unloaded` - 已卸载类的数量
* `Bytes` - 已卸载类的大小
* `Time` - 加载和卸载类所花费的时间

### `jstat -compiler <pid>`

`-compiler` 选项用于输出 JIT 编译器的统计信息。

```
$ jstat -compiler 13348
Compiled Failed Invalid   Time   FailedType FailedMethod
    3633      1       0  14.01            1 sun/misc/URLClassPath$JarLoader getResource
```

其中，每一列的含义如下：

* `Compiled` - JIT 编译的总次数
* `Failed` - JIT 编译失败的次数
* `Invalid` - JIT 编译不可用的次数
* `Time` - JIT 编译所花费的时间
* `FailedType` - 最后一次编译失败的类型
* `FailedMethod` - 最后一次编译失败的方法名称

关于 `FailedType` 字段的解释，可以 [参考这里](https://zhuanlan.zhihu.com/p/25478502)，它实际上是一个枚举值：

```
enum {
  no_compile, // 0：没有编译
  normal_compile, // 1：普通编译（从方法正常入口开始编译）
  osr_compile, // 2：On-Stack Replacement 编译（从方法中某个循环的回边开始编译）
  native_compile // 3：Native Wrapper 编译
};
```

### `jstat -printcompilation <pid>`

`-printcompilation` 选项用于输出 JIT 编译的方法信息：

```
$ jstat -printcompilation 15100
Compiled  Size  Type Method
    3101     79    1 java/util/concurrent/locks/AbstractQueuedSynchronizer doReleaseShared
```

其中，每一列的含义如下：

* `Compiled` - 最近编译方法的数量
* `Size` - 最近编译方法的字节数
* `Type` - 最近编译方法的编译类型
* `Method` - 最近编译的方法名称

### `jstat -gc <pid>`

`-gc` 选项用于输出垃圾回收堆的统计。

```
$ jstat -gc 11324
   S0C    S1C  S0U      S1U      EC       EU        OC         OU        MC      MU   CCSC   CCSU    YGC     YGCT   FGC     FGCT      GCT
9728.0 4096.0  0.0   4069.0 51200.0  26670.1   68608.0    10714.9   29824.0 27948.7 3968.0 3502.4      5    0.045     1    0.030    0.075
```

这里的列比较多，前面一部分显示了和 GC 相关的堆的各个区域的大小（单位均为 KB）：

* `S0C` - 当前 S0 区的容量
* `S1C` - 当前 S1 区的容量
* `S0U` - S0 区已使用大小
* `S1U` - S1 区已使用大小
* `EC` - 当前 Eden 区的容量
* `EU` - Eden 区已使用大小

其中，S0 和 S1 又被称为第一个幸存区和第二个幸存区，Eden 又被称为伊甸园区，S0、S1 和 Eden 这三个区域合称为新生代（`New Generation`）。

* `OC` - 当前老年区的容量（`Old Generation`）
* `OU` - 老年区已使用大小
* `MC` - 当前元数据空间的容量（`Metaspace`）
* `MU` - 元数据空间已使用大小
* `CCSC` - 当前压缩类空间的容量（`Compressed Class Space`）
* `CCSU` - 压缩类空间已使用大小

在 Java 8 之前的版本中没有元数据空间，所以显示的是永久代大小：

* `PC` - 当前永久区的容量（`Permanent Generation`）
* `PU` - 永久区已使用大小

后面几列显示了 GC 的次数和耗时：

* `YGC` - 新生代 GC 次数
* `YGCT` - 新生代 GC 耗时
* `FGC` - Full GC 次数
* `FGCT` - Full GC 耗时
* `GCT` - GC 总耗时

下面这张图比较直观地显示了 GC 堆的各个区域以及它们之间的关系（[图片来源](https://www.cnblogs.com/ruoli-0/p/14275977.html)）：

![](./images/gc-heap.png)

### `jstat -gccapacity <pid>`

`-gccapacity` 选项和 `-gc` 选项类似，也是用于输出垃圾回收堆的统计，和 `-gc` 相比，它不仅输出了各个代的当前大小，还输出了各个代的最大值和最小值，这可以方便地计算出各个代的内存占用情况，排查 OOM 问题。

```
$ jstat -gccapacity 11324
 NGCMN    NGCMX     NGC     S0C   S1C       EC      OGCMN      OGCMX       OGC         OC       MCMN     MCMX      MC     CCSMN    CCSMX     CCSC    YGC    FGC
 33792.0 170496.0  99840.0 9728.0 4096.0  51200.0    68608.0   341504.0    68608.0    68608.0      0.0 1075200.0  29824.0      0.0 1048576.0   3968.0      5     1
```

其中，每一列的含义如下：

* `NGCMN` - 新生代容量的最小值
* `NGCMX` - 新生代容量的最大值
* `NGC` - 当前新生代的容量
* `S0C` - 当前 S0 区的容量
* `S1C` - 当前 S1 区的容量
* `EC` - 当前 Eden 区的容量

> S0C + S1C + EC 为啥不等于 NGC？因为 S0C、S1C、EC 这些表示的是容量（`Capacity`）而不是真实使用的大小（`Utilization`）。

* `OGCMN` - 老年代容量的最小值
* `OGCMX` - 老年代容量的最大值
* `OGC` - 当前老年代的容量
* `OC` - 当前老年区的容量

这里比较疑惑的两列是 OGC 和 OC，看起来它们的值完全一样的。根据 [官方文档](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jstat.html#gccapacity_option) 知道，OGC 表示 **Current old generation capacity**，OC 表示 **Current old space capacity**，那么 old generation 和 old space 有什么区别呢？实际上 `generation（代）` 和 `space（区）` 是 JVM 中的两个概念，一个代可以包含多个区，比如新生代包含了 S0、S1、Eden 三个区，而老年代就只有一个区，所以 OGC 实际上也就是 OC。

* `MCMN` - 元数据空间容量的最小值
* `MCMX` - 元数据空间容量的最大值
* `MC` - 当前元数据空间的容量
* `CCSMN` - 压缩类空间容量的最小值
* `CCSMX` - 压缩类空间容量的最大值
* `CCSC` - 当前压缩类空间的容量
* `YGC` - 新生代 GC 次数
* `FGC` - Full GC 次数

同样地，在 Java 8 之前的版本中没有元数据空间，所以显示的是永久代大小：

* `PGCMN`	- 永久代容量的最小值
* `PGCMX`	- 永久代容量的最大值
* `PGC`	- 当前永久代的容量
* `PC` - 当前永久区的容量

这里的 PGC/PC 和 OGC/OC 一样，一个是代的容量，一个是区的容量。永久代就只有一个区，所以 PGC 和 PC 也是相同的。

### `jstat -gcutil <pid>`

`-gcutil` 选项和 `-gc` 选项类似，也是用于输出垃圾回收堆的统计，只不过它输出的不是每个内存区的大小，而是百分比，可以更直观的看出每个区的使用情况。

```
$ jstat -gcutil 15100
  S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT
  0.00  99.22  54.62  15.50  93.89  90.97      5    0.067     1    0.045    0.112
```

其中，每一列的含义如下：

* `S0` - S0 区的使用率
* `S1` - S1 区的使用率
* `E` - Eden 区的使用率
* `O` - 老年代的使用率
* `M` - 元数据空间的使用率
* `CCS` - 压缩类空间的使用率

同样地，在 Java 8 之前的版本中没有元数据空间，显示的是永久代的使用率：

* `P`	- 永久代的使用率

后面几列和 `-gc` 选项的输出一样，显示了 GC 的次数和耗时：

* `YGC` - 新生代 GC 次数
* `YGCT` - 新生代 GC 耗时
* `FGC` - Full GC 次数
* `FGCT` - Full GC 耗时
* `GCT` - GC 总耗时

### `jstat -gcnew <pid>`

`-gcnew` 选项用于输出新生代的详细信息：

```
$ jstat -gcnew 15100
 S0C    S1C    S0U    S1U   TT MTT  DSS      EC       EU     YGC     YGCT
9728.0 4096.0    0.0 4064.0  6  15 9728.0  51200.0  28991.8      5    0.067
```

其中，每一列的含义如下：

* `S0C` - 当前 S0 区的容量
* `S1C` - 当前 S1 区的容量
* `S0U` - S0 区已使用大小
* `S1U` - S1 区已使用大小
* `TT` - 当前的老年代阀值（`Tenuring threshold`）
* `MTT` - 老年代的最大阀值（`Maximum tenuring threshold`）
* `DSS` - 期望的存活区大小（`Desired survivor size`）
* `EC` - 当前 Eden 区的容量
* `EU` - Eden 区已使用大小
* `YGC` - 新生代 GC 次数
* `YGCT` - 新生代 GC 耗时

大多数列前面已经介绍过，不过有三个新列值得注意一下：`TT` 表示当前的老年代阈值，也就是从新生代对象晋升到老年代对象的年龄，一个对象的年龄就是这个对象经历 GC 的次数，上面的输出中 `TT = 6` 表示当一个新生代对象如果经过 6 次 GC 后还存活将被移到老年代中。`MTT` 表示老年代的最大阈值，可以在程序启动时通过 JVM 参数 `--XX:MaxTenuringThreshold=15` 进行配置，这个值一般在 0-15 之间。`DSS` 表示期望的存活区大小，要理解这个值的大小，我们必须还得了解 JVM 的另一个参数 `-XX:TargetSurvivorRatio=50`，它表示存活区的目标使用率，默认值为 50%，而 `DSS` 就是根据这个计算出来的：

```
DSS = (存活区容量 * TargetSurvivorRatio) / 100
```

当存活区的对象大小超出 DSS 大小时，JVM 会自动调整 TT 的值，那么调整成多少呢？我们可以从 [OpenJDK 的源码](https://github.com/openjdk/jdk) 中找到答案。在 [src/hotspot/share/gc/shared/ageTable.cpp](https://github.com/openjdk/jdk/blob/master/src/hotspot/share/gc/shared/ageTable.cpp) 文件中有一个 `compute_tenuring_threshold` 函数：

```cpp
uint AgeTable::compute_tenuring_threshold(size_t desired_survivor_size) {
  uint result;

  if (AlwaysTenure || NeverTenure) {
    assert(MaxTenuringThreshold == 0 || MaxTenuringThreshold == markWord::max_age + 1,
           "MaxTenuringThreshold should be 0 or markWord::max_age + 1, but is " UINTX_FORMAT, MaxTenuringThreshold);
    result = MaxTenuringThreshold;
  } else {
    size_t total = 0;
    uint age = 1;
    assert(sizes[0] == 0, "no objects with age zero should be recorded");
    while (age < table_size) {
      total += sizes[age];
      // check if including objects of age 'age' made us pass the desired
      // size, if so 'age' is the new threshold
      if (total > desired_survivor_size) break;
      age++;
    }
    result = age < MaxTenuringThreshold ? age : MaxTenuringThreshold;
  }


  log_debug(gc, age)("Desired survivor size " SIZE_FORMAT " bytes, new threshold " UINTX_FORMAT " (max threshold " UINTX_FORMAT ")",
                     desired_survivor_size * oopSize, (uintx) result, MaxTenuringThreshold);

  return result;
}
```

从代码可以看出，从年龄为 1 的对象开始统计大小，一直往上累加，当累加到年龄为 n 时，如果总大小超出了 DSS，就将 TT 设置为 n。

### `jstat -gcnewcapacity <pid>`

`-gcnewcapacity` 选项用于输出新生代各个区的大小信息：

```
$ jstat -gcnewcapacity 15100
  NGCMN      NGCMX       NGC      S0CMX     S0C     S1CMX     S1C       ECMX        EC      YGC   FGC
   33792.0   170496.0   100864.0  56832.0   9728.0  56832.0   4096.0   169472.0    51200.0     5     1
```

其中，每一列的含义如下：

* `NGCMN` - 新生代容量的最小值
* `NGCMX` - 新生代容量的最大值
* `NGC` - 当前新生代的容量
* `S0CMX` - S0 区容量的最大值
* `S0C` - 当前 S0 区的容量
* `S1CMX` - S1 区容量的最大值
* `S1C` - 当前 S1 区的容量
* `ECMX` - Eden 区容量的最大值
* `EC` - 当前 Eden 区的容量
* `YGC` - 新生代 GC 次数
* `FGC` - Full GC 次数

### `jstat -gcold <pid>`

`-gcold` 选项用于输出老年代的详细信息：

```
$ jstat -gcold 15100
   MC       MU      CCSC     CCSU       OC          OU       YGC    FGC    FGCT     GCT
 29696.0  27882.8   3840.0   3493.1     68608.0     10637.1      5     1    0.045    0.112
```

其中，每一列的含义如下：

* `MC` - 当前元数据空间的容量
* `MU` - 元数据空间已使用大小
* `CCSC` - 当前压缩类空间的容量
* `CCSU` - 压缩类空间已使用大小
* `OC` - 当前老年区的容量
* `OU` - 老年区已使用大小
* `YGC` - 新生代 GC 次数
* `FGC` - Full GC 次数
* `FGCT` - Full GC 耗时
* `GCT` - GC 总耗时

### `jstat -gcoldcapacity <pid>`

`-gcoldcapacity` 选项用于输出老年代各个区的大小信息：

```
$ jstat -gcoldcapacity 15100
   OGCMN       OGCMX        OGC         OC       YGC   FGC    FGCT     GCT
    68608.0    341504.0     68608.0     68608.0     5     1    0.045    0.112
```

其中，每一列的含义如下：

* `OGCMN` - 老年代容量的最小值
* `OGCMX` - 老年代容量的最大值
* `OGC` - 当前老年代的容量
* `OC` - 当前老年区的容量
* `YGC` - 新生代 GC 次数
* `FGC` - Full GC 次数
* `FGCT` - Full GC 耗时
* `GCT` - GC 总耗时

### `jstat -gcmetacapacity <pid>`

`-gcmetacapacity` 选项用于输出元数据空间各个区的大小信息：

```
$ jstat -gcmetacapacity 15100
   MCMN       MCMX        MC       CCSMN      CCSMX       CCSC     YGC   FGC    FGCT     GCT
       0.0  1075200.0    29696.0        0.0  1048576.0     3840.0     5     1    0.045    0.112
```

其中，每一列的含义如下：

* `MCMN` - 元数据空间容量的最小值
* `MCMX` - 元数据空间容量的最大值
* `MC` - 当前元数据空间的容量
* `CCSMN` - 压缩类空间容量的最小值
* `CCSMX` - 压缩类空间容量的最大值
* `CCSC` - 当前压缩类空间的容量
* `YGC` - 新生代 GC 次数
* `FGC` - Full GC 次数
* `FGCT` - Full GC 耗时
* `GCT` - GC 总耗时

### `jstat -gccause <pid>`

`-gccause` 选项和 `-gcutil` 类似，用于输出垃圾回收各个区域的占用情况，同时它还可以显示出最近一次和当前发生 GC 的原因：

```
$ jstat -gccause 15100
  S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT    LGCC                 GCC
  0.00  99.22  56.62  15.50  93.89  90.97      5    0.067     1    0.045    0.112 Allocation Failure   No GC
```

其中，前面的几列和 `-gcutil` 完全一样：

* `S0` - S0 区的使用率
* `S1` - S1 区的使用率
* `E` - Eden 区的使用率
* `O` - 老年代的使用率
* `M` - 元数据空间的使用率
* `CCS` - 压缩类空间的使用率
* `YGC` - 新生代 GC 次数
* `YGCT` - 新生代 GC 耗时
* `FGC` - Full GC 次数
* `FGCT` - Full GC 耗时
* `GCT` - GC 总耗时

最后多了两列：

* `LGCC` - 上次 GC 的原因
* `GCC` - 当前 GC 的原因

### `jstat -option -t -h<lines> <pid> <interval> <count>`

除了上面这些选项，`jstat` 还支持一些命令行参数来灵活地控制输出。比如 `-t` 用于在每一行的开头打印一个时间戳；`-h` 用于周期性地输出表头信息；命令的最后还可以加 `<interval>` 和 `<count>` 两个参数，用于周期性地输出信息：

```
$ jstat -gcutil -t -h3 15100 1000 5
Timestamp         S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT
         5448.3   0.00  99.22  56.62  15.50  93.89  90.97      5    0.067     1    0.045    0.112
         5449.4   0.00  99.22  56.62  15.50  93.89  90.97      5    0.067     1    0.045    0.112
         5450.4   0.00  99.22  56.62  15.50  93.89  90.97      5    0.067     1    0.045    0.112
Timestamp         S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT
         5451.3   0.00  99.22  56.62  15.50  93.89  90.97      5    0.067     1    0.045    0.112
         5452.4   0.00  99.22  56.62  15.50  93.89  90.97      5    0.067     1    0.045    0.112
```

从上面的命令输出可以看到，在每一行前面多了一列 `Timestamp`，每隔 1s 就输出一次，共输出了 5 次，而且每隔 3 次就会打印一次表头信息，当我们需要持续对 GC 信息进行监控时这些参数将非常有用。

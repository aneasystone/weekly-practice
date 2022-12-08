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

### `jstat -gc <pid>`

垃圾回收堆的统计

### `jstat -gccapacity <pid>`

### `jstat -gccause <pid>`

### `jstat -gcmetacapacity <pid>`

### `jstat -gcnew <pid>`

### `jstat -gcnewcapacity <pid>`

### `jstat -gcold <pid>`

### `jstat -gcoldcapacity <pid>`

### `jstat -gcutil <pid>`

垃圾回收统计概述

### `jstat -printcompilation <pid>`

### `jstat -option -t -h<lines> <pid> <interval> <count>`

```
# jstat -gcutil 20636 1000 10
  S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT   
  0.00  34.38  48.32  20.40  96.47  90.26   6539  160.802     0    0.000  160.802
  0.00  34.38  49.53  20.40  96.47  90.26   6539  160.802     0    0.000  160.802
  0.00  34.38  49.54  20.40  96.47  90.26   6539  160.802     0    0.000  160.802
  0.00  34.38  49.71  20.40  96.47  90.26   6539  160.802     0    0.000  160.802
  0.00  34.38  49.71  20.40  96.47  90.26   6539  160.802     0    0.000  160.802
```
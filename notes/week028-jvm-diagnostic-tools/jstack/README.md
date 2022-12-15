## jstack - Stack Trace for Java

`jstack` 用于生成 Java 程序当前时刻的线程快照，这个命令可以帮我们定位线程出现长时间停顿的原因，比如线程间的死锁、死循环、请求外部资源导致的长时间等待等。

它的命令格式如下：

```
$ jstack -h
Usage:
    jstack [-l] <pid>
        (to connect to running process)
    jstack -F [-m] [-l] <pid>
        (to connect to a hung process)
    jstack [-m] [-l] <executable> <core>
        (to connect to a core file)
    jstack [-m] [-l] [server_id@]<remote server IP or hostname>
        (to connect to a remote debug server)

Options:
    -F  to force a thread dump. Use when jstack <pid> does not respond (process is hung)
    -m  to print both java and native frames (mixed mode)
    -l  long listing. Prints additional information about locks
    -h or -help to print this help message
```

### `jstack <pid>`

`jstack` 直接后跟 Java 进程的 PID，用于输出 Java 进程当前的线程堆栈：

```
$ jstack 8324
2022-12-14 07:35:00
Full thread dump Java HotSpot(TM) 64-Bit Server VM (25.351-b10 mixed mode):

"Service Thread" #13 daemon prio=9 os_prio=0 tid=0x00000152d8d6e000 nid=0x4764 runnable [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"C1 CompilerThread3" #12 daemon prio=9 os_prio=2 tid=0x00000152d8d1c000 nid=0x363c waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"C2 CompilerThread2" #11 daemon prio=9 os_prio=2 tid=0x00000152d8d09800 nid=0x3fcc waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"C2 CompilerThread1" #10 daemon prio=9 os_prio=2 tid=0x00000152d8cf4800 nid=0x3700 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"C2 CompilerThread0" #9 daemon prio=9 os_prio=2 tid=0x00000152d8cf1000 nid=0x384 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"JDWP Command Reader" #8 daemon prio=10 os_prio=0 tid=0x00000152d8ce1000 nid=0x2b50 runnable [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"JDWP Event Helper Thread" #7 daemon prio=10 os_prio=0 tid=0x00000152d8ce0800 nid=0x1ae0 runnable [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"JDWP Transport Listener: dt_socket" #6 daemon prio=10 os_prio=0 tid=0x00000152d7609800 nid=0x1340 runnable [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"Attach Listener" #5 daemon prio=5 os_prio=2 tid=0x00000152d758b800 nid=0x16a4 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"Signal Dispatcher" #4 daemon prio=9 os_prio=2 tid=0x00000152d7573800 nid=0x2884 runnable [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"Finalizer" #3 daemon prio=8 os_prio=1 tid=0x00000152d694a800 nid=0x1d68 in Object.wait() [0x0000000ab48ff000]
   java.lang.Thread.State: WAITING (on object monitor)
        at java.lang.Object.wait(Native Method)
        - waiting on <0x00000000fbd88f08> (a java.lang.ref.ReferenceQueue$Lock)
        at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:150)
        - locked <0x00000000fbd88f08> (a java.lang.ref.ReferenceQueue$Lock)
        at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:171)
        at java.lang.ref.Finalizer$FinalizerThread.run(Finalizer.java:188)

"Reference Handler" #2 daemon prio=10 os_prio=2 tid=0x00000152d755a000 nid=0x4368 in Object.wait() [0x0000000ab47ff000]
   java.lang.Thread.State: WAITING (on object monitor)
        at java.lang.Object.wait(Native Method)
        - waiting on <0x00000000fbd86ba0> (a java.lang.ref.Reference$Lock)
        at java.lang.Object.wait(Object.java:502)
        at java.lang.ref.Reference.tryHandlePending(Reference.java:191)
        - locked <0x00000000fbd86ba0> (a java.lang.ref.Reference$Lock)
        at java.lang.ref.Reference$ReferenceHandler.run(Reference.java:153)

"main" #1 prio=5 os_prio=0 tid=0x00000152c4b53000 nid=0x9fc waiting on condition [0x0000000ab3dff000]
   java.lang.Thread.State: TIMED_WAITING (sleeping)
        at java.lang.Thread.sleep(Native Method)
        at com.example.DemoApp.main(DemoApp.java:14)

"VM Thread" os_prio=2 tid=0x00000152d7533800 nid=0x3ef8 runnable

"GC task thread#0 (ParallelGC)" os_prio=0 tid=0x00000152c4b69800 nid=0x4650 runnable

"GC task thread#1 (ParallelGC)" os_prio=0 tid=0x00000152c4b6a800 nid=0x41ec runnable

"GC task thread#2 (ParallelGC)" os_prio=0 tid=0x00000152c4b6c000 nid=0xa44 runnable

"GC task thread#3 (ParallelGC)" os_prio=0 tid=0x00000152c4b6d800 nid=0xeb0 runnable

"GC task thread#4 (ParallelGC)" os_prio=0 tid=0x00000152c4b6f800 nid=0x32c4 runnable

"GC task thread#5 (ParallelGC)" os_prio=0 tid=0x00000152c4b70800 nid=0x40d4 runnable

"GC task thread#6 (ParallelGC)" os_prio=0 tid=0x00000152c4b73800 nid=0x4270 runnable

"GC task thread#7 (ParallelGC)" os_prio=0 tid=0x00000152c4b74800 nid=0x2560 runnable

"VM Periodic Task Thread" os_prio=2 tid=0x00000152d8daa800 nid=0x26dc waiting on condition

JNI global references: 464
```

#### 线程解释

上面是示例程序的线程堆栈，可以看出就算程序非常简单，JVM 也会帮我们创建很多辅助的线程，一共有 23 个：

* Service Thread

JVM 内部线程，用于监听和处理一些 JVM 的内部事件（[参考](https://stackoverflow.com/questions/65227612/what-is-the-service-thread-in-the-jvm)）。

* C1 CompilerThread3
* C2 CompilerThread2
* C2 CompilerThread1
* C2 CompilerThread0

这几个线程是 JIT 编译器相关的线程，用于 C1 编译（Client Compiler）和 C2 编译（Server Compiler）。

* JDWP Command Reader
* JDWP Event Helper Thread
* JDWP Transport Listener: dt_socket

JDWP 全称为 **Java Debug Wire Protocol**，用于 Java 调试器，由于我们这里使用了调试模式启动程序，所以能看到这几个线程。

* Attach Listener
* Signal Dispatcher

JVM 提供了一种进程间通信的机制，能让一个进程将命令传到另一个进程，并让它执行某些操作，比如这里我们执行 `jstack` 命令就是通过这个机制来实现的。

JVM 在启动时会自动创建 `Signal Dispatcher` 线程，顾名思义，这个线程是专门用于处理各类信号的，执行 `jstack` 命令实际上会向目标进程发送一个 `SIGQUIT` 信号，在 JVM 里，除了 `Signal Dispatcher` 线程，其他线程对这个信号都做了屏蔽，当 `Signal Dispatcher` 线程接受到 `SIGQUIT` 信号后，就会创建 `Attach Listener` 线程。

`Attach Listener` 线程启动时，会创建一个套接字文件，`jstack` 进程在发送 `SIGQUIT` 信号后就一直在等待这个文件的生成，一旦检测到套接字文件生成，就可以和目标进程的 `Attach Listener` 线程通信了，而通信的过程比较简单，就是一边发送命令，一边执行命令。

关于 Attach 机制的实现原理可以参考 [这篇文章](http://lovestblog.cn/blog/2014/06/18/jvm-attach/)。

* Finalizer

JVM 在进行垃圾回收时，会检测对象是否实现了 `finalize()` 方法，如果实现了该方法并且该方法还没有被执行，则会将对象放到一个叫做 `F-Queue` 的队列（`java.lang.ref.Finalizer.ReferenceQueue`）中，`Finalizer` 线程就是用于遍历这个队列，并执行 `finalize()` 方法。

* Reference Handler

这个线程主要用于处理引用对象本身（软引用、弱引用、虚引用）的垃圾回收问题，它将引用的状态从 Pending 迁移到 Enqueued，具体可以参考 [这篇文章](https://xie.infoq.cn/article/1817914961ef7570c1d079a06)。

* main

这个就是我们代码的主线程。

* VM Thread

这是 JVM 内置的一个线程, 主要用来协调其它线程达到安全点（Safepoint），需要达到安全点的线程主要有：Stop the world 的 GC,  Thread dump, 线程挂起以及偏向锁的撤销。

* GC task thread#0 (ParallelGC)
* GC task thread#1 (ParallelGC)
* GC task thread#2 (ParallelGC)
* GC task thread#3 (ParallelGC)
* GC task thread#4 (ParallelGC)
* GC task thread#5 (ParallelGC)
* GC task thread#6 (ParallelGC)
* GC task thread#7 (ParallelGC)

很明显，这些都是 GC 线程，并且能从线程名字可以看出我们使用的垃圾回收器是 `ParallelGC`。我们可以通过 JVM 参数 `-XX:ParallelGCThreads=n` 修改线程数量，这里默认是 8 个 GC 线程（根据机器的 CPU 核数）。

* VM Periodic Task Thread

这个线程是 JVM 周期性任务调度的线程，比如定期的内存监控、JVM 运行状况监控等。

#### 线程分析

一个典型的线程堆栈信息如下：

```
"main" #1 prio=5 os_prio=0 tid=0x00000152c4b53000 nid=0x9fc waiting on condition [0x0000000ab3dff000]
   java.lang.Thread.State: TIMED_WAITING (sleeping)
        at java.lang.Thread.sleep(Native Method)
        at com.example.DemoApp.main(DemoApp.java:14)
```

这里每个字段的含义如下：

* `"main"` - 线程的名字
* `#1` - 线程的编号
* `prio=5` - 线程优先级
* `os_prio=0` - 系统级别的线程优先级
* `tid=0x00000152c4b53000` - 线程 ID
* `nid=0x9fc` - Native 线程 ID
* `waiting on condition [0x0000000ab3dff000]` - 线程当前的状态

我们在做线程分析时，最关注的就是线程当前的状态，它有下面几种不同的状态：

* `runnable` - 运行中状态
* `blocked` - 阻塞状态，等待锁的释放
* `wating` - 等待状态，等待特定的操作被唤醒，一般停留在 `park()`、`wait()`、`sleep()`、`join()` 等语句
* `time_wating` - 有时限的等待状态
* `terminated` - 线程已经退出

这几种状态之间的转换关系如下图所示：

![](./images/thread-states.jpg)

每个对象都有且仅有一个 `Monitor` 用以实现线程之间的互斥与协作，它可能存在下面几个不同的区域：

![](./images/java-monitor.png)

* `Entry Set` - 表示线程通过 `synchronized` 要求获取对象的锁，如果对象未被锁住，则变为 `The Owner`，否则则在 `Entry Set` 等待。一旦对象锁被其他线程释放，立即参与竞争；
* `The Owner` - 表示线程成功竞争到对象锁；
* `Wait Set` - 表示线程通过对象的 `wait` 方法释放对象的锁，并在等待区等待被唤醒。

#### 死锁检测

`jstack` 不仅能输出 Java 进程当前的线程堆栈，而且还能对线程进行死锁检查，如果它发现存在死锁问题，会在最下面输出它找到的死锁。这里有一个简单的 [死锁演示程序](../demo-3/)，运行之后可以看到两个线程在互相等待，我们使用 `jstack` 命令对其进行检查，可以看到下面输出了死锁信息：

```
Found one Java-level deadlock:
=============================
"Thread-B":
  waiting for ownable synchronizer 0x00000000fbe5eda0, (a java.util.concurrent.locks.ReentrantLock$NonfairSync),
  which is held by "Thread-A"
"Thread-A":
  which is held by "Thread-B"

Java stack information for the threads listed above:
===================================================
"Thread-B":
        at sun.misc.Unsafe.park(Native Method)
        - parking to wait for  <0x00000000fbe5eda0> (a java.util.concurrent.locks.ReentrantLock$NonfairSync)
        at java.util.concurrent.locks.LockSupport.park(LockSupport.java:175)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.parkAndCheckInterrupt(AbstractQueuedSynchronizer.java:836)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.acquireQueued(AbstractQueuedSynchronizer.java:870)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.acquire(AbstractQueuedSynchronizer.java:1199)
        at java.util.concurrent.locks.ReentrantLock$NonfairSync.lock(ReentrantLock.java:209)
        at java.util.concurrent.locks.ReentrantLock.lock(ReentrantLock.java:285)
        at com.example.DemoApp.lambda$1(DemoApp.java:36)
        at com.example.DemoApp$$Lambda$2/1123225098.run(Unknown Source)
        at java.lang.Thread.run(Thread.java:750)
"Thread-A":
        at sun.misc.Unsafe.park(Native Method)
        - parking to wait for  <0x00000000fbe5edd0> (a java.util.concurrent.locks.ReentrantLock$NonfairSync)
        at java.util.concurrent.locks.LockSupport.park(LockSupport.java:175)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.parkAndCheckInterrupt(AbstractQueuedSynchronizer.java:836)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.acquireQueued(AbstractQueuedSynchronizer.java:870)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.acquire(AbstractQueuedSynchronizer.java:1199)
        at java.util.concurrent.locks.ReentrantLock$NonfairSync.lock(ReentrantLock.java:209)
        at java.util.concurrent.locks.ReentrantLock.lock(ReentrantLock.java:285)
        at com.example.DemoApp.lambda$0(DemoApp.java:19)
        at com.example.DemoApp$$Lambda$1/1151020327.run(Unknown Source)
        at java.lang.Thread.run(Thread.java:750)

Found 1 deadlock.
```

## `jstack -l <pid>`

正常情况下 `jstack` 只会打印线程的堆栈信息，使用 `-l` 选项可以用于输出有关该线程锁的信息，如下所示：

```
"Thread-B" #15 prio=5 os_prio=0 tid=0x000001b5934fb800 nid=0x18c4 waiting on condition [0x000000519abfe000]
   java.lang.Thread.State: WAITING (parking)
        at sun.misc.Unsafe.park(Native Method)
        - parking to wait for  <0x00000000fbe5eda0> (a java.util.concurrent.locks.ReentrantLock$NonfairSync)
        at java.util.concurrent.locks.LockSupport.park(LockSupport.java:175)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.parkAndCheckInterrupt(AbstractQueuedSynchronizer.java:836)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.acquireQueued(AbstractQueuedSynchronizer.java:870)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.acquire(AbstractQueuedSynchronizer.java:1199)
        at java.util.concurrent.locks.ReentrantLock$NonfairSync.lock(ReentrantLock.java:209)
        at java.util.concurrent.locks.ReentrantLock.lock(ReentrantLock.java:285)
        at com.example.DemoApp.lambda$1(DemoApp.java:36)
        at com.example.DemoApp$$Lambda$2/1123225098.run(Unknown Source)
        at java.lang.Thread.run(Thread.java:750)

   Locked ownable synchronizers:
        - <0x00000000fbe5edd0> (a java.util.concurrent.locks.ReentrantLock$NonfairSync)

"Thread-A" #14 prio=5 os_prio=0 tid=0x000001b5934fa800 nid=0x1f1c waiting on condition [0x000000519aaff000]
   java.lang.Thread.State: WAITING (parking)
        at sun.misc.Unsafe.park(Native Method)
        - parking to wait for  <0x00000000fbe5edd0> (a java.util.concurrent.locks.ReentrantLock$NonfairSync)
        at java.util.concurrent.locks.LockSupport.park(LockSupport.java:175)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.parkAndCheckInterrupt(AbstractQueuedSynchronizer.java:836)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.acquireQueued(AbstractQueuedSynchronizer.java:870)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer.acquire(AbstractQueuedSynchronizer.java:1199)
        at java.util.concurrent.locks.ReentrantLock$NonfairSync.lock(ReentrantLock.java:209)
        at java.util.concurrent.locks.ReentrantLock.lock(ReentrantLock.java:285)
        at com.example.DemoApp.lambda$0(DemoApp.java:19)
        at com.example.DemoApp$$Lambda$1/1151020327.run(Unknown Source)
        at java.lang.Thread.run(Thread.java:750)

   Locked ownable synchronizers:
        - <0x00000000fbe5eda0> (a java.util.concurrent.locks.ReentrantLock$NonfairSync)
```

在线程堆栈的下方，可以看到 `Locked ownable synchronizers` 这样的信息，这个表示的是该线程持有的锁，很显然，`Thread-B` 持有锁 `0x00000000fbe5edd0`，`Thread-A` 持有锁 `0x00000000fbe5eda0`；另外，堆栈中的 `parking to wait for` 表示线程在等待的锁，`Thread-B` 在等待锁 `0x00000000fbe5eda0`，`Thread-A` 在等待锁 `0x00000000fbe5edd0`；两个线程互相等待，所以出现了死锁。

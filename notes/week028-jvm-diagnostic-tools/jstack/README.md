## jstack

用于生成 Java 虚拟机当前时刻的线程快照

* 命令格式：
    * jstack option LVMID
* 用途
    * 定位线程出现长时间停顿的原因，如线程间死锁、死循环、请求外部资源导致的长时间等待等

```
# jstack -l 20636
2022-11-30 09:00:58
Full thread dump OpenJDK 64-Bit Server VM (25.342-b07 mixed mode):

"Attach Listener" #115 daemon prio=9 os_prio=0 tid=0x00007f142c001000 nid=0x1f4f waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

   Locked ownable synchronizers:
        - None

"NIOWorkerThread-64" #114 daemon prio=5 os_prio=0 tid=0x00007f1384022000 nid=0x518a waiting on condition [0x00007f148f3f2000]
   java.lang.Thread.State: WAITING (parking)
        at sun.misc.Unsafe.park(Native Method)
        - parking to wait for  <0x00000000c1810720> (a java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject)
        at java.util.concurrent.locks.LockSupport.park(LockSupport.java:175)
        at java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject.await(AbstractQueuedSynchronizer.java:2039)
        at java.util.concurrent.LinkedBlockingQueue.take(LinkedBlockingQueue.java:442)
        at java.util.concurrent.ThreadPoolExecutor.getTask(ThreadPoolExecutor.java:1074)
        at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1134)
        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
        at java.lang.Thread.run(Thread.java:750)

   Locked ownable synchronizers:
        - None

...
```

### 线程分析

* 线程的几种状态
    * NEW
    * RUNNABLE
    * BLOCKED
    * WAITING
    * TIMED_WAITING
    * TERMINATED

![](./images/thread-states.jpg)

* Monitor
    * 用以实现线程之间的互斥与协作
    * 每个对象有且仅有一个
* Entry Set：表示线程通过 synchronized 要求获取对象的锁，如果对象未被锁住，则变为 The Owner，否则则在 Entry Set 等待。一旦对象锁被其他线程释放，立即参与竞争。
* The Owner：表示线程成功竞争到对象锁。
* Wait Set：表示线程通过对象的 wait 方法释放对象的锁，并在等待区等待被唤醒。

![](./images/java-monitor.png)

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
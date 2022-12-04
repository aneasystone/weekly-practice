## jmap（ JVM Memory Map ）

生成 heap dump 文件，查询 finalize 执行队列、Java 堆和永久代的详细信息

* 命令格式
    * jmap [option] LVMID
* 常见 option
    * dump : 生成堆转储快照
    * -XX:+HeapDumpOnOutOfMemoryError
    * finalizerinfo : 显示在 F-Queue 队列等待 Finalizer 线程执行 finalizer 方法的对象
    * heap : 显示堆详细信息
    * histo : 显示堆中对象的统计信息
* 替代工具：jcmd

```
# jmap -dump:live,format=b,file=dump.hprof 20636
Dumping heap to /root/dump.hprof ...
Heap dump file created
```

```
# jmap -heap 20636
Attaching to process ID 20636, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 25.342-b07

using thread-local object allocation.
Parallel GC with 23 thread(s)

Heap Configuration:
   MinHeapFreeRatio         = 0
   MaxHeapFreeRatio         = 100
   MaxHeapSize              = 1048576000 (1000.0MB)
   NewSize                  = 349175808 (333.0MB)
   MaxNewSize               = 349175808 (333.0MB)
   OldSize                  = 699400192 (667.0MB)
   NewRatio                 = 2
   SurvivorRatio            = 8
   MetaspaceSize            = 21807104 (20.796875MB)
   CompressedClassSpaceSize = 1073741824 (1024.0MB)
   MaxMetaspaceSize         = 17592186044415 MB
   G1HeapRegionSize         = 0 (0.0MB)

Heap Usage:
PS Young Generation
Eden Space:
   capacity = 57671680 (55.0MB)
   used     = 47560256 (45.35699462890625MB)
   free     = 10111424 (9.64300537109375MB)
   82.46726296164773% used
From Space:
   capacity = 1048576 (1.0MB)
   used     = 0 (0.0MB)
   free     = 1048576 (1.0MB)
   0.0% used
To Space:
   capacity = 1048576 (1.0MB)
   used     = 0 (0.0MB)
   free     = 1048576 (1.0MB)
   0.0% used
PS Old Generation
   capacity = 262668288 (250.5MB)
   used     = 10726192 (10.229293823242188MB)
   free     = 251942096 (240.2707061767578MB)
   4.083550428439995% used

4773 interned Strings occupying 390856 bytes.
```

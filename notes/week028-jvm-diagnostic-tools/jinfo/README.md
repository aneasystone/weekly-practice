## jinfo - JVM Configuration info

实时查看和调整虚拟机运行参数

* 命令格式
    * jinfo [option] [args] LVMID
    * jps –v 只能查看到显示指定的参数，jinfo 可以查看未被显示指定的参数
* 参数
    * -flag : 输出指定 args 参数的值（也可修改）
    * -flags : 不需要 args 参数，输出所有 JVM 参数的值
    * -sysprops : 输出系统属性，等同于 System.getProperties()

```
# jinfo -flags 20636
Attaching to process ID 20636, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 25.342-b07
Non-default VM flags: -XX:CICompilerCount=15 -XX:+HeapDumpOnOutOfMemoryError -XX:InitialHeapSize=1048576000 -XX:+ManagementServer -XX:MaxHeapSize=1048576000 -XX:MaxNewSize=349175808 -XX:MinHeapDeltaBytes=524288 -XX:NewSize=349175808 -XX:OldSize=699400192 -XX:OnOutOfMemoryError=null -XX:+UseCompressedClassPointers -XX:+UseCompressedOops -XX:+UseParallelGC 
Command line:  -Dzookeeper.log.dir=/root/apache-zookeeper-3.5.5-bin/bin/../logs -Dzookeeper.log.file=zookeeper-local.log -Dzookeeper.root.logger=INFO,CONSOLE -Dzookeeper.4lw.commands.whitelist=* -XX:+HeapDumpOnOutOfMemoryError -XX:OnOutOfMemoryError=kill -9 %p -Xmx1000m -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.local.only=false
```
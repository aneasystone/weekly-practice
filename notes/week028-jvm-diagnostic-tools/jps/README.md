## jps - JVM Process Status Tool

显示所有的 HotSpot 虚拟机进程

* 命令格式
    * jps [options] [hostid]
* 主要参数
    * -l : 输出主类全名或 jar 路径
    * -q : 只输出 LVMID
    * -m : 输出 JVM 启动时传递给 main() 的参数
    * -v : 输出 JVM 启动时显示指定的 JVM 参数

```
# jps -l
30362 sun.tools.jps.Jps
20636 org.apache.zookeeper.server.quorum.QuorumPeerMain
20895 ./zkui-2.0-SNAPSHOT-jar-with-dependencies.jar
```
## jstatd - JVM jstat Daemon

前面在学习 `jps`、`jinfo`、`jstat` 等等这些工具时，都只是监控本机的 Java 程序，那如果我们的 Java 程序运行在远程主机上怎么办呢？一种简单的方法就是使用 JDK 自带的 `jstatd` 服务。

`jstatd` 是一个 RMI 服务器，它的作用相当于代理。不过要注意的是，直接运行它会报错：

```
$ jstatd
Could not create remote object
access denied ("java.util.PropertyPermission" "java.rmi.server.ignoreSubClasses" "write")
java.security.AccessControlException: access denied ("java.util.PropertyPermission" "java.rmi.server.ignoreSubClasses" "write")
        at java.security.AccessControlContext.checkPermission(AccessControlContext.java:472)
        at java.security.AccessController.checkPermission(AccessController.java:886)
        at java.lang.SecurityManager.checkPermission(SecurityManager.java:549)
        at java.lang.System.setProperty(System.java:806)
        at sun.tools.jstatd.Jstatd.main(Jstatd.java:139)
```

看错误日志，是由于 `jstatd` 没有足够的权限，可以使用 [Java 的安全策略](https://docs.oracle.com/javase/7/docs/technotes/guides/security/PolicyFiles.html) 对它分配权限。我们创建一个安全策略文件 `jstatd.all.policy`，内容如下：

```
grant codebase "file:C:/Program Files/Java/jdk1.8.0_351/lib/tools.jar" {
   permission java.security.AllPermission;
};
```

然后使用下面的方法重新启动 `jstatd` 服务：

```
$ jstatd -J-Djava.security.policy=./jstatd.all.policy
```

默认情况下，`jstatd` 会在 1099 端口开启 RMI 服务器，可以使用 `-p` 参数修改端口：

```
$ jstatd -p 2099 -J-Djava.security.policy=./jstatd.all.policy
```

`jstatd` 服务启动成功后，就可以在本地监控远程服务器上的 Java 进程了。下面的命令通过 `jps` 显示了远程服务器上的 Java 进程：

```
$ jps localhost:1099
5204 org.eclipse.equinox.launcher_1.6.400.v20210924-0641.jar
5380 Jstatd
8936 BootLanguageServerBootApp
5900 Jps
8204 DemoApp
```

下面的命令通过 `jstat` 监控远程服务器上某个 Java 进程的 GC 堆使用情况：

```
$ jstat -gcutil 8204@localhost:2099
  S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT
  0.00   0.00  20.01   0.00  17.56  19.80      0    0.000     0    0.000    0.000
```

不过貌似 `jstatd` 只支持 `jps` 和 `jstat` 两个工具进行连接，使用其他的工具连接时会报错：

```
$ jstack 8204@localhost:1099
Attaching to remote server 8204@localhost:1099, please wait...
Error attaching to remote server: java.rmi.NotBoundException: SARemoteDebugger_8204
sun.jvm.hotspot.debugger.DebuggerException: java.rmi.NotBoundException: SARemoteDebugger_8204
        at sun.jvm.hotspot.RMIHelper.lookup(RMIHelper.java:115)
        at sun.jvm.hotspot.HotSpotAgent.connectRemoteDebugger(HotSpotAgent.java:517)
        at sun.jvm.hotspot.HotSpotAgent.setupDebugger(HotSpotAgent.java:374)
        at sun.jvm.hotspot.HotSpotAgent.go(HotSpotAgent.java:304)
        at sun.jvm.hotspot.HotSpotAgent.attach(HotSpotAgent.java:183)
        at sun.jvm.hotspot.tools.Tool.start(Tool.java:196)
        at sun.jvm.hotspot.tools.Tool.execute(Tool.java:118)
        at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
        at java.lang.reflect.Method.invoke(Method.java:498)
        at sun.tools.jstack.JStack.main(JStack.java:106)
Caused by: java.rmi.NotBoundException: SARemoteDebugger_8204
        at sun.rmi.registry.RegistryImpl.lookup(RegistryImpl.java:227)
        at sun.rmi.server.UnicastServerRef.oldDispatch(UnicastServerRef.java:469)
        at sun.rmi.server.UnicastServerRef.dispatch(UnicastServerRef.java:301)
        at sun.rmi.transport.Transport$1.run(Transport.java:197)
        at java.security.AccessController.doPrivileged(Native Method)
        at sun.rmi.transport.Transport.serviceCall(Transport.java:196)
        at sun.rmi.transport.tcp.TCPTransport.handleMessages(TCPTransport.java:573)
        at sun.rmi.transport.tcp.TCPTransport$ConnectionHandler.run0(TCPTransport.java:834)
        at sun.rmi.transport.tcp.TCPTransport$ConnectionHandler.lambda$run$0(TCPTransport.java:688)
        at java.security.AccessController.doPrivileged(Native Method)
        at sun.rmi.transport.tcp.TCPTransport$ConnectionHandler.run(TCPTransport.java:687)
        at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
        at java.lang.Thread.run(Thread.java:750)
        at sun.rmi.transport.StreamRemoteCall.exceptionReceivedFromServer(StreamRemoteCall.java:303)
        at sun.rmi.transport.StreamRemoteCall.executeCall(StreamRemoteCall.java:279)
        at sun.rmi.server.UnicastRef.invoke(UnicastRef.java:379)
        at sun.rmi.registry.RegistryImpl_Stub.lookup(RegistryImpl_Stub.java:123)
        at java.rmi.Naming.lookup(Naming.java:101)
        at sun.jvm.hotspot.RMIHelper.lookup(RMIHelper.java:113)
        ... 13 more
```

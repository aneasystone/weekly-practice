## jsadebugd - Serviceability Agent Debug Daemon for Java

在使用 [jstatd](../jstatd/README.md) 的时候，我们发现只有 `jps` 和 `jstat` 两个工具能远程连接上，而其他的工具如 `jinfo` 和 `jstack` 等连接时都会报错。这是因为 JDK 将这些工具分成了两大类：`jps` 和 `jstat` 被归类为 `Monitoring Tools`，而 `jinfo` 和 `jstack` 等被归类为 `Troubleshooting Tools`，这些 `Troubleshooting Tools` 也支持远程连接，不过在远程服务器上必须启动调试服务器（Debug Server）才行。

`jsadebugd` 命令就是用于在远程启动一个调试服务器，它和 `jstatd` 一样，也是一个 RMI 服务器，相当于客户端工具和远程 Java 进程中间的代理。不过和 `jstatd` 不一样的是，它需要 Attach 到某个 Java 进程或者某个核心文件，它的命令格式如下：

```
$ jsadebugd -help
Usage: jsadebugd [options] <pid> [server-id]
                (to connect to a live java process)
   or  jsadebugd [options] <executable> <core> [server-id]
                (to connect to a core file produced by <executable>)
                server-id is an optional unique id for this debug server, needed
                if multiple debug servers are run on the same machine
where options include:
   -h | -help   to print this help message
```

### `jsadebugd <pid> <server-id>`

使用下面的命令 Attach 到某个 Java 进程，并启动调试服务器：

```
$ jsadebugd 3680 demo
Attaching to process ID 3680 and starting RMI services, please wait...
Debugger attached and RMI services started.
```

调试服务器启动后，就可以使用 `jinfo` 和 `jstack` 等远程连接，使用方法和本地一样，只不过 `<pid>` 参数换成了 `<server-id>@<ip>:<port>`（RMI 服务器的端口号默认为 1099）：

```
$ jinfo -flags demo@localhost:1099
```

```
$ jmap -heap demo@localhost:1099
```

```
$ jstack -l demo@localhost:1099
```

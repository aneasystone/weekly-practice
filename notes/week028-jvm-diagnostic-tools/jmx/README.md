## jmx - Java Management Extensions Agent

自 Java 6 开始，Java 程序启动时都会在 JVM 内部启动一个 [JMX Agent](https://docs.oracle.com/javase/8/docs/technotes/guides/management/agent.html)，`JMX Agent` 会启动一个 `MBean Server` 组件，把 `MBeans`（ 包括 Java 平台标准的 `MBean` 和你自己创建的 `MBean` ）注册到它里面，然后暴露给 `JMX Client` 管理。简单来说就是每个 Java 程序都可以通过 JMX 来被 `JMX Client` 管理，而且这一切都是自动完成的。而 JConsole 和 VisualVM 就是 `JMX Client`，它们能够自动发现本机的 Java 进程，也可以通过显式地配置 JMX 连接来监控远程主机上的 Java 进程。

在程序启动时指定下面的参数来开启 JMX 功能：

```
-Dcom.sun.management.jmxremote=true \
-Dcom.sun.management.jmxremote.port=9091 \
-Dcom.sun.management.jmxremote.ssl=false \
-Dcom.sun.management.jmxremote.authenticate=false
```

> 也可以使用 `jcmd` 的 `ManagementAgent.start` 命令来开启 JMX 功能：
> 
> ```
> $ jcmd 4332 ManagementAgent.start jmxremote.port=9999 jmxremote.ssl=false jmxremote.authenticate=false
> 4332:
> Command executed successfully
> ```

JMX 开启后就可以在 JConsole 或 VisualVM 等工具中通过远程连接 `localhost:9091` 来管理 Java 程序了。

JMX 实际上是一个 Java Agent 程序，位于 `jre/lib/management-agent.jar`，它也有自己的配置文件，位于 `jre/lib/management` 目录，我们可以在 `management.properties` 文件中找到 JMX 支持的所有配置参数。

### 设置主机名

有时候可能因为主机名解析问题导致连接不上 JMX 端口，可以通过设置 `-Djava.rmi.server.hostname=127.0.0.1` 和 `-Dcom.sun.management.jmxremote.host=127.0.0.1` 参数来解决：

```
-Djava.rmi.server.hostname=127.0.0.1 \
-Dcom.sun.management.jmxremote=true \
-Dcom.sun.management.jmxremote.local.only=false \
-Dcom.sun.management.jmxremote.port=9091 \
-Dcom.sun.management.jmxremote.host=127.0.0.1 \
-Dcom.sun.management.jmxremote.rmi.port=9092 \
-Dcom.sun.management.jmxremote.ssl=false \
-Dcom.sun.management.jmxremote.authenticate=false
```

### 设置访问密码

在上面的启动参数中，我们使用 `-Dcom.sun.management.jmxremote.authenticate=false` 参数关闭了 JMX 的认证功能，但是在公开环境暴露 JMX 端口可能存在一定的安全隐患，这时我们需要开启密码认证：

```
-Dcom.sun.management.jmxremote=true \
-Dcom.sun.management.jmxremote.port=9091 \
-Dcom.sun.management.jmxremote.ssl=false \
-Dcom.sun.management.jmxremote.authenticate=true \
-Dcom.sun.management.jmxremote.access.file=./jmx.access \
-Dcom.sun.management.jmxremote.password.file=./jmx.password
```

我们需要将 `authenticate` 参数设置为 `true`，另外，还需要添加一个访问权限文件 `jmx.access` 和密码文件 `jmx.password`。访问权限文件 `jmx.access` 的内容如下：

```
user readonly
admin readwrite
```

`readonly` 表示只能读取 MBean 的属性和接受通知，`readwrite` 表示不仅能读取 MBean 的属性和接受通知，而且还允许修改属性，调用方法，创建和删除 MBean 等。

密码文件 `jmx.password` 的内容如下：

```
user 123456
admin 123456
```

不过这个时候直接运行 Java 程序会报错：

```
错误: 必须限制口令文件读取访问权限: ./jmx.password
```

这是因为我们这里的密码文件是明文，为了保证安全性，必须将其设置成只有当前用户能访问，并且只有可读的权限：

```
$ chown <username>:<username>
$ chmod 400 jmx.password
```

> 如果是 Windows 系统，可以使用命令：`cacls jmx.password /P <username>:R`

再次重启 Java 程序后，使用 JMX Client 连接时就必须输入用户名和密码了。

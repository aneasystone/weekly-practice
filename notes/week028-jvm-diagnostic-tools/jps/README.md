## jps - JVM Process Status Tool

`jps` 命令类似于 Linux 下的 `ps` 命令，只不过它只显示 Java 进程。使用 `jps` 可以方便地查看 Java 进程的启动类、启动参数和 JVM 参数等。

### `jps`

不带任何参数的 `jps` 命令可以列出所有 Java 进程的 PID 和主函数类名（对于 `java -jar` 启动的程序显示的是 jar 文件名称）：

```
$ jps
8384 org.eclipse.equinox.launcher_1.6.400.v20210924-0641.jar
9648 Jps
2232 DemoApplication
2812 BootLanguageServerBootApp
```

### `jps -q`

`-q` 参数用于只输出进程 PID：

```
$ jps -q
8384
2232
12772
2812
```

### `jps -m`

`-m` 参数用于显示 Java 进程的启动参数：

```
$ jps -m
8384 org.eclipse.equinox.launcher_1.6.400.v20210924-0641.jar -configuration c:\Users\aneasystone\AppData\Roaming\Code\User\globalStorage\redhat.java\1.13.0\config_win -data c:\Users\aneasystone\AppData\Roaming\Code\User\workspaceStorage\0a27248ad31d34f0a29508e47798626c\redhat.java\jdt_ws
12040 Jps -m
2232 DemoApplication
2812 BootLanguageServerBootApp
```

### `jps -l`

`-l` 参数用于输出主函数的完整类名（对于 `java -jar` 启动的程序显示的是 jar 文件路径）

```
> jps -l
8384 c:\Users\aneasystone\.vscode\extensions\redhat.java-1.13.0-win32-x64\server\plugins\org.eclipse.equinox.launcher_1.6.400.v20210924-0641.jar
2232 com.example.demo.DemoApplication
7048 sun.tools.jps.Jps
2812 org.springframework.ide.vscode.boot.app.BootLanguageServerBootApp
```

### `jps -v`

`-v` 参数用于输出所有显式地传给 Java 程序的 JVM 参数：

```
$ jps -v
8384 org.eclipse.equinox.launcher_1.6.400.v20210924-0641.jar --add-modules=ALL-SYSTEM --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.nio.fs=ALL-UNNAMED -Declipse.application=org.eclipse.jdt.ls.core.id1 -Dosgi.bundles.defaultStartLevel=4 -Declipse.product=org.eclipse.jdt.ls.core.product -Djava.import.generatesMetadataFilesAtProjectRoot=false -Dfile.encoding=utf8 -XX:+UseParallelGC -XX:GCTimeRatio=4 -XX:AdaptiveSizePolicyWeight=90 -Dsun.zip.disableMemoryMapping=true -Xmx1G -Xms100m -Xlog:disable -javaagent:c:\Users\aneasystone\.vscode\extensions\redhat.java-1.13.0-win32-x64\lombok\lombok-1.18.24.jar -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=c:\Users\aneasystone\AppData\Roaming\Code\User\workspaceStorage\0a27248ad31d34f0a29508e47798626c\redhat.java
10980 Jps -Dapplication.home=C:\Program Files\Java\jdk1.8.0_351 -Xms8m
2232 DemoApplication -agentlib:jdwp=transport=dt_socket,server=n,suspend=y,address=localhost:53871
2812 BootLanguageServerBootApp -Dsts.lsp.client=vscode -Dsts.log.file=/dev/null -XX:TieredStopAtLevel=1 -Xlog:jni+resolve=off -Dspring.config.location=file:c:\Users\aneasystone\.vscode\extensions\pivotal.vscode-spring-boot-1.40.0\language-server\BOOT-INF\classes\application.properties
```

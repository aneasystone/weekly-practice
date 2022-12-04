## jhat（ JVM Heap Analysis Tool ）

与 jmap 搭配使用，用来分析 jmap 生成的 dump

* 命令格式
    * jhat [options] [dumpfile]
* 注意事项
    * 内置微型的 HTTP 服务器，生成分析结果后，可以在浏览器中查看，默认端口 7000
    * 一般不会直接在服务器上进行分析，因为 jhat 是一个耗时并且耗费硬件资源的过程，一般把服务器生成的 dump 文件复制到本地进行分析

```
# jhat /root/dump.hprof
Reading from /root/dump.hprof...
Dump file created Wed Nov 30 09:00:09 CST 2022
Snapshot read, resolving...
Resolving 142345 objects...
Chasing references, expect 28 dots............................
Eliminating duplicate references............................
Snapshot resolved.
Started HTTP server on port 7000
Server is ready.
```
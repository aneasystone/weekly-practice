# WEEK045 - 使用 Arthas 排查线上问题

[Arthas](https://arthas.aliyun.com/) 是阿里开源的一款 Java 应用诊断工具，可以在线排查问题，动态跟踪 Java 代码，以及实时监控 JVM 状态。这个工具的大名我早有耳闻，之前一直听别人推荐，却没有使用过。最近在线上遇到了一个问题，由于开发人员在异常处理时没有将线程堆栈打印出来，只是简单地抛出了一个系统错误，导致无法确定异常的具体来源；因为是线上环境，如果要修改代码重新发布，流程会非常漫长，所以只能通过分析代码来定位，正当我看着繁复的代码一筹莫展的时候，突然想到了 Arthas 这个神器，于是尝试着使用 Arthas 来排查这个问题，没想到轻松几步就定位到了原因，上手非常简单，着实让我很吃惊。正所谓 “工欲善其事，必先利其器”，这话果真不假，于是事后花了点时间对 Arthas 的各种用法学习了一番，此为总结。

## 基本使用

如果是联网环境，可以直接使用下面的命令下载并运行 Arthas：

```
$ wget https://arthas.aliyun.com/arthas-boot.jar
$ java -jar arthas-boot.jar
```

```
$ curl -X POST -H "Content-Type: application/json" -d '{"x":1,"y":2}' http://localhost:8080/add
3
```

```
$ curl -X POST -H "Content-Type: application/json" -d '{"x":1}' http://localhost:8080/add
系统错误！
```

## 线上问题排查

### 使用 `watch` 监听函数出入参和异常

### 使用 `jad/sc/redefine` 热更新代码

### 排查类冲突问题

### 性能分析

## 参考

* [Arthas 文档](https://arthas.aliyun.com/doc/)
* [OGNL 参考文档](https://commons.apache.org/proper/commons-ognl/language-guide.html)
* [Arthas 在线教程 - Killercoda](https://killercoda.com/arthas/course/arthas-tutorials-cn)
* [谈谈阿里arthas背后的原理](https://developer.aliyun.com/article/1004682)
* [Arthas运行原理](https://zhuanlan.zhihu.com/p/115127052)
* [Arthas原理系列(五)：watch命令的实现原理](https://juejin.cn/post/6908874607474769934)
* [Arthas原理：如何做到与应用代码隔离？](https://yeas.fun/archives/arthas-isolation)

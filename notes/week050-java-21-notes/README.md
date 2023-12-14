# WEEK050 - Java 21 初体验

2023 年 9 月 19 日，[Java 21](https://openjdk.org/projects/jdk/21/) 发布正式版本，这是 Java 时隔两年发布的又一个 LTS 版本，上一个 LTS 版本是 2021 年 9 月 14 日发布的 [Java 17](https://openjdk.org/projects/jdk/17/)：

![](./images/jdk-versions.png)

Java 17 目前是使用最广泛的版本，但随着 Java 21 的发布，这一局面估计会很快被打破，这是因为 Java 21 可能是几年内最为重要的版本，它带来了一系列重要的功能和特性，包括 [记录模式](https://openjdk.org/jeps/440)，[`switch` 模式匹配](https://openjdk.org/jeps/441)，[字符串模板](https://openjdk.org/jeps/430)，[分代式 ZGC](https://openjdk.org/jeps/439)，[不需要定义类的 Main 方法](https://openjdk.org/jeps/445)，等等等等，不过其中最为重要的一项，当属由 [Loom 项目](https://openjdk.org/projects/loom/) 发展而来的 [虚拟线程](https://openjdk.org/jeps/444)。Java 程序一直以文件体积大、启动速度慢、内存占用多被人诟病，但是有了虚拟线程，再结合 [GraalVM](https://www.graalvm.org/) 的原生镜像，我们就可以写出媲美 C、Rust 或 Go 一样小巧灵活、高性能、可伸缩的应用程序。

转眼间，距离 Java 21 发布已经快 3 个月了，网上相关的文章也已经铺天盖地，为了不使自己落伍，于是便打算花点时间学习一下。尽管在坊间一直流传着 **版本任你发，我用 Java 8** 这样的说法，但是作为一线 Java 开发人员，最好还是紧跟大势，未雨绸缪，有备无患。而且最重要的是，随着 [Spring Boot 2.7.18 的发布，2.x 版本将不再提供开源支持](https://spring.io/blog/2023/11/23/spring-boot-2-7-18-available-now)，而 3.x 不支持 Java 8，最低也得 Java 17，所以仍然相信这种说法的人除非不使用 Spring Boot，要么不升级 Spring Boot，否则学习 Java 新版本都是势在必行。 

## 准备开发环境

我这里使用 Docker Desktop 的 [Dev Environments](https://docs.docker.com/desktop/dev-environments/) 作为我们的实验环境。Dev Environments 是 Docker Desktop 从 3.5.0 版本开始引入的一项新特性，目前还处于 Beta 阶段，它通过配置文件的方式方便开发人员创建容器化的、可复用的开发环境，结合 VSCode 的 [Dev Containers 插件](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) 以及它丰富的插件生态可以帮助开发人员迅速展开编码工作，而不用疲于开发环境的折腾。

![](./images/dev-environments.png)

Dev Environments 的界面如上图所示，官方提供了两个示例供参考，一个是单容器服务，一个是多容器服务：

* [https://github.com/dockersamples/single-dev-env](https://github.com/dockersamples/single-dev-env)
* [https://github.com/dockersamples/compose-dev-env](https://github.com/dockersamples/compose-dev-env)

我们可以直接从 Git 仓库地址来创建开发环境，就如官方提供的示例一样，也可以从本地目录创建开发环境，默认情况下，Dev Environments 会自动检测项目的语言和依赖，不过自动检测的功能并不是那么准确，比如我们的目录是一个 Java 项目，Dev Environments 会使用 [docker/dev-environments-java](https://hub.docker.com/r/docker/dev-environments-java) 镜像来创建开发环境，而这个镜像使用的是 Java 11，并不是我们想要的。

> 如果自动检测失败，就会使用 [docker/dev-environments-default](https://hub.docker.com/r/docker/dev-environments-default) 这个通用镜像来创建开发环境。

所以我们还得手动指定镜像，总的来说，就是在项目根目录下创建一个 `compose-dev.yaml` 配置文件，内容如下：

```
services:
  app:
    entrypoint:
    - sleep
    - infinity
    image: openjdk:21-jdk
    init: true
    volumes:
    - type: bind
      source: /var/run/docker.sock
      target: /var/run/docker.sock
```

然后再使用 Dev Environments 打开该目录，程序会自动拉取该镜像并创建开发环境：

![](./images/dev-environments-created.png)

开发环境创建成功后，我们就可以使用 VSCode 打开了：

![](./images/dev-environments-done.png)

使用 VSCode 打开开发环境，实际上就是使用 VSCode 的 [Dev Containers 插件](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) 连接到容器里面，打开终端，敲入 `java -version` 命令：

```
bash-4.4# java -version
openjdk version "21" 2023-09-19
OpenJDK Runtime Environment (build 21+35-2513)
OpenJDK 64-Bit Server VM (build 21+35-2513, mixed mode, sharing)
```

由于这是一个崭新的环境，我们还要为 VSCode 安装一些开发所需的插件，比如 [Extension Pack for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack)：

![](./images/vscode-dev-env.png)

至此我们就得到了一个非常干净纯粹的 Java 21 开发环境。

## 特性体验

接下来，我们就在这个全新的开发环境中一览 Java 21 的全部特性，包括下面 15 个 JEP：

* 430: [String Templates (Preview)](https://openjdk.org/jeps/430)
* 431: [Sequenced Collections](https://openjdk.org/jeps/431)
* 439: [Generational ZGC](https://openjdk.org/jeps/439)
* 440: [Record Patterns](https://openjdk.org/jeps/440)
* 441: [Pattern Matching for `switch`](https://openjdk.org/jeps/441)
* 442: [Foreign Function & Memory API (Third Preview)](https://openjdk.org/jeps/442)
* 443: [Unnamed Patterns and Variables (Preview)](https://openjdk.org/jeps/443)
* 444: [Virtual Threads](https://openjdk.org/jeps/444)
* 445: [Unnamed Classes and Instance Main Methods (Preview)](https://openjdk.org/jeps/445)
* 446: [Scoped Values (Preview)](https://openjdk.org/jeps/446)
* 448: [Vector API (Sixth Incubator)](https://openjdk.org/jeps/448)
* 449: [Deprecate the Windows 32-bit x86 Port for Removal](https://openjdk.org/jeps/449)
* 451: [Prepare to Disallow the Dynamic Loading of Agents](https://openjdk.org/jeps/451)
* 452: [Key Encapsulation Mechanism API](https://openjdk.org/jeps/452)
* 453: [Structured Concurrency (Preview)](https://openjdk.org/jeps/453)

### 字符串模板

字符串模板是很多语言都具备的特性，它允许在字符串中使用占位符来动态替换变量的值，这种构建字符串的方式比传统的字符串拼接或格式化更为简洁和直观。相信学过 JavaScript 的同学对下面这个 [Template literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals) 的语法不陌生：

```
const name = 'zhangsan'
const age = 18
const message = `My name is ${name}, I'm ${age} years old.`
console.log(message)
```

如上所示，JavaScript 通过反引号 ` 来定义字符串模板，而 Java 21 则引入了一个叫做 **模版表达式（Template expressions）** 的概念来定义字符串模板。下面是一个简单示例：

```
String name = "zhangsan";
int age = 18;
String message = STR."My name is \{name}, I'm \{age} years old.";
System.out.println(message);
```

看上去和 JavaScript 的 Template literals 非常相似，但还是有一些区别的，模版表达式包含三个部分：

* 首先是一个 **模版处理器（template processor）**：这里使用的是 `STR` 模板处理器，也可以是 `RAW` 或 `FMT` 等，甚至可以自定义；
* 中间是一个点号（`.`）；
* 最后跟着一个字符串模板，模板中使用 `\{name}` 和 `\{age}` 这样的占位符语法，这被称为 **内嵌表达式（embedded expression）**；

当模版表达式运行的时候，模版处理器会将模版内容与内嵌表达式的值组合起来，生成结果。

不过，当我们执行上述代码时，很可能会报 `Invalid escape sequence (valid ones are  \b  \t  \n  \f  \r  \"  \'  \\ )` 这样的错：

![](./images/preview-feature-error.png)

这是因为字符串模板还只是一个预览特性，根据 [JEP 12: Preview Features](https://openjdk.org/jeps/12)，我们需要添加 `--enable-preview` 参数开启预览特性，使用 `javac` 编译时，还需要添加 `--release` 参数。使用下面的命令将 `.java` 文件编译成 `.class` 文件：

```
$ javac --enable-preview --release 21 StringTemplates.java 
Note: StringTemplates.java uses preview features of Java SE 21.
Note: Recompile with -Xlint:preview for details.
```

再使用下面的命令运行 `.class` 文件：

```
$ java --enable-preview StringTemplates
My name is zhangsan, I'm 18 years old.
```

#### `STR` 模版处理器

`STR` 模板处理器中的内嵌表达式还有很多其他写法，比如执行数学运算：

```
int x = 1, y = 2;
String s1 = STR."\{x} + \{y} = \{x + y}";
```

调用方法：

```
String s2 = STR."Java version is \{getVersion()}";
```

访问字段：

```
Person p = new Person(name, age);
String s3 = STR."My name is \{p.name}, I'm \{p.age} years old.";
```

内嵌表达式中可以直接使用双引号，不用 `\"` 转义：

```
String s4 = STR."I'm \{age >= 18 ? "an adult" : "a child"}.";
```

内嵌表达式中可以编写注释和换行：

```
String s5 = STR."I'm \{
    // check the age
    age >= 18 ? "an adult" : "a child"
}.";
```

#### 多行模板表达式

在 Java 13 的 [JEP 355](https://openjdk.org/jeps/355) 中首次引入了 **文本块（Text Blocks）** 特性，并经过 Java 14 的 [JEP 368](https://openjdk.org/jeps/368) 和 Java 15 的 [JEP 378](https://openjdk.org/jeps/378) 两个版本的迭代，使得该特性正式可用，这个特性可以让我们在 Java 代码中愉快地使用多行字符串。在使用文本块之前，定义一个 JSON 格式的字符串可能会写出像下面这样无法直视的代码来：

```
String json1 = "{\n" +
               "  \"name\": \"zhangsan\",\n" +
               "  \"age\": 18\n" +
               "}\n";
```

但是在使用文本块之后，这样的代码就变得非常清爽：

```
String json2 = """
               {
                 "name": "zhangsan",
                 "age": 18
               }
               """;
```

文本块以三个双引号 `"""` 开始，同样以三个双引号结束，看上去和 Python 的多行字符串类似，不过 Java 的文本块会自动处理换行和缩进，使用起来更方便。上面的文本块在 Java 中输出如下：

```
{
  "name": "zhangsan",
  "age": 18
}

```

注意开头没有换行，结尾有一个换行。而在 Python 中输出如下：

```

               {
                 "name": "zhangsan",
                 "age": 18
               }

```

不仅开头和结尾都有换行，而且每一行有很多缩进，这里可以看出 Python 的处理很简单，它直接把 `"""` 之间的内容原样输出了，而 Java 是根据最后一个 `"""` 和内容之间的相对缩进来决定输出。很显然，我们更喜欢 Java 这样的输出结果，如果希望 Python 有同样的输出结果，就得这样写：

```
json = """{
  "name": "zhangsan",
  "age": 18
}
"""
```

这在代码的可读性上就比不上 Java 了，这里不得不感叹 Java 的设计，在细节的处理上做的确实不错。

言归正传，说回字符串模板这个特性，我们也可以在文本块中使用，如下：

```
String json3 = STR."""
               {
                 "name": "\{name}",
                 "age": \{age}
               }
               """;
```

#### `FMT` 模板处理器

`FMT` 是 Java 21 内置的另一个模版处理器，它不仅有 `STR` 模版处理器的插值功能，还可以对输出进行格式化操作。**格式说明符（format specifiers）** 放在嵌入表达式的左侧，如下所示：

```
%7.2f\{price}
```

支持的格式说明符参见 [java.util.Formatter](https://cr.openjdk.org/~jlaskey/templates/docs/api/java.base/java/util/Formatter.html) 文档。

> 不过在我的环境里编译时，会报错 `cannot find symbol: variable FMT`，就算是把镜像更换成 `openjdk:22-jdk` 也是一样的错，不清楚是为什么。

### 有序集合

[Java 集合框架（Java Collections Framework，JCF）](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/doc-files/coll-index.html) 为集合的表示和操作提供了一套统一的体系架构，让开发人员可以使用标准的接口来组织和操作集合，而不必关心底层的数据结构或实现方式。JCF 的接口大致可以分为 `Collection` 和 `Map` 两组，一共 15 个：

![](./images/jcf-interfaces.png)

在过去的 20 个版本里，这些接口已经被证明非常有用，在日常开发中发挥了重要的作用。那么 Java 21 为什么又要增加一个新的 **有序集合（Sequenced Collections）** 接口呢？

#### 不一致的顺序操作

这是因为这些接口在处理集合顺序问题时很不一致，导致了无谓的复杂性，比如要获取集合的第一个元素：

|               | 获取第一个元素                   |
| ------------- | ------------------------------- |
| List          | list.get(0)                     |
| Deque         | deque.getFirst()                |
| SortedSet     | sortedSet.first()               |
| LinkedHashSet | linkedHashSet.iterator().next() |

可以看到，不同的集合有着不同的实现。再比如获取集合的最后一个元素：

|               | 获取最后一个元素           |
| ------------- | ------------------------- |
| List          | list.get(list.size() - 1) |
| Deque         | deque.getLast()           |
| SortedSet     | sortedSet.last()          |
| LinkedHashSet | -                         |

List 的实现显得非常笨重，而 LinkedHashSet 根本没有提供直接的方法，只能将整个集合遍历一遍才能获取最后一个元素。

除了获取集合的第一个元素和最后一个元素，对集合进行逆序遍历也是各不相同，比如 `NavigableSet` 提供了 `descendingSet()` 方法来逆序遍历：

```
for (var e : navSet.descendingSet()) {
    process(e);
}
```

`Deque` 通过 `descendingIterator()` 来逆序遍历：

```
for (var it = deque.descendingIterator(); it.hasNext();) {
    var e = it.next();
    process(e);
}
```

而 `List` 则是通过 `listIterator()` 来逆序遍历：

```
for (var it = list.listIterator(list.size()); it.hasPrevious();) {
    var e = it.previous();
    process(e);
}
```

由此可见，与顺序相关的处理方法散落在 JCF 的不同地方，使用起来极为不便。于是，Java 21 为我们提供了一个描述和操作有序集合的新接口，这个接口定义了一些与顺序相关的方法，将这些散落在各个地方的逻辑集中起来，让我们更方便地处理有序集合。

#### 统一的有序集合接口

与顺序相关的操作主要包括三个方面：

* 获取集合的第一个或最后一个元素
* 向集合的最前面或最后面插入或删除元素
* 按照逆序遍历集合

为此，Java 21 新增了三个有序接口：`SequencedCollection`、`SequencedSet` 和 `SequencedMap`，他们的定义如下：

```
interface SequencedCollection<E> extends Collection<E> {
    SequencedCollection<E> reversed();
    void addFirst(E);
    void addLast(E);
    E getFirst();
    E getLast();
    E removeFirst();
    E removeLast();
}

interface SequencedSet<E> extends Set<E>, SequencedCollection<E> {
    SequencedSet<E> reversed();
}

interface SequencedMap<K,V> extends Map<K,V> {
    SequencedMap<K,V> reversed();
    SequencedSet<K> sequencedKeySet();
    SequencedCollection<V> sequencedValues();
    SequencedSet<Entry<K,V>> sequencedEntrySet();
    V putFirst(K, V);
    V putLast(K, V);
    Entry<K, V> firstEntry();
    Entry<K, V> lastEntry();
    Entry<K, V> pollFirstEntry();
    Entry<K, V> pollLastEntry();
}
```

他们在 JCF 大家庭中的位置如下图所示：

![](./images/sequenced-collection.png)

有了这些接口，对于所有的有序集合，我们都可以通过下面的方法来获取第一个和最后一个元素：

```
System.out.println("The first element is: " + list.getFirst());
System.out.println("The last element is: " + list.getLast());
```

逆序遍历也变得格外简单：

```
list.reversed().forEach(it -> System.out.println(it));
```

### 分代式 ZGC

想要搞清楚 Java 21 中的 **分代式 ZGC（Generational ZGC）** 这个特性，我们需要先搞清楚什么是 ZGC。

#### ZGC 简介

[ZGC（The Z Garbage Collector）](https://wiki.openjdk.org/display/zgc) 是由 Oracle 开发的一款垃圾回收器，最初在 Java 11 中以实验性功能推出，并经过几个版本的迭代，最终在 Java 15 中被宣布为 [Production Ready](https://openjdk.org/jeps/377)，相比于其他的垃圾回收器，ZGC 更适用于大内存、低延迟服务的内存管理和回收。下图展示的是不同的垃圾回收器所专注的目标也各不相同：

![](./images/gc-landscape.png)

低延迟服务的最大敌人是 GC 停顿，所谓 GC 停顿指的是垃圾回收期间的 **STW（Stop The World）**，当 STW 时，所有的应用线程全部暂停，等待 GC 结束后才能继续运行。要想实现低延迟，就要想办法减少 GC 的停顿时间，根据 [JEP 333](https://openjdk.org/jeps/333) 的介绍，最初 ZGC 的目标是：

* GC 停顿时间不超过 10ms；
* 支持处理小到几百 MB，大到 TB 量级的堆；
* 相对于使用 G1，应用吞吐量的降低不超过 15%；

经过几年的发展，目前 ZGC 的最大停顿时间已经优化到了不超过 1 毫秒（Sub-millisecond，亚毫秒级），且停顿时间不会随着堆的增大而增加，甚至不会随着 live-set 或 root-set 的增大而增加（通过 [JEP 376 Concurrent Thread-Stack Processing](https://openjdk.org/jeps/376) 实现），支持处理最小 8MB，最大 16TB 的堆：

![](./images/zgc-goals.png)

ZGC 之所以能实现这么快的速度，不仅是因为它在算法上做了大量的优化和改进，而且还革命性的使用了大量的创新技术，包括：

* Concurrent：全链路并发，ZGC 在整个垃圾回收阶段几乎全部实现了并发；
* Region-based：和 G1 类似，ZGC 是一种基于区域的垃圾回收器；
* Compacting：和 CMS、G1 一样，ZGC 使用了 **标记-复制算法**，该算法会产生内存碎片，所以要进行内存整理；
* NUMA-aware：NUMA 全称 Non-Uniform Memory Access（非一致内存访问），是一种多内存访问技术，使用 NUMA，CPU 会访问离它最近的内存，提升读写效率；
* Using colored pointers：染色指针是一种将数据存放在指针里的技术，JVM 是通过染色指针来标识某个对象是否需要被回收；
* Using load barriers：当应用程序从堆中读取对象引用时，JIT 会向应用代码中注入一小段代码，这就是读屏障；通过读屏障操作，当对象地址发生转移时，不仅赋值的引用更改为最新值，自身引用也被修正了，整个过程看起来像是自愈；

关于这些技术点，网上的参考资料有很多，有兴趣的同学可以通过本文的更多部分进一步学习。

#### ZGC 工作流程

https://www.yuanjava.cn/posts/ZGC/

#### ZGC 实践



### 记录模式

https://openjdk.org/jeps/440

### `switch` 模式匹配

https://openjdk.org/jeps/441

### 外部函数和内存 API

https://openjdk.org/jeps/442

### 未命名模式和变量

https://openjdk.org/jeps/443

### 虚拟线程

https://openjdk.org/jeps/444

### 未命名类和实例的 Main 方法

https://openjdk.org/jeps/445

### 作用域值

https://openjdk.org/jeps/446

### 向量 API

https://openjdk.org/jeps/448

### 弃用 Windows 32-bit x86 移植，为删除做准备

https://openjdk.org/jeps/449

### 准备禁用代理的动态加载

https://openjdk.org/jeps/451

### 密钥封装机制 API

https://openjdk.org/jeps/452

### 结构化并发

https://openjdk.org/jeps/453

## 参考

* [The Arrival of Java 21](https://blogs.oracle.com/java/post/the-arrival-of-java-21)
* [Java 版本历史](https://zh.wikipedia.org/wiki/Java%E7%89%88%E6%9C%AC%E6%AD%B7%E5%8F%B2)
* [Java 9 - 21：新特性解读](https://www.didispace.com/java-features/)
* [JDK11 升级 JDK17 最全实践干货来了 | 京东云技术团队](https://my.oschina.net/u/4090830/blog/10142895)
* [Java 21：下一个LTS版本，提供了虚拟线程、记录模式和模式匹配](https://www.infoq.cn/article/zIiqcmU8hiGhmuSAhzwb)
* [Hello, Java 21](https://spring.io/blog/2023/09/20/hello-java-21/)
* [Runtime efficiency with Spring (today and tomorrow)](https://spring.io/blog/2023/10/16/runtime-efficiency-with-spring)
* [GraalVM for JDK 21 is here!](https://medium.com/graalvm/graalvm-for-jdk-21-is-here-ee01177dd12d)

## 更多

### 垃圾回收

* [7 kinds of garbage collection for Java](https://opensource.com/article/22/7/garbage-collection-java)
* [GC progress from JDK 8 to JDK 17](https://kstefanj.github.io/2021/11/24/gc-progress-8-17.html)
* [Java中9种常见的CMS GC问题分析与解决](https://tech.meituan.com/2020/11/12/java-9-cms-gc.html)
* [亚毫秒GC暂停到底有多香？JDK17+ZGC初体验](https://tech.dewu.com/article?id=59)
* [ZGC关键技术分析](https://my.oschina.net/u/5783135/blog/10120461)
* [Per Liden 的博客](https://malloc.se/)

#### ZGC

* [An Introduction to ZGC: A Scalable and Experimental Low-Latency JVM Garbage Collector](https://www.baeldung.com/jvm-zgc-garbage-collector)

### Java 历史版本特性一览

#### Java 20

* 429: [Scoped Values (Incubator)](https://openjdk.org/jeps/429)
* 432: [Record Patterns (Second Preview)](https://openjdk.org/jeps/432)
* 433: [Pattern Matching for switch (Fourth Preview)](https://openjdk.org/jeps/433)
* 434: [Foreign Function & Memory API (Second Preview)](https://openjdk.org/jeps/434)
* 436: [Virtual Threads (Second Preview)](https://openjdk.org/jeps/436)
* 437: [Structured Concurrency (Second Incubator)](https://openjdk.org/jeps/437)
* 438: [Vector API (Fifth Incubator)](https://openjdk.org/jeps/438)

#### Java 19

* 405: [Record Patterns (Preview)](https://openjdk.org/jeps/405)
* 422: [Linux/RISC-V Port](https://openjdk.org/jeps/422)
* 424: [Foreign Function & Memory API (Preview)](https://openjdk.org/jeps/424)
* 425: [Virtual Threads (Preview)](https://openjdk.org/jeps/425)
* 426: [Vector API (Fourth Incubator)](https://openjdk.org/jeps/426)
* 427: [Pattern Matching for switch (Third Preview)](https://openjdk.org/jeps/427)
* 428: [Structured Concurrency (Incubator)](https://openjdk.org/jeps/428)

#### Java 18

* 400: [UTF-8 by Default](https://openjdk.org/jeps/400)
* 408: [Simple Web Server](https://openjdk.org/jeps/408)
* 413: [Code Snippets in Java API Documentation](https://openjdk.org/jeps/413)
* 416: [Reimplement Core Reflection with Method Handles](https://openjdk.org/jeps/416)
* 417: [Vector API (Third Incubator)](https://openjdk.org/jeps/417)
* 418: [Internet-Address Resolution SPI](https://openjdk.org/jeps/418)
* 419: [Foreign Function & Memory API (Second Incubator)](https://openjdk.org/jeps/419)
* 420: [Pattern Matching for switch (Second Preview)](https://openjdk.org/jeps/420)
* 421: [Deprecate Finalization for Removal](https://openjdk.org/jeps/421)

#### Java 17 (LTS)

* 306: [Restore Always-Strict Floating-Point Semantics](https://openjdk.org/jeps/306)
* 356: [Enhanced Pseudo-Random Number Generators](https://openjdk.org/jeps/356)
* 382: [New macOS Rendering Pipeline](https://openjdk.org/jeps/382)
* 391: [macOS/AArch64 Port](https://openjdk.org/jeps/391)
* 398: [Deprecate the Applet API for Removal](https://openjdk.org/jeps/398)
* 403: [Strongly Encapsulate JDK Internals](https://openjdk.org/jeps/403)
* 406: [Pattern Matching for switch (Preview)](https://openjdk.org/jeps/406)
* 407: [Remove RMI Activation](https://openjdk.org/jeps/407)
* 409: [Sealed Classes](https://openjdk.org/jeps/409)
* 410: [Remove the Experimental AOT and JIT Compiler](https://openjdk.org/jeps/410)
* 411: [Deprecate the Security Manager for Removal](https://openjdk.org/jeps/411)
* 412: [Foreign Function & Memory API (Incubator)](https://openjdk.org/jeps/412)
* 414: [Vector API (Second Incubator)](https://openjdk.org/jeps/414)
* 415: [Context-Specific Deserialization Filters](https://openjdk.org/jeps/415)

#### Java 16

* 338: [Vector API (Incubator)](https://openjdk.org/jeps/338)
* 347: [Enable C++14 Language Features](https://openjdk.org/jeps/347)
* 357: [Migrate from Mercurial to Git](https://openjdk.org/jeps/357)
* 369: [Migrate to GitHub](https://openjdk.org/jeps/369)
* 376: [ZGC: Concurrent Thread-Stack Processing](https://openjdk.org/jeps/376)
* 380: [Unix-Domain Socket Channels](https://openjdk.org/jeps/380)
* 386: [Alpine Linux Port](https://openjdk.org/jeps/386)
* 387: [Elastic Metaspace](https://openjdk.org/jeps/387)
* 388: [Windows/AArch64 Port](https://openjdk.org/jeps/388)
* 389: [Foreign Linker API (Incubator)](https://openjdk.org/jeps/389)
* 390: [Warnings for Value-Based Classes](https://openjdk.org/jeps/390)
* 392: [Packaging Tool](https://openjdk.org/jeps/392)
* 393: [Foreign-Memory Access API (Third Incubator)](https://openjdk.org/jeps/393)
* 394: [Pattern Matching for instanceof](https://openjdk.org/jeps/394)
* 395: [Records](https://openjdk.org/jeps/395)
* 396: [Strongly Encapsulate JDK Internals by Default](https://openjdk.org/jeps/396)
* 397: [Sealed Classes (Second Preview)](https://openjdk.org/jeps/397)

#### Java 15

* 339: [Edwards-Curve Digital Signature Algorithm (EdDSA)](https://openjdk.org/jeps/339)
* 360: [Sealed Classes (Preview)](https://openjdk.org/jeps/360)
* 371: [Hidden Classes](https://openjdk.org/jeps/371)
* 372: [Remove the Nashorn JavaScript Engine](https://openjdk.org/jeps/372)
* 373: [Reimplement the Legacy DatagramSocket API](https://openjdk.org/jeps/373)
* 374: [Disable and Deprecate Biased Locking](https://openjdk.org/jeps/374)
* 375: [Pattern Matching for instanceof (Second Preview)](https://openjdk.org/jeps/375)
* 377: [ZGC: A Scalable Low-Latency Garbage Collector](https://openjdk.org/jeps/377)
* 378: [Text Blocks](https://openjdk.org/jeps/378)
* 379: [Shenandoah: A Low-Pause-Time Garbage Collector](https://openjdk.org/jeps/379)
* 381: [Remove the Solaris and SPARC Ports](https://openjdk.org/jeps/381)
* 383: [Foreign-Memory Access API (Second Incubator)](https://openjdk.org/jeps/383)
* 384: [Records (Second Preview)](https://openjdk.org/jeps/384)
* 385: [Deprecate RMI Activation for Removal](https://openjdk.org/jeps/385)

#### Java 14

* 305: [Pattern Matching for instanceof (Preview)](https://openjdk.org/jeps/305)
* 343: [Packaging Tool (Incubator)](https://openjdk.org/jeps/343)
* 345: [NUMA-Aware Memory Allocation for G1](https://openjdk.org/jeps/345)
* 349: [JFR Event Streaming](https://openjdk.org/jeps/349)
* 352: [Non-Volatile Mapped Byte Buffers](https://openjdk.org/jeps/352)
* 358: [Helpful NullPointerExceptions](https://openjdk.org/jeps/358)
* 359: [Records (Preview)](https://openjdk.org/jeps/359)
* 361: [Switch Expressions (Standard)](https://openjdk.org/jeps/361)
* 362: [Deprecate the Solaris and SPARC Ports](https://openjdk.org/jeps/362)
* 363: [Remove the Concurrent Mark Sweep (CMS) Garbage Collector](https://openjdk.org/jeps/363)
* 364: [ZGC on macOS](https://openjdk.org/jeps/364)
* 365: [ZGC on Windows](https://openjdk.org/jeps/365)
* 366: [Deprecate the ParallelScavenge + SerialOld GC Combination](https://openjdk.org/jeps/366)
* 367: [Remove the Pack200 Tools and API](https://openjdk.org/jeps/367)
* 368: [Text Blocks (Second Preview)](https://openjdk.org/jeps/368)
* 370: [Foreign-Memory Access API (Incubator)](https://openjdk.org/jeps/370)

#### Java 13

* 350: [Dynamic CDS Archives](https://openjdk.org/jeps/350)
* 351: [ZGC: Uncommit Unused Memory](https://openjdk.org/jeps/351)
* 353: [Reimplement the Legacy Socket API](https://openjdk.org/jeps/353)
* 354: [Switch Expressions (Preview)](https://openjdk.org/jeps/354)
* 355: [Text Blocks (Preview)](https://openjdk.org/jeps/355)

#### Java 12

* 189: [Shenandoah: A Low-Pause-Time Garbage Collector (Experimental)](https://openjdk.org/jeps/189)
* 230: [Microbenchmark Suite](https://openjdk.org/jeps/230)
* 325: [Switch Expressions (Preview)](https://openjdk.org/jeps/325)
* 334: [JVM Constants API](https://openjdk.org/jeps/334)
* 340: [One AArch64 Port, Not Two](https://openjdk.org/jeps/340)
* 341: [Default CDS Archives](https://openjdk.org/jeps/341)
* 344: [Abortable Mixed Collections for G1](https://openjdk.org/jeps/344)
* 346: [Promptly Return Unused Committed Memory from G1](https://openjdk.org/jeps/346)

#### Java 11 (LTS)

* 181: [Nest-Based Access Control](https://openjdk.org/jeps/181)
* 309: [Dynamic Class-File Constants](https://openjdk.org/jeps/309)
* 315: [Improve Aarch64 Intrinsics](https://openjdk.org/jeps/315)
* 318: [Epsilon: A No-Op Garbage Collector](https://openjdk.org/jeps/318)
* 320: [Remove the Java EE and CORBA Modules](https://openjdk.org/jeps/320)
* 321: [HTTP Client (Standard)](https://openjdk.org/jeps/321)
* 323: [Local-Variable Syntax for Lambda Parameters](https://openjdk.org/jeps/323)
* 324: [Key Agreement with Curve25519 and Curve448](https://openjdk.org/jeps/324)
* 327: [Unicode 10](https://openjdk.org/jeps/327)
* 328: [Flight Recorder](https://openjdk.org/jeps/328)
* 329: [ChaCha20 and Poly1305 Cryptographic Algorithms](https://openjdk.org/jeps/329)
* 330: [Launch Single-File Source-Code Programs](https://openjdk.org/jeps/330)
* 331: [Low-Overhead Heap Profiling](https://openjdk.org/jeps/331)
* 332: [Transport Layer Security (TLS) 1.3](https://openjdk.org/jeps/332)
* 333: [ZGC: A Scalable Low-Latency Garbage Collector (Experimental)](https://openjdk.org/jeps/333)
* 335: [Deprecate the Nashorn JavaScript Engine](https://openjdk.org/jeps/335)
* 336: [Deprecate the Pack200 Tools and API](https://openjdk.org/jeps/336)

#### Java 10

* 286: [Local-Variable Type Inference](https://openjdk.org/jeps/286)
* 296: [Consolidate the JDK Forest into a Single Repository](https://openjdk.org/jeps/296)
* 304: [Garbage-Collector Interface](https://openjdk.org/jeps/304)
* 307: [Parallel Full GC for G1](https://openjdk.org/jeps/307)
* 310: [Application Class-Data Sharing](https://openjdk.org/jeps/310)
* 312: [Thread-Local Handshakes](https://openjdk.org/jeps/312)
* 313: [Remove the Native-Header Generation Tool (javah)](https://openjdk.org/jeps/313)
* 314: [Additional Unicode Language-Tag Extensions](https://openjdk.org/jeps/314)
* 316: [Heap Allocation on Alternative Memory Devices](https://openjdk.org/jeps/316)
* 317: [Experimental Java-Based JIT Compiler](https://openjdk.org/jeps/317)
* 319: [Root Certificates](https://openjdk.org/jeps/319)
* 322: [Time-Based Release Versioning](https://openjdk.org/jeps/322)

#### Java 9

* 102: [Process API Updates](https://openjdk.org/jeps/102)
* 110: [HTTP 2 Client](https://openjdk.org/jeps/110)
* 143: [Improve Contended Locking](https://openjdk.org/jeps/143)
* 158: [Unified JVM Logging](https://openjdk.org/jeps/158)
* 165: [Compiler Control](https://openjdk.org/jeps/165)
* 193: [Variable Handles](https://openjdk.org/jeps/193)
* 197: [Segmented Code Cache](https://openjdk.org/jeps/197)
* 199: [Smart Java Compilation, Phase Two](https://openjdk.org/jeps/199)
* 200: [The Modular JDK](https://openjdk.org/jeps/200)
* 201: [Modular Source Code](https://openjdk.org/jeps/201)
* 211: [Elide Deprecation Warnings on Import Statements](https://openjdk.org/jeps/211)
* 212: [Resolve Lint and Doclint Warnings](https://openjdk.org/jeps/212)
* 213: [Milling Project Coin](https://openjdk.org/jeps/213)
* 214: [Remove GC Combinations Deprecated in JDK 8](https://openjdk.org/jeps/214)
* 215: [Tiered Attribution for javac](https://openjdk.org/jeps/215)
* 216: [Process Import Statements Correctly](https://openjdk.org/jeps/216)
* 217: [Annotations Pipeline 2.0](https://openjdk.org/jeps/217)
* 219: [Datagram Transport Layer Security (DTLS)](https://openjdk.org/jeps/219)
* 220: [Modular Run-Time Images](https://openjdk.org/jeps/220)
* 221: [Simplified Doclet API](https://openjdk.org/jeps/221)
* 222: [jshell: The Java Shell (Read-Eval-Print Loop)](https://openjdk.org/jeps/222)
* 223: [New Version-String Scheme](https://openjdk.org/jeps/223)
* 224: [HTML5 Javadoc](https://openjdk.org/jeps/224)
* 225: [Javadoc Search](https://openjdk.org/jeps/225)
* 226: [UTF-8 Property Files](https://openjdk.org/jeps/226)
* 227: [Unicode 7.0](https://openjdk.org/jeps/227)
* 228: [Add More Diagnostic Commands](https://openjdk.org/jeps/228)
* 229: [Create PKCS12 Keystores by Default](https://openjdk.org/jeps/229)
* 231: [Remove Launch-Time JRE Version Selection](https://openjdk.org/jeps/231)
* 232: [Improve Secure Application Performance](https://openjdk.org/jeps/232)
* 233: [Generate Run-Time Compiler Tests Automatically](https://openjdk.org/jeps/233)
* 235: [Test Class-File Attributes Generated by javac](https://openjdk.org/jeps/235)
* 236: [Parser API for Nashorn](https://openjdk.org/jeps/236)
* 237: [Linux/AArch64 Port](https://openjdk.org/jeps/237)
* 238: [Multi-Release JAR Files](https://openjdk.org/jeps/238)
* 240: [Remove the JVM TI hprof Agent](https://openjdk.org/jeps/240)
* 241: [Remove the jhat Tool](https://openjdk.org/jeps/241)
* 243: [Java-Level JVM Compiler Interface](https://openjdk.org/jeps/243)
* 244: [TLS Application-Layer Protocol Negotiation Extension](https://openjdk.org/jeps/244)
* 245: [Validate JVM Command-Line Flag Arguments](https://openjdk.org/jeps/245)
* 246: [Leverage CPU Instructions for GHASH and RSA](https://openjdk.org/jeps/246)
* 247: [Compile for Older Platform Versions](https://openjdk.org/jeps/247)
* 248: [Make G1 the Default Garbage Collector](https://openjdk.org/jeps/248)
* 249: [OCSP Stapling for TLS](https://openjdk.org/jeps/249)
* 250: [Store Interned Strings in CDS Archives](https://openjdk.org/jeps/250)
* 251: [Multi-Resolution Images](https://openjdk.org/jeps/251)
* 252: [Use CLDR Locale Data by Default](https://openjdk.org/jeps/252)
* 253: [Prepare JavaFX UI Controls & CSS APIs for Modularization](https://openjdk.org/jeps/253)
* 254: [Compact Strings](https://openjdk.org/jeps/254)
* 255: [Merge Selected Xerces 2.11.0 Updates into JAXP](https://openjdk.org/jeps/255)
* 256: [BeanInfo Annotations](https://openjdk.org/jeps/256)
* 257: [Update JavaFX/Media to Newer Version of GStreamer](https://openjdk.org/jeps/257)
* 258: [HarfBuzz Font-Layout Engine](https://openjdk.org/jeps/258)
* 259: [Stack-Walking API](https://openjdk.org/jeps/259)
* 260: [Encapsulate Most Internal APIs](https://openjdk.org/jeps/260)
* 261: [Module System](https://openjdk.org/jeps/261)
* 262: [TIFF Image I/O](https://openjdk.org/jeps/262)
* 263: [HiDPI Graphics on Windows and Linux](https://openjdk.org/jeps/263)
* 264: [Platform Logging API and Service](https://openjdk.org/jeps/264)
* 265: [Marlin Graphics Renderer](https://openjdk.org/jeps/265)
* 266: [More Concurrency Updates](https://openjdk.org/jeps/266)
* 267: [Unicode 8.0](https://openjdk.org/jeps/267)
* 268: [XML Catalogs](https://openjdk.org/jeps/268)
* 269: [Convenience Factory Methods for Collections](https://openjdk.org/jeps/269)
* 270: [Reserved Stack Areas for Critical Sections](https://openjdk.org/jeps/270)
* 271: [Unified GC Logging](https://openjdk.org/jeps/271)
* 272: [Platform-Specific Desktop Features](https://openjdk.org/jeps/272)
* 273: [DRBG-Based SecureRandom Implementations](https://openjdk.org/jeps/273)
* 274: [Enhanced Method Handles](https://openjdk.org/jeps/274)
* 275: [Modular Java Application Packaging](https://openjdk.org/jeps/275)
* 276: [Dynamic Linking of Language-Defined Object Models](https://openjdk.org/jeps/276)
* 277: [Enhanced Deprecation](https://openjdk.org/jeps/277)
* 278: [Additional Tests for Humongous Objects in G1](https://openjdk.org/jeps/278)
* 279: [Improve Test-Failure Troubleshooting](https://openjdk.org/jeps/279)
* 280: [Indify String Concatenation](https://openjdk.org/jeps/280)
* 281: [HotSpot C++ Unit-Test Framework](https://openjdk.org/jeps/281)
* 282: [jlink: The Java Linker](https://openjdk.org/jeps/282)
* 283: [Enable GTK 3 on Linux](https://openjdk.org/jeps/283)
* 284: [New HotSpot Build System](https://openjdk.org/jeps/284)
* 285: [Spin-Wait Hints](https://openjdk.org/jeps/285)
* 287: [SHA-3 Hash Algorithms](https://openjdk.org/jeps/287)
* 288: [Disable SHA-1 Certificates](https://openjdk.org/jeps/288)
* 289: [Deprecate the Applet API](https://openjdk.org/jeps/289)
* 290: [Filter Incoming Serialization Data](https://openjdk.org/jeps/290)
* 291: [Deprecate the Concurrent Mark Sweep (CMS) Garbage Collector](https://openjdk.org/jeps/291)
* 292: [Implement Selected ECMAScript 6 Features in Nashorn](https://openjdk.org/jeps/292)
* 294: [Linux/s390x Port](https://openjdk.org/jeps/294)
* 295: [Ahead-of-Time Compilation](https://openjdk.org/jeps/295)
* 297: [Unified arm32/arm64 Port](https://openjdk.org/jeps/297)
* 298: [Remove Demos and Samples](https://openjdk.org/jeps/298)
* 299: [Reorganize Documentation](https://openjdk.org/jeps/299)

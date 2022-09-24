# WEEK024 - Java 8 之 Stream API 用法总结

Java 编程语言发展迅速，从 Java 9 开始，Java 采取了小步迭代的发布方式，以每 6 个月发布一个版本的速度在持续更新，[目前最新的版本已经升到 19 了](https://blogs.oracle.com/java/post/the-arrival-of-java-19)：

![](./images/java-versions.png)

尽管如此，据 [JRebel](https://www.jrebel.com/) 2022 年发布的 [Java 开发者生产力报告](https://www.jrebel.com/resources/java-developer-productivity-report-2022) 显示，Java 8 作为第一个 LTS 版本（另两个是 Java 11 和 17），仍然是使用最多的一个版本。

![](./images/java-version-usage.png)

Java 8 由 Oracle 公司于 2014 年 3 月 18 日发布，在这个版本中新增了大量的特性，首次引入了 Lambda 表达式和方法引用，开启了 Java 语言函数式编程的大门，其中新增的 Stream API（`java.util.stream`）特性更是将函数式编程发挥到了淋漓尽致。

## Stream API 概述

在 Java 8 之前，处理集合数据的常规方法是 `for` 循环：

```java
List<String> words = List.of("A", "B", "C");
for (String word: words) {
    System.out.println(word.toLowerCase());
}
```

或者使用 `iterator` 迭代器：

```java
List<String> words = List.of("A", "B", "C");
Iterator<String> iterator = words.iterator();
while (iterator.hasNext()) {
    System.out.println(iterator.next().toLowerCase());
}
```

这种集合的遍历方式被称为 `外部迭代`，也就是说由用户来决定 “做什么”（大写转小写） 和 “怎么做”（通过 `for` 或 `iterator` 遍历）。

而在 Java 8 中，新增的 Stream API 通过 `内部迭代` 来处理集合数据，使用了访问者设计模式（`Visitor Pattern`），用户只需要通过函数式的方法提供 “做什么” 即可，“怎么做” 交给 Stream API 内部实现：

```java
List<String> words = List.of("A", "B", "C");
words.stream().forEach(word -> System.out.println(word.toLowerCase()));
```

使用内部迭代可以让用户更聚焦待解决的问题，编写代码不易出错，而且通常编写的代码更少也更易读。这是 Stream API 的一大特征。

另外，正如 Stream API 的名字一样，Stream API 中有很多方法都会返回流对象本身，于是我们就可以将多个操作串联起来形成一个管道，写出下面这样流式风格（fluent style）的代码：

```java
List<String> names = students.stream()
    .filter(s -> s.getScore() >= 60)
    .sorted((x, y) -> x.getScore() - y.getScore())
    .map(Student::getName)
    .collect(Collectors.toList());
```

## Stream API 使用

### 流的创建

### 中间操作

### 结束操作

## 参考

1. [Java8 Stream的总结](https://juejin.cn/post/6844903565350141966)
1. [Java 8 新特性](https://www.runoob.com/java/java8-new-features.html)
1. https://www.runoob.com/java/java8-streams.html
1. https://www.baeldung.com/tag/java-streams/
1. https://www.cnblogs.com/wangzhuxing/p/10204894.html
1. https://www.cnblogs.com/yulinfeng/p/12561664.html

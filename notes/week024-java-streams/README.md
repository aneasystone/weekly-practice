# WEEK024 - Java 8 之 Stream API 用法总结

Java 编程语言发展迅速，从 Java 9 开始，Java 采取了小步迭代的发布方式，以每 6 个月发布一个版本的速度在持续更新，[目前最新的版本已经升到 19 了](https://blogs.oracle.com/java/post/the-arrival-of-java-19)：

![](./images/java-versions.png)

尽管如此，据 [JRebel](https://www.jrebel.com/) 2022 年发布的 [Java 开发者生产力报告](https://www.jrebel.com/resources/java-developer-productivity-report-2022) 显示，Java 8 作为第一个 LTS 版本（另两个是 Java 11 和 17），仍然是使用最多的一个版本。

![](./images/java-version-usage.png)

Java 8 由 Oracle 公司于 2014 年 3 月 18 日发布，在这个版本中新增了大量的特性，首次引入了 Lambda 表达式和方法引用，开启了 Java 语言函数式编程的大门，其中新增的 Stream API（`java.util.stream`）特性更是将函数式编程发挥到了淋漓尽致的地步。

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

而在 Java 8 中，新增的 Stream API 通过 `内部迭代` 来处理集合数据，使用了 [访问者设计模式（Visitor Pattern）](https://en.wikipedia.org/wiki/Visitor_pattern)，用户只需要通过函数式的方法提供 “做什么” 即可，“怎么做” 交给 Stream API 内部实现：

```java
List<String> words = List.of("A", "B", "C");
words.stream().forEach(word -> System.out.println(word.toLowerCase()));
```

使用内部迭代可以让用户更聚焦待解决的问题，编写代码不易出错，而且通常编写的代码更少也更易读。这是 Stream API 的一大特征。

另外，正如 Stream API 的名字一样，Stream API 中有很多方法都会返回流对象本身，于是我们就可以将多个操作串联起来形成一个管道（*pipeline*），写出下面这样流式风格（*fluent style*）的代码：

```java
List<String> names = students.stream()
    .filter(s -> s.getScore() >= 60)
    .sorted((x, y) -> x.getScore() - y.getScore())
    .map(Student::getName)
    .collect(Collectors.toList());
```

## Stream API 使用

### 流的创建

JDK 中提供了很多途径来创建一个流，这一节总结一些常用的创建流的方法。流有一个很重要的特性：**不会对数据源进行修改**，所以我们可以对同一个数据源创建多个流。

#### 创建一个空流

我们可以通过 `Stream.empty()` 创建一个不包含任何数据的空流：

```java
Stream<String> streamEmpty = Stream.empty();
```

在代码中使用空指针是一种不好的编程风格，空流的作用就是为了避免在程序中返回空指针：

```java
public Stream<String> streamOf(List<String> list) {
    return list == null || list.isEmpty() ? Stream.empty() : list.stream();
}
```

#### 从集合类创建流

JDK 中自带了大量的集合类，比如 `List`、`Set` 和 `Queue` 以及它们的子类，这些类都继承自 `Collection` 接口：

![](./images/jdk-collections.gif)

注意 `Map` 不是集合类，但是 `Map` 中的 `keySet()`、`values()` 和 `entrySet()` 方法返回的是集合类。

我们可以通过任何一个集合类的 `stream()` 方法创建一个流：

```java
List<String> collection = Arrays.asList("a", "b", "c");
Stream<String> streamOfCollection = collection.stream();
```

#### 从数组创建流

数组和集合类都是用于存储多个对象，只不过数组的长度固定，而集合的长度可变。我们可以使用 `Arrays.stream()` 静态方法从一个数组创建流：

```java
String[] array = new String[]{"a", "b", "c"};
Stream<String> streamOfArray = Arrays.stream(array);
```

也可以使用 `Stream.of()` 方法来创建：

```java
Stream<String> streamOfArray2 = Stream.of(array);
```

由于 `Stream.of()` 函数的入参定义是一个可变参数，本质上是个数组，所以既可以像上面那样传入一个数组，也可以直接传入数组元素创建：

```java
Stream<String> streamOfArray3 = Stream.of("a", "b", "c");
```

#### 使用 `Stream.builder()` 手工创建流

有时候流中的数据不是来自某个数据源，而是需要手工添加，我们可以使用 `Stream.builder()` 方法手工创建流：

```java
Stream<String> streamOfBuilder = Stream.<String>builder()
    .add("a")
    .add("b")
    .add("c")
    .build();
```

也可以往 builder 中依次添加：

```java
Stream.Builder<String> builder = Stream.<String>builder();
builder.add("a");
builder.add("b");
builder.add("c");
Stream<String> streamOfBuilder2 = builder.build();
```

#### 使用 `Stream.generate()` 生成流

`Stream.generate()` 方法也可以用于手工创建流，这个方法需要提供一个 `Supplier<T>` 的实现，生成的是一个无限流，一般通过 `limit` 来限定数量：

```java
Stream<String> streamOfGenerate = Stream.generate(() -> "hello").limit(3);
```

上面的例子中通过 Lambda 表达式 `() -> "hello"` 一直生成 `hello` 字符串。如果要生成不一样的数据，可以将变量传到 Lambda 表达式中，比如下面的例子生成 1 2 3 这样的连续整数：

```java
AtomicInteger num = new AtomicInteger(0);
Stream<Integer> streamOfGenerate2 = Stream.generate(() -> num.incrementAndGet()).limit(3);
```

#### 使用 `Stream.iterate()` 生成流

在上面的例子中，我们通过将变量传到 Lambda 表达式来生成一个整数数列，像这种根据迭代来生成数据的场景，还有一种更简单的实现：

```java
Stream<Integer> streamOfIterate = Stream.iterate(1, n -> n + 1).limit(3);
```

`iterate()` 函数第一个参数为流的第一个元素，后续的元素通过第二个参数中的 `UnaryOperator<T>` 来迭代生成。

#### 生成基础类型的流

由于 `Stream<T>` 接口使用了泛型，它的类型参数只能是对象类型，所以我们无法生成基础类型的流，我们只能使用相应的封装类型来生成流，这样就会导致自动装箱和拆箱（**auto-boxing**），影响性能。

于是 JDK 提供了几个特殊的接口来方便我们创建基础类型的流。JDK 一共有 8 个基础类型，包括 4 个整数类型（`byte`、`short`、`int`、`long`），2 个浮点类型（`float`、`double`），1 个字符型（`char`）和 1 个布尔型（`boolean`），不过只提供了 3 个基础类型的流：`IntStream`、`LongStream` 和 `DoubleStream`。

基础类型流和普通流接口基本一致，我们可以通过上面介绍的各种方法来创建基础类型流。JDK 还针对不同的基础类型提供了相应的更便捷的生成流的方法，比如 `IntStream.range()` 函数用于方便的生成某个范围内的整数序列：

```java
IntStream intStream = IntStream.range(1, 4);
```

要注意的是这个数列是左闭右开的，不包含第二个参数，`IntStream.rangeClosed()` 函数生成的数列是左右都是闭区间：

```java
IntStream intStream2 = IntStream.rangeClosed(1, 3);
```

此外，`Random` 类也提供了一些生成基础类型流的方法，比如下面的代码生成 3 个随机的 `int` 型整数：

```java
IntStream intStream = new Random().ints(3);
```

生成随机的 `long` 和 `double` 类型：

```java
LongStream longStream = new Random().longs(3);
DoubleStream doubleStream = new Random().doubles(3);
```

#### 使用 `String.chars()` 生成字符流

`String` 类提供了一个 `chars()` 方法，用于从字符串生成字符流，正如上面所说，JDK 只提供了 `IntStream`、`LongStream` 和 `DoubleStream` 三种基础类型流，并没有 `CharStream` 一说，所以返回值使用了 `IntStream`：

```java
IntStream charStream = "abc".chars();
```

#### 使用 `Pattern.splitAsStream()` 生成字符串流

我们知道，`String` 类里有一个 `split()` 方法可以将一个字符串分割成子串，但是返回值是一个数组，如果要生成一个子串流，可以使用正则表达式包中 `Pattern` 类的 `splitAsStream()` 方法：

```java
Stream<String> stringStream = Pattern.compile(", ").splitAsStream("a, b, c");
```

#### 从文件生成字符串流

另外，Java NIO 包中的 `Files` 类提供了一个 `lines()` 方法，它依次读取文件的每一行并生成字符串流：

```java
try (Stream<String> stringStream = Files.lines(Paths.get(filePath + "test.txt"));) {
    stringStream.forEach(System.out::println);
}
```

注意使用 `try-with-resources` 关闭文件。

### 中间操作

上一节主要介绍了一些常用的创建流的方法，流一旦创建好了，就可以对流执行各种操作。我们将对流的操作分成两种类型：**中间操作（Intermediate operation）** 和 **结束操作（Terminal operation）**，所有的中间操作返回的结果都是流本身，所以可以写出链式的代码，而结束操作会关闭流，让流无法再访问。

中间操作又可以分成 **无状态操作（Stateless operation）** 和 **有状态操作（Stateful operation）** 两种，无状态是指元素的处理不受前面元素的影响，而有状态是指必须等到所有元素处理之后才知道最终结果。

下面通过一些实例来演示不同操作的具体用法，首先创建一个流，包含一些学生数据：

```java
Stream<Student> students = Stream.of(
    Student.builder().name("张三").age(27).number(3L).interests("画画、篮球").build(),
    Student.builder().name("李四").age(29).number(2L).interests("篮球、足球").build(),
    Student.builder().name("王二").age(27).number(1L).interests("唱歌、跳舞、画画").build(),
    Student.builder().name("麻子").age(31).number(4L).interests("篮球、羽毛球").build()
);
```

#### 无状态操作

##### `filter`

`filter` 用于对数据流进行过滤，它接受一个 `Predicate<? super T> predicate` 参数，返回符合该 Predicate 条件的元素：

```java
students = students.filter(s -> s.getAge() > 30);
```

##### `map` / `mapToInt` / `mapToLong` / `mapToDouble`

`map` 接受一个 `Function<? super T, ? extends R> mapper` 类型的参数，对数据流的类型进行转换，从 T 类型转换为 R 类型，比如下面的代码将数据流 `Stream<Student>` 转换为 `Stream<StudentDTO>`：

```java
Stream<StudentDTO> studentDTOs = students.map(s -> {
    return StudentDTO.builder().name(s.getName()).age(s.getAge()).build();
});
```

如果要转换成基本类型流，可以使用 `mapToInt`、`mapToLong` 或 `mapToDouble` 方法：

```java
LongStream studentAges = students.mapToLong(s -> s.getAge());
```

上面的 Lambda 也可以写成方法引用：

```java
LongStream studentAges2 = students.mapToLong(Student::getAge);
```

##### `flatMap` / `flatMapToInt` / `flatMapToLong` / `flatMapToDouble`

`flatMap` 接受一个 `Function<? super T, ? extends Stream<? extends R>> mapper` 类型的参数，和 `map` 不同的是，他将 T 类型转换为 R 类型的流，而不是转换为 R 类型，然后再将流中所有数据平铺得到最后的结果：

```java
Stream<String> studentInterests = students.flatMap(s -> Arrays.stream(s.getInterests().split("、")));
```

每个学生可能有一个或多个兴趣，使用 `、` 分割，上面的代码首先将每个学生的兴趣拆开得到一个字符串流，然后将流中的元素平铺，最后得到汇总后的字符串流，该流中包含了所有学生的所有兴趣（元素可能重复）。可以看出 `flatMap` 实际上是对多个流的数据进行合并。

##### `peek`

`peek` 一般用来调试，它接受一个 `Consumer<? super T> action` 参数，可以在流的计算过程中对元素进行处理，无返回结果，比如打印出元素的状态：

```java
Stream<String> studentNames = students.filter(s -> s.getAge() > 20)
    .peek(System.out::println)
    .map(Student::getName)
    .peek(System.out::println);
```

##### `unordered`

*相遇顺序（encounter order）* 是流中的元素被处理时的顺序，创建流的数据源决定了流是否有序，比如 `List` 或数组是有序的，而 `HashSet` 是无序的。一些中间操作也可以修改流的相遇顺序，比如 `sorted()` 用于将无序流转换为有序，而 `unordered()` 也可以将一个有序流变成无序。

对于 *顺序流（sequential streams）*，相遇顺序并不会影响性能，只会影响确定性。如果一个流是有序的，每次执行都会得到相同的结果，如果一个流是无序的，则可能会得到不同的结果。

> 不过根据官方文档的说法，我使用 `unordered()` 将一个流改成无序流，重复执行得到的结果还是一样的 `[2, 4, 6]`，并没有得到不同的结果：
>
> ```
> List<Integer> ints = Stream.of(1, 2, 3).unordered()
>	.map(x -> x*2)
>	.collect(Collectors.toList());
> ```
> [网上有说法](https://segmentfault.com/q/1010000017969473) 认为，这是因为 `unordered()` 并不会打乱流原本的顺序，只会 **消除流必须保持有序的约束**，从而允许后续操作使用不必考虑排序的优化。

对于 *并行流（parallel streams）*，去掉有序约束后可能会提高流的执行效率，有些聚合操作，比如 `distinct()` 或 `Collectors.groupingBy()` 在不考虑元素有序时具备更好的性能。

#### 有状态操作

##### `distinct`

`distinct()` 方法用于去除流中的重复元素：

```java
Stream<Integer> intStream = Stream.of(1, 2, 3, 2, 4, 3, 1, 2);
intStream = intStream.distinct();
```

`distinct()` 是根据流中每个元素的 `equals()` 方法来去重的，所以如果流中是对象类型，可能需要重写其 `equals()` 方法。

##### `sorted`

`sorted()` 方法根据 *自然序（natural order）* 对流中的元素进行排序，流中的元素必须实现 `Comparable` 接口：

```java
Stream<Integer> intStream = Stream.of(1, 3, 2, 4);
intStream = intStream.sorted();
```

如果流中的元素没有实现 `Comparable` 接口，我们可以提供一个比较器 `Comparator<? super T> comparator` 对流进行排序：

```java
students = students.sorted(new Comparator<Student>() {

    @Override
    public int compare(Student o1, Student o2) {
        return o1.getAge().compareTo(o2.getAge());
    }
    
});
```

上面是通过匿名内部类的方式创建了一个比较器，我们可以使用 Lambda 来简化它的写法：

```java
students = students.sorted((o1, o2) -> o1.getAge().compareTo(o2.getAge()));
```

另外，`Comparator` 还内置了一些静态方法可以进一步简化代码：

```java
students = students.sorted(Comparator.comparing(Student::getAge));
```

甚至可以组合多个比较条件写出更复杂的排序逻辑：

```java
students = students.sorted(
    Comparator.comparing(Student::getAge).thenComparing(Student::getNumber)
);
```

##### `skip` / `limit`

`skip` 和 `limit` 这两个方法有点类似于 SQL 中的 `LIMIT offset, rows` 语句，用于返回指定的记录条数，最常见的一个用处是用来做分页查询。

```java
Stream<Integer> intStream = Stream.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
intStream = intStream.skip(3).limit(3);
```

##### `dropWhile` / `takeWhile`

`dropWhile` 和 `takeWhile` 这两个方法的作用也是返回指定的记录条数，只不过条数不是固定的，而是根据某个条件来决定返回哪些元素：

```java
Stream<Integer> intStream = Stream.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
intStream = intStream.dropWhile(x -> x <= 3).takeWhile(x -> x <= 6);
```

### 结束操作

流的中间操作其实只是一个标记，它是延迟执行的，要等到结束操作时才会触发实际的计算，而且每个流只能有一个结束操作。结束操作会关闭流，对已经关闭的流再执行操作会抛出 `IllegalStateException` 异常。

结束操作也可以分成两种类型：**短路操作（Short-Circuit operation）** 和 **非短路操作（Non-Short-Circuit operation）**，短路操作是指不用处理全部元素就可以返回结果，它必须一个元素处理一次，而非短路操作可以批量处理数据，但是需要等全部元素都处理完才会返回结果。

#### 短路操作

##### `anyMatch` / `allMatch` / `nonMatch`

这几个 match 方法非常类似，它们都接受一个 `Predicate<? super T> predicate` 条件，用于判断流中元素是否满足某个条件。

`anyMatch` 表示只要有一个元素满足条件即返回 `true`：

```java
boolean hasAgeGreaterThan30 = students.anyMatch(s -> s.getAge() > 30);
```

`allMatch` 表示所有元素都满足条件才返回 `true`：

```java
boolean allAgeGreaterThan20 = students.allMatch(s -> s.getAge() > 20);
```

`noneMatch` 表示所有元素都不满足条件才返回 `true`：

```java
boolean noAgeGreaterThan40 = students.noneMatch(s -> s.getAge() > 40);
```

##### `findFirst` / `findAny`

这两个 find 方法也是非常类似，都是从流中返回一个元素，如果没有，则返回一个空的 `Optional`，它们经常和 `filter` 方法联合使用。

`findFirst` 用于返回流中第一个元素：

```java
Optional<Student> student = students.filter(s -> s.getAge() > 28).findFirst();
```

而 `findAny()` 返回的元素是不确定的，如果是顺序流，返回的是第一个元素：

```java
// 返回的是 李四
Optional<Student> student = students.filter(s -> s.getAge() > 28).findAny();
```

如果是并行流，则返回值是随机的：

```java
// 返回不确定
Optional<Student> student = students.parallel().filter(s -> s.getAge() > 28).findAny();
```

#### 非短路操作

##### `forEach` / `forEachOrdered`

这两个 `forEach` 方法有点类似于 `peek` 方法，都是接受一个 `Consumer<? super T> action` 参数，对流中每一个元素进行处理，只不过 `forEach` 是结束操作，而 `peek` 是中间操作。

```java
intStream.forEach(System.out::println);
```

这两个方法的区别在于 `forEach` 的处理顺序是不确定的，而 `forEachOrdered` 会按照流中元素的 *相遇顺序（encounter order）* 来处理。比如下面的代码：

```java
intStream.parallel().forEach(System.out::println);
```

由于这里使用了并行流，`forEach` 输出结果是随机的。如果换成 `forEachOrdered`，则会保证输出结果是有序的：

```java
intStream.parallel().forEachOrdered(System.out::println);
```

##### `toArray`

`toArray` 方法用于将流转换为一个数组，默认情况下数组类型是 `Object[]`：

```java
Object[] array = students.toArray();
```

如果要转换为确切的对象类型，`toArray` 还接受一个 `IntFunction<A[]> generator` 参数，也是数组的构造函数：

```java
Student[] array = students.toArray(Student[]::new);
```

##### `reduce`
##### `collect`
##### `min` / `max` / `count`

## 参考

1. [Java8 Stream的总结](https://juejin.cn/post/6844903565350141966)
1. [Java 8 新特性](https://www.runoob.com/java/java8-new-features.html)
1. [Package java.util.stream Description](https://docs.oracle.com/javase/8/docs/api/java/util/stream/package-summary.html)
1. https://www.runoob.com/java/java8-streams.html
1. https://www.baeldung.com/java-streams
1. https://www.baeldung.com/tag/java-streams/
1. https://www.cnblogs.com/wangzhuxing/p/10204894.html
1. https://www.cnblogs.com/yulinfeng/p/12561664.html

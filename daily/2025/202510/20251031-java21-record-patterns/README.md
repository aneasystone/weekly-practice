# 重温 Java 21 之记录模式

**记录模式（Record Patterns）** 是对 **记录类（Records）** 这个特性的延伸，所以，我们先大致了解下什么是记录类，然后再来看看什么是记录模式。

## 什么是记录类（Records）？

记录类早在 Java 14 就已经引入了，它类似于 Tuple，提供了一种更简洁、更紧凑的方式来表示不可变数据，记录类经过三个版本的迭代（[JEP 359](https://openjdk.org/jeps/359)、[JEP 384](https://openjdk.org/jeps/384)、[JEP 395](https://openjdk.org/jeps/395)），最终在 Java 16 中发布了正式版本。

记录类的概念在其他编程语言中其实早已有之，比如 Kotlin 的 [Data class](https://kotlinlang.org/docs/data-classes.html) 或者 Scala 的 [Case class](https://docs.scala-lang.org/tour/case-classes.html)。它本质上依然是一个类，只不过使用关键字 `record` 来定义：

```java
record Point(int x, int y) { }
```

记录类的定义非常灵活，我们可以在单独文件中定义，也可以在类内部定义，甚至在函数内部定义。记录类的使用和普通类无异，使用 `new` 创建即可：

```java
Point p1 = new Point(10, 20);
System.out.println("x = " + p1.x());
System.out.println("y = " + p1.y());
System.out.println("p1 is " + p1.toString());
```

记录类具备如下特点：

* 它是一个 `final` 类；
* 它不能继承其他类，也不能继承其他记录类；
* 它的所有字段也是 `final` 的，所以一旦创建就不能修改；
* 它内置实现了构造函数，函数参数就是所有的字段；
* 它内置实现了所有字段的 `getter` 方法，没有 `setter` 方法；
* 它内置实现了 `equals()`、`hashCode()` 和 `toString()` 函数；

所以上面的示例和下面的 `Point` 类是等价的：

```java
public final class Point {
  final int x;
  final int y;

  public Point(int x, int y) {
    this.x = x;
    this.y = y;
  }

  public int x() {
    return x;
  }

  public int y() {
    return y;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    Point point = (Point) o;
    return x == point.x && y == point.y;
  }

  @Override
  public int hashCode() {
    return Objects.hash(x, y);
  }

  @Override
  public String toString() {
    return "Point{" +
        "x=" + x +
        ", y=" + y +
        '}';
  }
}
```

我们也可以在记录类中声明新的方法：

```java
record Point(int x, int y) {
    boolean isOrigin() {
        return x == 0 && y == 0;
    }
}
```

记录类的很多特性和 [Lombok](https://projectlombok.org/) 非常类似，比如下面通过 Lombok 的 `@Value` 注解创建一个不可变对象：

```java
@Value
public class Point {
  int x;
  int y;
}
```

不过记录类和 Lombok 还是有一些区别的：

* 根据 [JEP 395](https://openjdk.org/jeps/395) 的描述，记录类是作为不可变数据的透明载体，也就是说记录类无法隐藏字段；然而，Lombok 允许我们修改字段名称和访问级别；
* 记录类适合创建小型对象，当类中存在很多字段时，记录类会变得非常臃肿；使用 Lombok 的 `@Builder` 构建器模式可以写出更干净的代码；
* 记录类只能创建不可变对象，而 Lombok 的 `@Data` 可以创建可变对象；
* 记录类不支持继承，但是 Lombok 创建的类可以继承其他类或被其他类继承；

## 什么是记录模式（Record Patterns）？

相信很多人都写过类似下面这样的代码：

```java
if (obj instanceof Integer) {
  int intValue = ((Integer) obj).intValue();
  System.out.println(intValue);
}
```

这段代码实际上做了三件事：

* **Test**：测试 `obj` 的类型是否为 `Integer`；
* **Conversion**：将 `obj` 的类型转换为 `Integer`；
* **Destructuring**：从 `Integer` 类中提取出 `int` 值；

这三个步骤构成了一种通用的模式：测试并进行强制类型转换，这种模式被称为 [模式匹配（Pattern Matching）](https://openjdk.org/projects/amber/design-notes/patterns/pattern-matching-for-java)。虽然简单，但是却很繁琐。Java 16 在 [JEP 394](https://openjdk.org/jeps/394) 中正式发布了 **`instanceof` 模式匹配** 的特性，帮我们减少这种繁琐的条件状态提取：

```java
if (obj instanceof Integer intValue) {
  System.out.println(intValue);
}
```

这里的 `Integer intValue` 被称为 **类型模式（Type Patterns）**，其中 `Integer` 是匹配的断言，`intValue` 是匹配成功后的变量，这个变量可以直接使用，不需要再进行类型转换了。

匹配的断言也支持记录类：

```java
if (obj instanceof Point p) {
  int x = p.x();
  int y = p.y();
  System.out.println(x + y);
}
```

不过，这里虽然测试和转换代码得到了简化，但是从记录类中提取值仍然不是很方便，我们还可以进一步简化这段代码：

```java
if (obj instanceof Point(int x, int y)) {
  System.out.println(x + y);
}
```

这里的 `Point(int x, int y)` 就是 Java 21 中的 **记录模式（Record Patterns）**，可以说它是 `instanceof` 模式匹配的一个特例，专门用于从记录类中提取数据；记录模式也经过了三个版本的迭代：[JEP 405](https://openjdk.org/jeps/405)、[JEP 432](https://openjdk.org/jeps/432) 和 [JEP 440](https://openjdk.org/jeps/440)，现在终于在 Java 21 中发布了正式版本。

此外，记录模式还支持嵌套，我们可以在记录模式中嵌套另一个模式，假设有下面两个记录类：

```java
record Address(String province, String city) {}
record Person(String name, Integer age, Address address) {}
```

我们可以一次性提取出外部记录和内部记录的值：

```java
if (obj instanceof Person(String name, Integer age, Address(String province, String city))) {
  System.out.println("Name: " + name);
  System.out.println("Age: " + age);
  System.out.println("Address: " + province + " " + city);
}
```

仔细体会上面的代码，是不是非常优雅？

## `switch` 模式匹配

学习了记录模式，我们再来看看 Java 21 中的另一个特性，它和上面学习的 **`instanceof` 模式匹配** 息息相关。

除了 **`instanceof` 模式匹配**，其实还有另一种模式匹配叫做 **`switch` 模式匹配**，这个特性经历了 [JEP 406](https://openjdk.org/jeps/406)、[JEP 420](https://openjdk.org/jeps/420)、[JEP 427](https://openjdk.org/jeps/427)、[JEP 433](https://openjdk.org/jeps/433)  和 [JEP 441](https://openjdk.org/jeps/441) 五个版本的迭代，从 Java 17 开始首个预览版本到 Java 21 正式发布足足开发了 2 年时间。

在介绍这个功能之前，有一个前置知识点需要复习一下：在 Java 14 中发布了一个特性叫做 [Switch Expressions](https://openjdk.org/jeps/361)，这个特性允许我们在 `case` 中使用 Lambda 表达式来简化 `switch` 语句的写法：

```java
int result = switch (type) {
  case "child" -> 0;
  case "adult" -> 1;
  default -> -1;
};
System.out.println(result);
```

这种写法不仅省去了繁琐的 `break` 关键词，而且 `switch` 作为表达式可以直接赋值给一个变量。**`switch` 模式匹配** 则更进一步，允许我们在 `case` 语句中进行类型的测试和转换，下面是 `switch` 模式匹配的一个示例：

```java
String formatted = switch (obj) {
  case Integer i -> String.format("int %d", i);
  case Long l    -> String.format("long %d", l);
  case Double d  -> String.format("double %f", d);
  case String s  -> String.format("string %s", s);
  default        -> "unknown";
};
System.out.println(formatted);
```

作为对比，如果不使用 `switch` 模式匹配，我们只能写出下面这样的面条式代码：

```java
String formatted;
if (obj instanceof Integer i) {
  formatted = String.format("int %d", i);
} else if (obj instanceof Long l) {
  formatted = String.format("long %d", l);
} else if (obj instanceof Double d) {
  formatted = String.format("double %f", d);
} else if (obj instanceof String s) {
  formatted = String.format("string %s", s);
} else {
  formatted = "unknown";
}
System.out.println(formatted);
```

更多关于 `switch` 模式匹配的用法可以参考这篇文章：

* https://inside.java/2023/11/13/sip088/

## 小结

今天我们学习了 Java 21 中的 **记录模式** 和 **`switch` 模式匹配** 两个特性。

**记录模式（Record Patterns）** 建立在记录类和模式匹配的基础之上，进一步简化了代码的书写：

1. **记录类（Records）** 是一种轻量级的、不可变的数据载体，从 Java 16 开始正式发布，相比于 Lombok 更加原生，避免了注解编译时的额外处理，代码更加透明；
2. **模式匹配** 将类型测试、转换和值提取这三个繁琐的步骤统一起来，使得代码更加简洁。从 Java 16 开始支持 `instanceof` 模式匹配，允许在条件语句中直接进行类型的测试和转换；
3. **记录模式** 是 `instanceof` 模式匹配的特例，专门用于从记录类中提取数据，通过记录模式，我们可以一次性从记录对象中提取多个字段，使得代码更加直观易读；

而 **`switch` 模式匹配** 进一步扩展了模式匹配的应用场景，允许在 `switch` 表达式中进行类型的测试、转换和值的提取，相比于传统的 `if-else` 链式判断，代码结构更加清晰。

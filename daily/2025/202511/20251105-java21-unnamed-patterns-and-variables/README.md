# 重温 Java 21 之未命名模式和变量

未命名模式和变量也是一个预览特性，其主要目的是为了提高代码的可读性和可维护性。

在 Java 代码中，我们偶尔会遇到一些不需要使用的变量，比如下面这个例子中的异常 `e`：

```java
try { 
  int i = Integer.parseInt(s);
  System.out.println("Good number: " + i);
} catch (NumberFormatException e) { 
  System.out.println("Bad number: " + s);
}
```

这时我们就可以使用这个特性，使用下划线 `_` 来表示不需要使用的变量：

```java
try { 
  int i = Integer.parseInt(s);
  System.out.println("Good number: " + i);
} catch (NumberFormatException _) { 
  System.out.println("Bad number: " + s);
}
```

上面这个这被称为 **未命名变量（Unnamed Variables）**。

顾名思义，未命名模式和变量包含两个方面：**未命名模式（Unnamed Patterns）** 和 **未命名变量（Unnamed Variables）**。

## 未命名模式（Unnamed Patterns）

在上一篇笔记中，我们学习了什么是 **记录模式（Record Pattern）** 以及 `instanceof` 和 `switch` 两种模式匹配。未命名模式允许在模式匹配中省略掉记录组件的类型和名称。下面的代码展示了如何在 `instanceof` 模式匹配中使用未命名模式这个特性：

```java
if (obj instanceof Person(String name, _)) {
  System.out.println("Name: " + name);
}
```

其中 Person 记录的第二个参数 `Integer age` 在后续的代码中没用到，于是用下划线 `_` 把类型和名称都代替掉。我们也可以只代替 `age` 名称，这被称为 **未命名模式变量（Unnamed Pattern Variables）**：

```java
if (obj instanceof Person(String name, Integer _)) {
  System.out.println("Name: " + name);
}
```

这个特性也可以在 `switch` 模式匹配中使用：

```java
switch (b) {
  case Box(RedBall _), Box(BlueBall _) -> processBox(b);
  case Box(GreenBall _)                -> stopProcessing();
  case Box(_)                          -> pickAnotherBox();
}
```

这里前两个 `case` 是未命名模式变量，最后一个 `case` 是未命名模式。

## 未命名变量（Unnamed Variables）

未命名变量的使用场景更加丰富，除了上面在 `catch` 子句中使用的例子外，下面列举了一些其他的典型场景。

在 `for` 循环中使用：

```java
int acc = 0;
for (Order _ : orders) {
  if (acc < LIMIT) { 
    ... acc++ ...
  }
}
```

在赋值语句中使用：

```java
Queue<Integer> q = ... // x1, y1, z1, x2, y2, z2, ...
while (q.size() >= 3) {
  var x = q.remove();
  var y = q.remove();
  var _ = q.remove();
  ... new Point(x, y) ...
}
```

在 `try-with-resource` 语句中使用：

```java
try (var _ = ScopedContext.acquire()) {
  // No use of acquired resource
}
```

在 lambda 表达式中使用：

```java
stream.collect(
  Collectors.toMap(String::toUpperCase, _ -> "NODATA")
)
```

## 未命名类和实例 Main 方法（预览版本）

除了未命名模式和变量，Java 21 还引入了一个 **未命名类和实例 Main 方法** 预览特性。相信所有学过 Java 的人对下面这几行代码都非常熟悉吧：

```java
public class Hello {
  public static void main(String[] args) {
    System.out.println("Hello");
  }
}
```

通常我们初学 Java 的时候，都会写出类似这样的 Hello World 程序，不过作为初学者的入门示例，这段代码相比其他语言来说显得过于臃肿了，给初学者的感觉就是 Java 太复杂了，因为这里掺杂了太多只有在开发大型应用的时候才会涉及到的概念：

* 首先 `public class Hello` 这行代码涉及了类的声明和访问修饰符，这些概念可以用于数据隐藏、重用、访问控制、模块化等，在大型复杂应用程序中很有用；但是对于一个初学者，往往是从变量、控制流和子程序的基本编程概念开始学习的，在这个小例子中，它们毫无意义；
* 其次，`main()` 函数的 `String[] args` 这个参数主要用于接收从命令行传入的参数，但是对于一个初学者来说，在这里它显得非常神秘，因为它在代码中从未被使用过；
* 最后，`main()` 函数前面的 `static` 修饰符是 Java 类和对象模型的一部分，这个概念这对初学者也很不友好，甚至是有害的，因为如果要在代码中添加一个新的方法或字段时，为了访问它们，我们必须将它们全部声明成 `static` 的，这是一种既不常见也不是好习惯的用法，要么就要学习如何实例化对象。

为了让初学者可以快速上手，Java 21 引入了未命名类和实例 Main 方法这个特性，这个特性包含两个部分：

1. 增强了 Java 程序的 **启动协议（the launch protocol）**，使得 `main` 方法可以没有访问修饰符、没有 `static` 修饰符和没有 `String[]` 参数：

```java
class Hello { 
  void main() { 
    System.out.println("Hello");
  }
}
```

这样的 `main` 方法被称为 **实例 Main 方法（instance main methods）**。

2. 实现了 **未命名类（unnamed class）** 特性，使我们可以不用声明类，进一步简化上面的代码：

```java
void main() {
  System.out.println("Hello");
}
```

在 Java 语言中，每个类都位于一个包中，每个包都位于一个模块中。而一个未命名的类位于未命名的包中，未命名的包位于未命名的模块中。

## 小结

今天我们学习了 Java 21 中的 **未命名模式和变量** 以及 **未命名类和实例 Main 方法** 两个特性：

- **未命名模式和变量** 通过使用下划线 `_` 来表示那些不需要使用的模式变量和普通变量，消除了编译器对未使用变量的警告，使得代码意图更加明确；
- **未命名类和实例 Main 方法** 这个特性则着眼于降低 Java 的学习曲线，通过简化程序的启动协议，使得初学者可以无需掌握访问修饰符、`static` 修饰符、类的概念等高级特性，就能快速编写简单的 Java 程序；

这两个特性的引入虽然看似微不足道，但都体现了 Java 语言设计者的用心，他们在保持语言强大功能的同时，也在努力让 Java 变得更加易于上手。

# 重温 Java 21 之作用域值

**作用域值（Scoped Values）** 是 [Loom](https://wiki.openjdk.org/display/loom) 项目提出的另一个重要特性，它提供了一种隐式方法参数的形式，允许在大型程序的各个部分之间安全地共享数据，而无需将它们作为显式参数添加到调用链中的每个方法中。作用域值通常是作为一个公共静态字段，因此可以从任何方法中访问到。如果多个线程使用相同的作用域值，则从每个线程的角度来看，它可能包含不同的值。

如果您熟悉 **线程本地变量（thread-local variables）**，这听起来会很熟悉，事实上，作用域值正是为了解决使用线程本地变量时可能遇到的一些问题，在某些情况下可以将其作为线程本地变量的现代替代品。

## 一个例子

在 Web 应用开发中，一个经典的场景是获取当前已登录的用户信息，下面的代码模拟了大概的流程：

```java
public class UserDemo {
    
  public static void main(String[] args) {

    // 从 request 中获取用户信息
    String userId = getUserFromRequest();
    
    // 查询用户详情
    String userInfo = new UserService().getUserInfo(userId);
    System.out.println(userInfo);
  }

  private static String getUserFromRequest() {
    return "admin";
  }

  static class UserService {
    public String getUserInfo(String userId) {
      return new UserRepository().getUserInfo(userId);
    }
  }

  static class UserRepository {
    public String getUserInfo(String userId) {
      return String.format("%s:%s", userId, userId);
    }
  }
}
```

在接收到请求时，首先对用户进行身份验证，然后得到用户信息，这个信息可能被很多地方使用。在这里我们使用方法参数将用户信息传递到其他要使用的地方，可以看到，`userId` 参数从 `UserDemo` 传到 `UserService` 又传到 `UserRepository`。

在一个复杂的应用程序中，请求的处理可能会延伸到数百个方法，这时，我们需要为每一个方法添加 `userId` 参数，将用户传递到最底层需要用户信息的方法中。很显然，额外的 `userId` 参数会使我们的代码很快变得混乱，因为大多数方法不需要用户信息，甚至可能有一些方法出于安全原因根本不应该能够访问用户。如果在调用堆栈的某个深处我们还需要用户的 IP 地址怎么办？那么我们将不得不再添加一个 `ip` 参数，然后通过无数的方法传递它。

## 使用 `ThreadLocal` 线程本地变量

解决这一问题的传统方法是使用 `ThreadLocal`，它是线程本地变量，只要线程不销毁，我们随时可以获取 `ThreadLocal` 中的变量值。

```java
public class UserDemoThreadLocal {
    
  private final static ThreadLocal<String> USER = new ThreadLocal<>();
  
  public static void main(String[] args) {
    
    // 从 request 中获取用户信息
    String userId = getUserFromRequest();
    USER.set(userId);

    // 查询用户详情
    String userInfo = new UserService().getUserInfo();
    System.out.println(userInfo);
  }

  private static String getUserFromRequest() {
    return "admin";
  }

  static class UserService {
    public String getUserInfo() {
      return new UserRepository().getUserInfo();
    }
  }

  static class UserRepository {
    public String getUserInfo() {
      String userId = USER.get();
      return String.format("%s:%s", userId, userId);
    }
  }
}
```

这里我们定义了一个名为 `USER` 的 `ThreadLocal` 全局变量，获取完用户信息之后将其存入 `USER` 中，然后在 `UserRepository` 中直接从 `USER` 中获取。尽管看起来像普通变量，但线程本地变量的特点是每个线程都有一个独立实例，它的值取决于哪个线程调用其 `get` 或 `set` 方法来读取或写入其值。使用线程本地变量，可以方便地在调用堆栈上的方法之间共享数据，而无需使用方法参数。

> 注意，`ThreadLocal` 只能在单个线程中共享数据，如果内部方法中创建了新线程，我们可以使用 `InheritableThreadLocal`，它是 `ThreadLocal` 的子类，主要用于子线程创建时自动继承父线程的 `ThreadLocal` 变量，方便必要信息的进一步传递。

## 使用 `ScopedValue` 作用域值

不幸的是，线程本地变量存在许多设计缺陷，无法避免：

* **不受限制的可变性（Unconstrained mutability）** - 线程本地变量都是可变的，它的值可以随意被更改，任何能够调用线程本地变量的 `get` 方法的代码都可以随时调用该变量的 `set` 方法；但是往往更常见的需求是从一个方法向其他方法简单的单向数据传输，就像上面的示例一样；对线程本地变量的任意修改可能导致类似意大利面条的数据流以及难以察觉的错误；
* **无限寿命（Unbounded lifetime）** - 一旦线程本地变量通过 `set` 方法设值，这个值将在线程的整个生命周期中被保留，直到调用 `remove` 方法，不幸的是，开发人员经常忘记调用 `remove` 方法；如果使用了线程池，如果没有正确清除线程本地变量，可能会将一个线程的变量意外地泄漏到另一个不相关的线程中，导致潜在地安全漏洞；此外，忘记清理线程局部变量还可能导致内存泄露；
* **昂贵的继承（Expensive inheritance）** - 当使用大量线程时，我们通常会使用 `InheritableThreadLocal` 让子线程自动继承父线程的线程本地变量，子线程无法共享父线程使用的存储空间，这会显著增加程序的内存占用；特别是在虚拟线程推出之后，这个问题变得更为显著，因为虚拟线程足够廉价，程序中可能会创建成千上万的虚拟线程，如果一百万个虚拟线程中的每一个都有自己的线程局部变量副本，很快就会出现内存不足的问题。

**作用域值（Scoped Values）** 就是为解决这些问题而诞生的新概念。

* 首先，作用域值是不可变的，它的值无法更改，单向的数据传输使得代码流程更清晰；
* 另外，作用域值只在有限范围内使用，用完立即释放，不存在忘记清理的问题，所以也不会导致内存泄露；
* 最后，作用域值更轻量，由于它是不可变的，所以父线程和子线程可以复用一个实例，再多的虚拟线程也不会有内存不足的问题。

下面用 `ScopedValue` 对上面的代码进行重写：

```java
public class UserDemoScopedValue {
    
  final static ScopedValue<String> USER = ScopedValue.newInstance();

  public static void main(String[] args) {
    // 从 request 中获取用户信息
    String userId = getUserFromRequest();
    ScopedValue.where(USER, userId)
      .run(() -> {
        // 查询用户详情
        String userInfo = new UserService().getUserInfo();
        System.out.println(userInfo);
      });
  }

  private static String getUserFromRequest() {
    return "admin";
  }

  static class UserService {
    public String getUserInfo() {
      return new UserRepository().getUserInfo();
    }
  }

  static class UserRepository {
    public String getUserInfo() {
      String userId = USER.get();
      return String.format("%s:%s", userId, userId);
    }
  }
}
```

我们首先调用 `ScopedValue.where(USER, userId)`，它用于将作用域值和某个对象进行绑定，然后调用 `run()` 方法，它接受一个 lambda 表达式，从该表达式直接或间接调用的任何方法都可以通过 `get()` 方法读取作用域值。

作用域值仅在 `run()` 调用的生命周期内有效，在 `run()` 方法完成后，绑定将被销毁。这种有界的生命周期，使得数据从调用方传输到被调用方（直接和间接）的单向传输一目了然。

## 作用域值的重绑定

上面说过，作用域值是不可变的，没有任何方法可以更改作用域值，但是我们可以重新绑定作用域值：

```java
private static final ScopedValue<String> X = ScopedValue.newInstance();

void foo() {
  ScopedValue.where(X, "hello").run(() -> bar());
}

void bar() {
  System.out.println(X.get()); // prints hello
  ScopedValue.where(X, "goodbye").run(() -> baz());
  System.out.println(X.get()); // prints hello
}

void baz() {
  System.out.println(X.get()); // prints goodbye
}
```

在这个例子中，`foo()` 方法将作用域值 `X` 绑定为 `hello`，所以在 `bar()` 方法中使用 `X.get()` 获得的是 `hello`；但是接下来，我们重新将 `X` 绑定为 `goodbye`，再去调用 `baz()` 方法，这时在 `baz()` 方法中使用 `X.get()` 得到的就是 `goodbye` 了；不过值得注意的是，当 `baz()` 方法结束后，重新回到 `bar()` 方法，使用 `X.get()` 获得的仍然是 `hello`，说明作用域值并没有被修改。

## 作用域值的线程继承

在使用 `ThreadLocal` 的时候，我们通常会使用 `InheritableThreadLocal` 让子线程自动继承父线程的线程本地变量，那么作用域值如何实现线程继承呢？可惜的是，并不存在 `InheritableScopedValue` 这样的类，Java 21 提供了另一种解决方案：[结构化并发 API（JEP 428）](https://openjdk.org/jeps/428)。

`StructuredTaskScope` 是结构化并发中的核心类，它的使用方法如下：

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
  Supplier<String> user = scope.fork(() -> USER.get());
  scope.join().throwIfFailed();
  System.out.println("task scope: " + user.get());
} catch (Exception ex) {
}
```

其中 `scope.fork()` 方法用于创建子线程，父线程中的作用域值会自动被 `StructuredTaskScope` 创建的子线程继承，子线程中的代码可以使用父线程中为作用域值建立的绑定，而几乎没有额外开销。与线程局部变量不同，父线程的作用域值绑定不会被复制到子线程中，因此它的性能更高，也不会消耗过多的内存。

子线程的作用域值绑定的生命周期由 `StructuredTaskScope` 提供的 `fork/join` 模型控制，`scope.join()` 等待子线程结束，当线程结束后绑定就会自动销毁，避免了使用线程本地变量时出现无限生命周期的问题。

结构化并发也是 Java 21 中的一项重要特性，我们将在后面的笔记中继续学习它的知识。

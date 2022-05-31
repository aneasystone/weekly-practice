# 构建一个 Restful 的 Web 服务

这篇教程介绍了如何使用 Spring Boot 创建一个简单的 `Hello World` Restful Web 服务。

## 初始化项目

访问 [start.spring.io](https://start.spring.io/) 创建一个 demo 项目，依赖选择 Spring Web。下载 zip 文件，并解压，这样我们的项目框架就搭建好了。

## 创建 `Greeting` 类

当用户请求这个接口时，希望返回这样的 JSON 格式：

```
{
    "id": 1,
    "content": "Hello, World!"
}
```

所以我们需要创建一个简单的 `Greeting` 类，用来表示这个返回结果：

```
public class Greeting {
	
	private final long id;
	private final String content;

	public Greeting(long id, String content) {
		this.id = id;
		this.content = content;
	}

	public long getId() {
		return id;
	}

	public String getContent() {
		return content;
	}	
}
```

> Spring Web 内置了 [Jackson JSON](https://github.com/FasterXML/jackson) 的依赖，用于将 `Greeting` 类序列化为 JSON 字符串。

## 创建 `GreetingController` 类

在 Spring Web 框架中，HTTP 请求是通过控制器（`Controller`）来处理的。所以我们需要创建一个 `Controller` 类，来处理 `Hello World` 请求：

```
@RestController
public class GreetingController {
	
	private static final String template = "Hello, %s!";
	private final AtomicLong counter = new AtomicLong();

	@GetMapping("/greeting")
	public Greeting greeting(@RequestParam(value = "name", defaultValue = "World") String name) {
		return new Greeting(counter.incrementAndGet(), String.format(template, name));
	}
}
```

这里使用 `@RestController` 注解来表示控制器类；使用 `@GetMapping("/greeting")` 注解将来自 `/greeting` 的请求映射到 `greeting()` 方法；使用 `@RequestParam` 注解来定义接口的请求参数为 `name`，默认值为 `World`。

相比于传统的 MVC Controller，Restful Controller 有一个非常重要区别，那就是在 Restful Controller 中不需要依赖于某些视图技术（view technology）来做服务端的 HTML 渲染，而是直接返回一个 `Greeting` 对象，这个对象会被转换为 JSON 格式。这个也是 `@RestController` 注解的作用，相当于 `@Controller` + `@ResponseBody`。

由于 Spring Web 内置了 [Jackson JSON](https://github.com/FasterXML/jackson) 的依赖，所以会自动使用 `MappingJackson2HttpMessageConverter` 来将 Greeting 对象转换为 JSON。


# 使用 `RestTemplate` 调用 Restful Web 服务

在这篇教程中，我们将创建一个 Spring Boot 的命令行程序，并使用 `RestTemplate` 调用在之前的教程中 [构建的那个简单的 Restful Web 服务](../rest-service/README.md)。

## 初始化项目

访问 [start.spring.io](https://start.spring.io/) 创建一个 demo 项目，依赖继续选择 Web。下载 zip 文件，并解压，这样我们的项目框架就搭建好了。

## 创建 `Greeting` 类

Spring 提供了一个非常方便的类 `RestTemplate` 来调用 Restful Web 服务，我们只需要简单的一行代码就可以完成 HTTP 调用，并将返回结果转换为对象。首先我们需要定义和上一篇教程中一样的领域类：

```
public class Greeting {

	private long id;

	@JsonProperty(value = "content")
	private String greeting;

	// getters and setters
}
```

`RestTemplate` 默认使用 Jackson 将 HTTP 接口返回的内容反序列化为领域类，接口返回的字段必须和领域类中定义的字段一模一样，如果存在不一样的字段，可以使用 `@JsonProperty` 注解指定映射关系。

## 定义 `RestTemplate`

我们可以直接通过 `new RestTemplate()` 创建一个 `RestTemplate` 对象来使用，不过更好的做法是使用 `RestTemplateBuilder` 构建一个 Bean，不用每次都创建新的对象。通过 `RestTemplateBuilder` 可以对 `RestTemplate` 进行配置，比如：超时时间，消息转换器，拦截器等等。

```
@Bean
public RestTemplate restTemplate(RestTemplateBuilder builder) {
	return builder.build();
}
```

## 使用 `RestTemplate`

接着在代码中创建一个 `CommandLineRunner`，并将 `RestTemplate` 作为参数注入进来，然后使用 `RestTemplate` 的 `getForObject(String url, Class<T> responseType)` 方法请求 Restful 接口并将结果转换为 `Greeting` 对象：

```
@Bean
public CommandLineRunner run(RestTemplate restTemplate) throws Exception {
	return args -> {
		Greeting greeting = restTemplate.getForObject("http://localhost:8080/greeting", Greeting.class);
		log.info(greeting.toString());
	};
}
```

## 打包运行

```
$ mvn clean package
$ java -jar .\target\demo-0.0.1-SNAPSHOT.jar
...
2022-06-01 07:56:05.548  INFO 6824 --- [           main] com.example.demo.DemoApplication         : Greeting [greeting=Hello, World!, id=6]
```

不过这里有一点不如意的是，这个 demo 是一个 Web 项目，因为上面初始化项目时我们选择了 Web 依赖，生成的代码里自动引用了 `spring-boot-starter-web`。作为一个 `RestTemplate` 的 demo，完全不用这么重量级。我们打开 `pom.xml` 文件，将 `spring-boot-starter-web` 换成 `spring-boot-starter`，并添加 `spring-boot-starter-json` 和 `spring-web` 依赖即可：

```
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter</artifactId>
</dependency>
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-json</artifactId>
</dependency>
<dependency>
	<groupId>org.springframework</groupId>
	<artifactId>spring-web</artifactId>
</dependency>
```

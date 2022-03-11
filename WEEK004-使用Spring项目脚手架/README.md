# WEEK004 - 使用 Spring 项目脚手架

在我们的日常工作中，经常需要从头开始创建一个 Spring 项目，很多人的做法是，复制一份已有的项目，然后改目录名，改项目名，改包名，然后再把一些不要的文件删掉，只保留项目的基本框架。

实际上，这样操作后保留下来的基本框架代码就是 **脚手架** 代码，有很多的工具可以帮我们自动生成脚手架代码。

## Spring Initializr

创建 Spring 项目最简单的方式就是使用官方提供的 [Spring Initializr](https://start.spring.io/)，下图是使用 Spring Initializr 生成项目脚手架代码的一个示例：

![](./images/spring-initializr.png)

在这个页面中，我们需要填写这些信息：

* 项目类型
	* Maven
	* Gradle
* 语言类型
	* Java
	* Kotlin
	* Groovy
* Spring Boot 版本
* 项目基本信息
	* Group
	* Artifact
	* Name
	* Description
	* Package name
	* Packaging
	* Java
* 项目依赖

这里我选择的是 Maven 项目，语言类型为 Java，Spring Boot 版本为 2.6.4，项目基本信息为默认的 demo，打包方式为 jar，并添加了一个 Spring Web 依赖。生成的项目代码结构如下：

![](./images/demo-project-structure.png)

按照 [Spring Boot 快速入门教程](https://spring.io/quickstart)，我们在 `DemoApplication.java` 里加几行代码：

```
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class DemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}

	@GetMapping("/hello")
	public String hello(@RequestParam(value = "name", defaultValue = "World") String name) {
		return String.format("Hello %s!", name);
	}
}
```

至此一个简单的 Web 项目就完成了，然后执行 `./mvnw spring-boot:run` 命令，第一次执行可能比较慢，这是在下载程序所需要的依赖，等启动结束后打开浏览器，访问 `http://localhost:8080/hello` 页面，就可以看到我们熟悉的 `Hello World` 了。

## STS

https://spring.io/tools

https://docs.spring.io/initializr/docs/current-SNAPSHOT/reference/html/

https://github.com/spring-io/initializr

https://github.com/spring-io/start.spring.io

https://start.aliyun.com/

## Maven Archetype

https://maven.apache.org/guides/introduction/introduction-to-archetypes.html

## JHipster

https://www.jhipster.tech/

## 参考

1. [Spring Quickstart Guide](https://spring.io/quickstart)

## 更多

### 1. Spring Initializr 支持的依赖一览

* DEVELOPER TOOLS
	* Spring Native [Experimental]
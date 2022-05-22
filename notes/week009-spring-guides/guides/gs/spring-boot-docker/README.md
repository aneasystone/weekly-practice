# 在 Docker 环境中开发 Spring Boot 项目

这篇教程介绍了如何构建一个 Docker 镜像来运行 Spring Boot 应用，我们首先创建一个基础的 Dockerfile 文件，然后试着做一些调整，最后还会介绍使用 Maven 插件来代替 `docker` 命令构建镜像。

开始教程之前，确保你的机器上已经安装了 Docker。

## 使用 Spring Initializr 创建一个项目

访问 [start.spring.io](https://start.spring.io/)，创建一个 Spring Boot 项目，或者直接访问这个链接（[pre-initialized project](https://start.spring.io/#!type=maven-project&language=java&platformVersion=2.7.0&packaging=jar&jvmVersion=11&groupId=com.example&artifactId=demo&name=demo&description=Demo%20project%20for%20Spring%20Boot&packageName=com.example.demo&dependencies=web)），点击 Generate 按钮下载项目初始代码。

## 设置 Spring Boot 应用

刚创建的项目入口类如下所示：

```
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }

}
```

此时我们可以直接 `mvn package` 将代码打成 jar 包并运行，不过这个应用现在还看不到什么用处。所以我们决定为其加一个 Web 首页：

```
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class DemoApplication {

  @RequestMapping("/")
  public String home() {
    return "Hello Docker World";
  }

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }

}
```

我们在 `Application` 类中添加一个 `home()` 方法，通过 `@RestController` 和 `@RequestMapping("/")` 将这个方法设置成 Web 首页。

打包并运行：

```
$ mvn clean package && java -jar .\target\demo-0.0.1-SNAPSHOT.jar
```

访问首页：

```
$ curl http://localhost:8080
Hello Docker World
```

## 构建镜像

https://spring.io/guides/gs/spring-boot-docker/

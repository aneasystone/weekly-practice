# WEEK014 - Spring Boot 生产就绪特性 Actuator

Spring Boot 官网将 Actuator 称为 [生产就绪特性（Production-ready features）](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#actuator)，它提供了诸如健康检查、审计、指标收集、HTTP 跟踪等功能，帮助我们监控和管理 Spring Boot 应用。

## 快速开始

使用 [Spring Initializr](https://start.spring.io/) 创建一个项目，依赖项选择 Web 和 Actuator，或者在已有项目中添加依赖：

```
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

启动程序后，就能访问 `/actuator` 接口了：

```
$ curl -s http://localhost:8080/actuator | jq
{
  "_links": {
    "self": {
      "href": "http://localhost:8080/actuator",
      "templated": false
    },
    "health": {
      "href": "http://localhost:8080/actuator/health",
      "templated": false
    },
    "health-path": {
      "href": "http://localhost:8080/actuator/health/{*path}",
      "templated": true
    }
  }
}
```

## 参考

https://segmentfault.com/a/1190000021611510
https://kucw.github.io/blog/2020/7/spring-actuator/
http://www.ityouknow.com/springboot/2018/02/06/spring-boot-actuator.html

https://www.baeldung.com/spring-boot-actuators
https://spring.io/guides/gs/actuator-service/

https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#actuator
https://docs.spring.io/spring-boot/docs/current/actuator-api/htmlsingle/

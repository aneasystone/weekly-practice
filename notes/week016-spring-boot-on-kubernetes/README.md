# WEEK016 - 在 Kubernetes 环境中开发 Spring Boot 项目

在前面的教程中，我们学习了很多 Spring Boot 与 Docker 或 Kubernetes 的知识。比如在 [spring-boot-docker](../week009-spring-guides/guides/gs/spring-boot-docker/README.md) 中介绍了如何编写 Dockerfile 文件，以及如何构建一个 Docker 镜像来运行 Spring Boot 应用；在 [week011-spring-boot-on-docker](../week011-spring-boot-on-docker/README.md) 中更加深入的学习了构建镜像的知识以及如何优化我们的 Spring Boot 镜像；然后在 [spring-boot-kubernetes](../week009-spring-guides/guides/gs/spring-boot-kubernetes/README.md) 这篇教程中介绍了如何在 Kubernetes 环境下部署 Spring Boot 应用，不过教程的内容浅尝辄止，只能算作 Kubernetes 的简单入门。

在这篇教程中，我们将继续学习 Kubernetes 的知识，以及在 Kubernetes 环境下部署 Spring Boot 应用的最佳实践。

## 准备应用

通过 [start.spring.io](https://start.spring.io/) 生成项目代码，依赖选择 webflux 和 actuator。代码生成后，直接使用 Spring Boot Maven Plugin 构建镜像：

```
$ ./mvnw spring-boot:build-image -Dspring-boot.build-image.imageName=aneasystone/spring-boot-k8s
```

然后使用 `docker run` 运行：

```
$ docker run --name spring-boot-k8s -p 8080:8080 -t aneasystone/spring-boot-k8s
```

通过 `/actuator/health` 端点检查程序是否启动成功：

```
$ curl http://localhost:8080/actuator/health
{"status":"UP"}
```

## 将应用部署到 Kubernetes

## 最佳实践

## 使用 `ConfigMaps` 配置

## 服务发现和负载均衡

* WEEK010 - Kubernetes 安装小记
* WEEK013 - Kubernetes 使用小记

## 参考

* [【Topical Guides】Spring on Kubernetes](https://spring.io/guides/topicals/spring-on-kubernetes/)

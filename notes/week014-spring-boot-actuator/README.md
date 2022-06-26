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

Spring Boot Actuator 提供了很多有用的接口，被称为端点（`Endpoints`），访问 `/actuator` 就可以看出程序当前暴露了哪些端点。端点的访问路径可以通过下面的配置修改：

```
management.endpoints.web.base-path=/management
```

从上面的命令结果可以看出在最新版本中，Actuator 只暴露一个 `/health` 端点，这个端点提供了关于应用健康情况的一些基础信息。

如果要开启所有端点，可以打开配置文件 `application.properties`，添加如下配置项：

```
management.endpoints.web.exposure.include=*
```

现在看看暴露了哪些端点：

```
$ curl -s http://localhost:8080/actuator | jq
{
  "_links": {
    "self": {
      "href": "http://localhost:8080/actuator",
      "templated": false
    },
    "beans": {
      "href": "http://localhost:8080/actuator/beans",
      "templated": false
    },
    "caches-cache": {
      "href": "http://localhost:8080/actuator/caches/{cache}",
      "templated": true
    },
    "caches": {
      "href": "http://localhost:8080/actuator/caches",
      "templated": false
    },
    "health": {
      "href": "http://localhost:8080/actuator/health",
      "templated": false
    },
    "health-path": {
      "href": "http://localhost:8080/actuator/health/{*path}",
      "templated": true
    },
    "info": {
      "href": "http://localhost:8080/actuator/info",
      "templated": false
    },
    "conditions": {
      "href": "http://localhost:8080/actuator/conditions",
      "templated": false
    },
    "configprops": {
      "href": "http://localhost:8080/actuator/configprops",
      "templated": false
    },
    "configprops-prefix": {
      "href": "http://localhost:8080/actuator/configprops/{prefix}",
      "templated": true
    },
    "env": {
      "href": "http://localhost:8080/actuator/env",
      "templated": false
    },
    "env-toMatch": {
      "href": "http://localhost:8080/actuator/env/{toMatch}",
      "templated": true
    },
    "loggers": {
      "href": "http://localhost:8080/actuator/loggers",
      "templated": false
    },
    "loggers-name": {
      "href": "http://localhost:8080/actuator/loggers/{name}",
      "templated": true
    },
    "heapdump": {
      "href": "http://localhost:8080/actuator/heapdump",
      "templated": false
    },
    "threaddump": {
      "href": "http://localhost:8080/actuator/threaddump",
      "templated": false
    },
    "metrics-requiredMetricName": {
      "href": "http://localhost:8080/actuator/metrics/{requiredMetricName}",
      "templated": true
    },
    "metrics": {
      "href": "http://localhost:8080/actuator/metrics",
      "templated": false
    },
    "scheduledtasks": {
      "href": "http://localhost:8080/actuator/scheduledtasks",
      "templated": false
    },
    "mappings": {
      "href": "http://localhost:8080/actuator/mappings",
      "templated": false
    }
  }
}
```

其中 `*` 表示开启所有端点，也可以只开启部分端点：

```
management.endpoints.web.exposure.include=beans,health,info
```

或者选择性的关闭部分端点：

```
management.endpoints.web.exposure.exclude=beans,info
```

## 原生端点解析

Spring Boot Actuator 暴露的原生端点大概可以分成三大类：

* 应用配置类：获取应用程序中加载的应用配置、环境变量、自动化配置报告等与Spring Boot应用密切相关的配置类信息。
* 度量指标类：获取应用程序运行过程中用于监控的度量指标，比如：内存信息、线程池信息、HTTP请求统计等。
* 操作控制类：提供了对应用的关闭等操作类功能。

下面对 Actuator 暴露的原生端点依次体验和学习。

### Beans (beans)

端点 `/beans` 列出了应用程序中所有 Bean 的信息，包括 Bean 的名称、别名、类型、是否单例、依赖等等。

```
$ curl -s http://localhost:8080/actuator/beans | jq
{
  "contexts": {
    "application": {
      "beans": {
        "endpointCachingOperationInvokerAdvisor": {
          "aliases": [],
          "scope": "singleton",
          "type": "org.springframework.boot.actuate.endpoint.invoker.cache.CachingOperationInvokerAdvisor",
          "resource": "class path resource [org/springframework/boot/actuate/autoconfigure/endpoint/EndpointAutoConfiguration.class]",
          "dependencies": [
            "org.springframework.boot.actuate.autoconfigure.endpoint.EndpointAutoConfiguration",
            "environment"
          ]
        },
        "defaultServletHandlerMapping": {
          "aliases": [],
          "scope": "singleton",
          "type": "org.springframework.web.servlet.HandlerMapping",
          "resource": "class path resource [org/springframework/boot/autoconfigure/web/servlet/WebMvcAutoConfiguration$EnableWebMvcConfiguration.class]",
          "dependencies": [
            "org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration$EnableWebMvcConfiguration"
          ]
        },
        ...
      },
      "parentId": null
    }
  }
}
```

### Caches (caches)

### Health (health)

`/health` 端点用来检查应用程序的健康情况，默认情况下它只会显示应用程序的状态为 `UP` 或 `DOWN`：

```
$ curl -s http://localhost:8080/actuator/health | jq
{
  "status": "UP"
}
```

通过 `management.endpoint.health.show-details` 配置可以控制接口返回的内容：

| 配置值 | 描述 |
| ---- | ---- |
| never | 不展示详情信息，只显示 `UP` 或 `DOWN` 状态，默认配置 |
| always | 对所有用户展示详情信息 |
| when-authorized | 只对通过认证的用户展示详情信息，授权的角色可以通过`management.endpoint.health.roles` 配置 |

我们将其设置为 `always`：

```
management.endpoint.health.show-details=always
```

此时接口返回内容如下：

```
$ curl -s http://localhost:8080/actuator/health | jq
{
  "status": "UP",
  "components": {
    "diskSpace": {
      "status": "UP",
      "details": {
        "total": 174500155392,
        "free": 34697940992,
        "threshold": 10485760,
        "exists": true
      }
    },
    "ping": {
      "status": "UP"
    }
  }
}
```

由于我这个只是一个 Demo 项目，没有其他的依赖组件，所以健康状态的详情信息有点少。可以在 `pom.xml` 中添加一个 Mongo 的依赖：

```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-mongodb</artifactId>
</dependency>
```

此时再查看 `/health` 端点，详情里就多个 Mongo 的信息了：

```
$ curl -s http://localhost:8080/actuator/health | jq
{
  "status": "UP",
  "components": {
    "diskSpace": {
      "status": "UP",
      "details": {
        "total": 174500155392,
        "free": 34691891200,
        "threshold": 10485760,
        "exists": true
      }
    },
    "mongo": {
      "status": "UP",
      "details": {
        "version": "4.0.27"
      }
    },
    "ping": {
      "status": "UP"
    }
  }
}
```

我们将 Mongo 服务手工停掉，再访问 `/health` 端点，可以看出，尽管我们的服务还是运行着的，但是我们服务的健康状态已经是 `DOWN` 了：

```
$ curl -s http://localhost:8080/actuator/health | jq
{
  "status": "DOWN",
  "components": {
    "diskSpace": {
      "status": "UP",
      "details": {
        "total": 174500155392,
        "free": 34691891200,
        "threshold": 10485760,
        "exists": true
      }
    },
    "mongo": {
      "status": "DOWN",
      "details": {
        "error": "org.springframework.dao.DataAccessResourceFailureException: Timed out after 30000 ms while waiting to connect. Client view of cluster state is {type=UNKNOWN, servers=[{address=localhost:27017, type=UNKNOWN, state=CONNECTING, exception={com.mongodb.MongoSocketOpenException: Exception opening socket}, caused by {java.net.ConnectException: Connection refused: connect}}]; nested exception is com.mongodb.MongoTimeoutException: Timed out after 30000 ms while waiting to connect. Client view of cluster state is {type=UNKNOWN, servers=[{address=localhost:27017, type=UNKNOWN, state=CONNECTING, exception={com.mongodb.MongoSocketOpenException: Exception opening socket}, caused by {java.net.ConnectException: Connection refused: connect}}]"
      }
    },
    "ping": {
      "status": "UP"
    }
  }
}
```

#### 健康指示器（`HealthIndicator`）

Spring Boot Actuator 提供了很多自动配置的 `健康指示器（HealthIndicator）`，当你的项目依赖某个组件的时候，该组件对应的健康指示器就会被自动装配，继而采集对应的信息。比如上面我们添加 Mongo 依赖后，`MongoHealthIndicator` 就会自动被用来采集 Mongo 的信息。

每个健康指示器都有一个 `key`，默认是指示器的 Bean 名称去掉 `HealthIndicator` 后缀，比如 Mongo 的健康指示器就是 `mongo`。可以使用 `management.health.<key>.enabled` 配置关闭某个指示器。可以通过下面这个配置关闭 Mongo 的健康检查：

```
management.health.mongo.enabled=false
```

常见的健康指示器和对应的 key 如下：

| Key | HealthIndicator |
| --- | --------------- |
| cassandra | CassandraDriverHealthIndicator
| couchbase | CouchbaseHealthIndicator |
| db | DataSourceHealthIndicator |
| diskspace | DiskSpaceHealthIndicator |
| elasticsearch | ElasticsearchRestHealthIndicator |
| hazelcast | HazelcastHealthIndicator |
| influxdb | InfluxDbHealthIndicator |
| jms | JmsHealthIndicator |
| ldap | LdapHealthIndicator |
| mail | MailHealthIndicator |
| mongo | MongoHealthIndicator |
| neo4j | Neo4jHealthIndicator |
| ping | PingHealthIndicator |
| rabbit | RabbitHealthIndicator |
| redis | RedisHealthIndicator |
| solr | SolrHealthIndicator |

可以通过下面这个配置关闭上面列表中的所有健康检查：

```
management.health.defaults.enabled=false
```

为了适应 Kubernetes 环境，Spring Boot Actuator 还提供了下面两个健康指示器，默认关闭。分别对应 Kubernetes 里的 `Liveness` 和  `Readiness` 探针，[参考 Kubernetes 官方文档](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)。

| Key | HealthIndicator |
| --- | --------------- |
| livenessstate | LivenessStateHealthIndicator |
| readinessstate | ReadinessStateHealthIndicator |

#### 自定义健康指示器

当 Actuator 自带的健康指示器不能满足我们需求时，我们也可以自定义一个健康指示器，只需要实现 `HealthIndicator` 接口或者继承`AbstractHealthIndicator` 类即可，下面是一个简单的示例：

```
/**
 * 自定义健康指示器
 */
@Component
public class TestHealthIndicator extends AbstractHealthIndicator {

    @Override
    protected void doHealthCheck(Builder builder) throws Exception {
        builder.up()
            .withDetail("app", "test")
            .withDetail("error", 0);
    }

}
```

`withDetail` 用于显示健康详情，如果要显示状态 `DOWN`，就抛出一个异常即可。此时的健康详情接口返回如下：

```
$ curl -s http://localhost:8080/actuator/health | jq
{
  "status": "UP",
  "components": {
    "diskSpace": {
      "status": "UP",
      "details": {
        "total": 174500155392,
        "free": 34691883008,
        "threshold": 10485760,
        "exists": true
      }
    },
    "ping": {
      "status": "UP"
    },
    "test": {
      "status": "UP",
      "details": {
        "app": "test",
        "error": 0
      }
    }
  }
}
```

### Info (info)

### Conditions Evaluation Report (conditions)

### Configuration Properties (configprops)

### Environment (env)

### Loggers (loggers)

### Heap Dump (heapdump)

### Thread Dump (threaddump)

### Metrics (metrics)

### Scheduled Tasks (scheduledtasks)

### Mappings (mappings)

### Shutdown (shutdown)

## 其他端点

除了 Actuator 的原生端点，还有一些特殊的端点，需要在特定的条件下才会有。

### Audit Events (auditevents)

### Flyway (flyway)

### HTTP Trace (httptrace)

### Spring Integration graph (integrationgraph)

### Liquibase (liquibase)

### Log File (logfile)

### Prometheus (prometheus)

### Quartz (quartz)

### Sessions (sessions)

### Application Startup (startup)

## 参考

1. [Production-ready Features](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)
1. [Spring Boot Actuator Web API Documentation](https://docs.spring.io/spring-boot/docs/current/actuator-api/htmlsingle/)
1. [Spring Boot Actuator 模块 详解：健康检查，度量，指标收集和监控](https://ricstudio.top/archives/spring_boot_actuator_learn)
1. [SpringBoot - 監控工具 Actuator](https://kucw.github.io/blog/2020/7/spring-actuator/)
1. [Spring Boot (十九)：使用 Spring Boot Actuator 监控应用](http://www.ityouknow.com/springboot/2018/02/06/spring-boot-actuator.html)
1. [Spring Boot Actuator](https://www.baeldung.com/spring-boot-actuators)
1. [Building a RESTful Web Service with Spring Boot Actuator](https://spring.io/guides/gs/actuator-service/)


## 更多

### Beans 列表

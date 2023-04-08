# WEEK034 - 实战 APISIX 服务发现

在 [week030-apisix-notes](../week030-apisix-notes/README.md) 中，我们通过 APISIX 官方提供的入门示例学习了 APISIX 的基本概念，并使用 Admin API 和 Dashboard 两种方法创建路由。在创建路由时，我们必须明确地知道服务的 IP 和端口，这给运维人员带来了一定的负担，因为服务的重启或扩缩容都可能会导致服务的 IP 和端口发生变化，当服务数量非常多的时候，维护成本将急剧升高。

APISIX 集成了多种服务发现机制来解决这个问题，通过服务注册中心，APISIX 可以动态地获取服务的实例信息，这样我们就不用在路由中写死固定的 IP 和端口了。

如下图所示，一个标准的服务发现流程大致包含了三大部分：

![](./images/discovery-cn.png)

1. 服务启动时将自身的一些信息，比如服务名、IP、端口等信息上报到注册中心；各个服务与注册中心使用一定机制（例如心跳）通信，如果注册中心与服务长时间无法通信，就会注销该实例；当服务下线时，会删除注册中心的实例信息；
2. 网关会准实时地从注册中心获取服务实例信息；
3. 当用户通过网关请求服务时，网关从注册中心获取的实例列表中选择一个进行代理；

目前市面上流行着很多注册中心，比如 Eureka、Nacos、Consul 等，APISIX 内置了下面这些服务发现机制：

* [基于 Eureka 的服务发现](https://apisix.apache.org/zh/docs/apisix/discovery/)
* [基于 Nacos 的服务发现](https://apisix.apache.org/zh/docs/apisix/discovery/nacos/)
* [基于 Consul 的服务发现](https://apisix.apache.org/zh/docs/apisix/discovery/consul/)
* [基于 Consul KV 的服务发现](https://apisix.apache.org/zh/docs/apisix/discovery/consul_kv/)
* [基于 DNS 的服务发现](https://apisix.apache.org/zh/docs/apisix/discovery/dns/)
* [基于 APISIX-Seed 架构的控制面服务发现](https://apisix.apache.org/zh/docs/apisix/discovery/control-plane-service-discovery/)
* [基于 Kubernetes 的服务发现](https://apisix.apache.org/zh/docs/apisix/discovery/kubernetes/)

## 基于 Eureka 的服务发现

[Eureka](https://spring.io/projects/spring-cloud-netflix) 是 Netflix 开源的一款注册中心服务，它也被称为 Spring Cloud Netflix，是 Spring Cloud 全家桶中的核心成员。本节将演示如何让 APISIX 通过 Eureka 来实现服务发现，动态地获取下游服务信息。

### 启动 Eureka Server

我们可以直接运行官方的示例代码 [spring-cloud-samples/eureka](https://github.com/spring-cloud-samples/eureka) 来启动一个 Eureka Server：

```
$ git clone https://github.com/spring-cloud-samples/eureka.git
$ cd eureka && ./gradlew bootRun
```

或者也可以直接使用官方制作好的镜像：

```
$ docker run -d -p 8761:8761 springcloud/eureka
```

启动之后访问 http://localhost:8761/ 看看 Eureka Server 是否已正常运行。

### 启动 Eureka Client

如果一切顺利，我们再准备一个简单的 Spring Boot 客户端程序，引入 `spring-cloud-starter-netflix-eureka-client` 依赖，再通过 `@EnableEurekaClient` 注解将服务信息注册到 Eureka Server：

```
@EnableEurekaClient
@SpringBootApplication
@RestController
public class EurekaApplication {

	public static void main(String[] args) {
		SpringApplication.run(EurekaApplication.class, args);
	}

	@RequestMapping("/")
	public String home() {
		return String.format("Hello, I'm eureka client.");
	}
}
```

在配置文件中设置服务名称和服务端口：

```
spring.application.name=eureka-client
server.port=8081
```

默认注册的 Eureka Server 地址是 `http://localhost:8761/eureka/`，可以通过下面的参数修改：

```
eureka.client.serviceUrl.defaultZone=http://localhost:8761/eureka/
```

默认情况下，Eureka Client 是将该服务所在的主机名注册到 Eureka Server，这在某些情况下可能会导致其他服务调不通该服务，我们可以通过下面的参数，让 Eureka Client 注册 IP 地址：

```
eureka.instance.prefer-ip-address=true
eureka.instance.ip-address=192.168.1.40
```

启动后，在 Eureka 页面的实例中可以看到我们注册的服务：

![](./images/eureka-instances.png)

### APISIX 集成 Eureka 服务发现

接下来，我们要让 APISIX 通过 Eureka Server 找到我们的服务。首先，在 APISIX 的配置文件 `config.yaml` 中添加如下内容：

```
discovery:
  eureka:
    host:
      - "http://192.168.1.40:8761"
    prefix: /eureka/
```

然后重启 APISIX，接着向 APISIX 中添加如下路由：

```
$ curl -X PUT http://127.0.0.1:9180/apisix/admin/routes/11 \
    -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -i -d '
{
    "methods": ["GET"],
    "uri": "/eureka",
    "plugins": {
        "proxy-rewrite" : {
            "regex_uri": ["/eureka", "/"]
        }
    },
    "upstream": {
        "type": "roundrobin",
        "discovery_type": "eureka",
		"service_name": "EUREKA-CLIENT"
    }
}'
```

之前创建路由时，我们在 `upstream` 中通过 `nodes` 参数表示上游服务器节点，这里我们不再需要写死服务器节点信息，而是通过 `"discovery_type": "eureka"` 和 `"service_name": "EUREKA-CLIENT"` 来让 APISIX 使用 `eureka` 服务发现机制，上游的服务名称为 `EUREKA-CLIENT`。

值得注意的是，虽然上面的 Eureka Client 的 `spring.application.name` 是小写，但是注册到 Eureka Server 的服务名称是大写，所以这里的 `service_name` 参数必须是大写。此外，这里我们还使用了 `proxy-rewrite` 插件，它相当于 Nginx 中的路径重写功能，当多个上游服务的接口地址相同时，通过路径重写可以将它们区分开来。

访问 APISIX 的 `/eureka` 地址验证一下：

```
$ curl http://127.0.0.1:9080/eureka
Hello, I'm eureka client.
```

我们成功通过 APISIX 访问到了我们的服务。

关于 APISIX 集成 Eureka 的更多信息，可以参考官方文档 [集成服务发现注册中心](https://apisix.apache.org/zh/docs/apisix/discovery/) 和官方博客 [API 网关 Apache APISIX 集成 Eureka 作为服务发现](https://www.apiseven.com/blog/apigateway-integration-eureka-service-discovery)。

## 基于 Nacos 的服务发现

[Nacos](https://nacos.io/zh-cn/index.html) 是阿里开源的一款集服务发现、配置管理和服务管理于一体的管理平台，APISIX 同样支持 Nacos 的服务发现机制。

### 启动 Nacos Server

首先，我们需要准备一个 Nacos Server，Nacos 官网提供了多种部署方式，可以 [通过源码或安装包安装](https://nacos.io/zh-cn/docs/v2/quickstart/quick-start.html)、[通过 Docker 安装](https://nacos.io/zh-cn/docs/v2/quickstart/quick-start-docker.html) 或 [通过 Kubernetes 安装](https://nacos.io/zh-cn/docs/v2/quickstart/quick-start-kubernetes.html)，我们这里直接使用 docker 命令启动一个本地模式的 Nacos Server：

```
$ docker run -e MODE=standalone -p 8848:8848 -p 9848:9848 -d nacos/nacos-server:v2.2.0
```

> 不知道为什么，有时候启动会报这样的错误：`com.alibaba.nacos.api.exception.runtime.NacosRuntimeException: errCode: 500, errMsg: load derby-schema.sql error`，多启动几次又可以了。

启动成功后，访问 http://localhost:8848/nacos/ 进入 Nacos 管理页面，默认用户名和密码为 `nacos/nacos`：

![](./images/nacos-home.png)

### 启动 Nacos Client

接下来，我们再准备一个简单的 Spring Boot 客户端程序，引入 `nacos-discovery-spring-boot-starter` 依赖，并通过它提供的 NameService 将服务信息注册到 Nacos Server：

```
@SpringBootApplication
@RestController
public class NacosApplication implements CommandLineRunner {

    @Value("${spring.application.name}")
    private String applicationName;

    @Value("${server.port}")
    private Integer serverPort;
	
	@NacosInjected
    private NamingService namingService;
	
	public static void main(String[] args) {
		SpringApplication.run(NacosApplication.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        namingService.registerInstance(applicationName, "192.168.1.40", serverPort);
    }

	@RequestMapping("/")
	public String home() {
		return String.format("Hello, I'm nacos client.");
	}
}
```

在配置文件中设置服务名称和服务端口：

```
spring.application.name=nacos-client
server.port=8082
```

以及 Nacos Server 的地址：

```
nacos.discovery.server-addr=127.0.0.1:8848
```

启动后，在 Nacos 的服务管理页面中就可以看到我们注册的服务了：

![](./images/nacos-service-management.png)

### APISIX 集成 Nacos 服务发现

接下来，我们要让 APISIX 通过 Nacos Server 找到我们的服务。首先，在 APISIX 的配置文件 `config.yaml` 中添加如下内容：

```
discovery:
  nacos:
    host:
      - "http://192.168.1.40:8848"
    prefix: "/nacos/v1/"
```

然后重启 APISIX，接着向 APISIX 中添加如下路由：

```
$ curl -X PUT http://127.0.0.1:9180/apisix/admin/routes/22 \
    -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -i -d '
{
    "methods": ["GET"],
    "uri": "/nacos",
    "plugins": {
        "proxy-rewrite" : {
            "regex_uri": ["/nacos", "/"]
        }
    },
    "upstream": {
        "type": "roundrobin",
        "discovery_type": "nacos",
		"service_name": "nacos-client"
    }
}'
```

和上面 Eureka 服务发现的例子一样，我们也使用 `proxy-rewrite` 插件实现了路径重写功能，访问 APISIX 的 `/nacos` 地址验证一下：

```
$ curl http://127.0.0.1:9080/nacos
Hello, I'm nacos client.
```

我们成功通过 APISIX 访问到了我们的服务。

关于 APISIX 集成 Nacos 的更多信息，可以参考官方文档 [基于 Nacos 的服务发现](https://apisix.apache.org/zh/docs/apisix/discovery/nacos/) 和官方博客 [Nacos 在 API 网关中的服务发现实践](https://www.apiseven.com/blog/nacos-api-gateway)。

## 基于 Consul 的服务发现

[Consul](https://www.consul.io/) 是由 HashiCorp 开源的一套分布式系统的解决方案，同时也可以作为一套服务网格解决方案，提供了丰富的控制平面功能，包括：服务发现、健康检查、键值存储、安全服务通信、多数据中心等。

### 启动 Consul Server

Consul 使用 Go 语言编写，安装和部署都非常简单，官方提供了 Consul 的多种安装方式，包括 [二进制安装](https://learn.hashicorp.com/collections/consul/get-started-vms)、[Kubernetes 安装](https://learn.hashicorp.com/tutorials/consul/kubernetes-deployment-guide) 或 [HCP 安装](https://developer.hashicorp.com/consul/tutorials/get-started-hcp/hcp-gs-deploy)。这里我们使用最简单的二进制安装方式，这种方式只需要执行一个可执行文件即可，首先，我们从 [Install Consul](https://developer.hashicorp.com/consul/downloads) 页面找到对应操作系统的安装包并下载：

```
$ curl -LO https://releases.hashicorp.com/consul/1.15.1/consul_1.15.1_linux_amd64.zip
$ unzip consul_1.15.1_linux_amd64.zip
```

下载并解压之后，Consul 就算安装成功了，使用 `consul version` 命令进行验证：

```
$ ./consul version
Consul v1.15.1
Revision 7c04b6a0
Build Date 2023-03-07T20:35:33Z
Protocol 2 spoken by default, understands 2 to 3 (agent will automatically use protocol >2 when speaking to compatible agents)
```

Consul 安装完成后，就可以启动 Consul Agent 了，Consul Agent 有 `-server` 和 `-client` 两种模式，`-client` 一般用于服务网格等场景，这里我们通过 `-server` 模式启动：

```
$ ./consul agent -server -ui -bootstrap-expect=1 -node=agent-one -bind=127.0.0.1 -client=0.0.0.0 -data-dir=./data_dir
==> Starting Consul agent...
              Version: '1.15.1'
           Build Date: '2023-03-07 20:35:33 +0000 UTC'
              Node ID: '8c1ccd5a-69b3-4c95-34c1-f915c19a3d08'
            Node name: 'agent-one'
           Datacenter: 'dc1' (Segment: '<all>')
               Server: true (Bootstrap: true)
          Client Addr: [0.0.0.0] (HTTP: 8500, HTTPS: -1, gRPC: -1, gRPC-TLS: 8503, DNS: 8600)
         Cluster Addr: 127.0.0.1 (LAN: 8301, WAN: 8302)
    Gossip Encryption: false
     Auto-Encrypt-TLS: false
            HTTPS TLS: Verify Incoming: false, Verify Outgoing: false, Min Version: TLSv1_2
             gRPC TLS: Verify Incoming: false, Min Version: TLSv1_2
     Internal RPC TLS: Verify Incoming: false, Verify Outgoing: false (Verify Hostname: false), Min Version: TLSv1_2

==> Log data will now stream in as it occurs:
```

其中 `-ui` 表示开启内置的 Web UI 管理界面，`-bootstrap-expect=1` 表示服务器希望以 bootstrap 模式启动，`-node=agent-one` 用于指定节点名称，`-bind=127.0.0.1` 这个地址用于 Consul 集群内通信，`-client=0.0.0.0` 这个地址用于 Consul 和客户端之间的通信，包括 HTTP 和 DNS 两种通信方式，`-data-dir` 参数用于设置数据目录。关于 `consul agent` 更多的命令行参数，可以参考 [Agents Overview](https://developer.hashicorp.com/consul/docs/agent) 和 [Agents Command-line Reference](https://developer.hashicorp.com/consul/docs/agent/config/cli-flags)。

> 
> 简单起见，我们也可以使用 `-dev` 参数以开发模式启动 Consul Agent：
> ```
> $ ./consul agent -dev
> ```
> 

如果 Consul Agent 启动成功，访问 http://localhost:8500/ 进入 Consul 的管理页面，在服务列表可以看到 consul 这个服务：

![](./images/consul-services.png)

在节点列表可以看到 agent-one 这个节点：

![](./images/consul-nodes.png)

### 启动 Consul Client

让我们继续编写 Consul Client 程序，引入 `spring-cloud-starter-consul-discovery` 依赖，并通过 `@EnableDiscoveryClient` 注解将服务信息注册到 Consul Server：

```
@EnableDiscoveryClient
@SpringBootApplication
@RestController
public class ConsulApplication {
	
	public static void main(String[] args) {
		SpringApplication.run(ConsulApplication.class, args);
	}

	@RequestMapping("/")
	public String home() {
		return String.format("Hello, I'm consul client.");
	}
}
```

可以看到和 Eureka Client 的代码几乎是完全一样的，不过有一点要注意，我们还需要在 pom.xml 文件中引入 `spring-boot-starter-actuator` 依赖，开启 Actuator 端点，因为 Consul 默认是通过 `/actuator/health` 接口来对程序做健康检查的。

在配置文件中设置服务名称和服务端口：

```
spring.application.name=consul-client
server.port=8083
```

以及 Consul 相关的配置：

```
spring.cloud.consul.host=127.0.0.1
spring.cloud.consul.port=8500
spring.cloud.consul.discovery.service-name=${spring.application.name}
spring.cloud.consul.discovery.prefer-ip-address=true
spring.cloud.consul.discovery.ip-address=192.168.1.40
```

启动后，在 Consul 的服务管理页面中就可以看到我们注册的服务了：

![](./images/consul-service-detail.png)

### APISIX 集成 Consul 服务发现

接下来，我们要让 APISIX 通过 Consul Server 找到我们的服务。首先，在 APISIX 的配置文件 `config.yaml` 中添加如下内容：

```
discovery:
  consul:
    servers:
      - "http://192.168.1.40:8500"
```

然后重启 APISIX，接着向 APISIX 中添加如下路由：

```
$ curl -X PUT http://127.0.0.1:9180/apisix/admin/routes/33 \
    -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -i -d '
{
    "methods": ["GET"],
    "uri": "/consul",
    "plugins": {
        "proxy-rewrite" : {
            "regex_uri": ["/consul", "/"]
        }
    },
    "upstream": {
        "type": "roundrobin",
        "discovery_type": "consul",
		"service_name": "consul-client"
    }
}'
```

访问 APISIX 的 `/consul` 地址验证一下：

```
$ curl http://127.0.0.1:9080/consul
Hello, I'm consul client.
```

关于 APISIX 集成 Consul 的更多信息，可以参考官方文档 [基于 Consul 的服务发现](https://apisix.apache.org/zh/docs/apisix/discovery/consul/)。

### 基于 Consul KV 的服务发现

Consul 还提供了分布式键值数据库的功能，这个功能和 Etcd、ZooKeeper 类似，主要用于存储配置参数和元数据。基于 Consul KV 我们也可以实现服务发现的功能。

首先准备 consul-kv-client 客户端程序，它的地址为 `192.168.1.40:8084`，我们通过 Consul KV 的 HTTP API 手工注册服务：

```
$ curl -X PUT http://127.0.0.1:8500/v1/kv/upstreams/consul-kv-client/192.168.1.40:8084 -d ' {"weight": 1, "max_fails": 2, "fail_timeout": 1}'
```

其中，`/v1/kv/` 后的路径按照 `{Prefix}/{Service Name}/{IP}:{Port}` 的格式构成。可以在 Consul 的 Key/Value 管理页面看到我们注册的服务：

![](./images/consul-key-value.png)

然后在 APISIX 的配置文件 `config.yaml` 中添加如下内容：

```
discovery:
  consul_kv:
    servers:
      - "http://192.168.1.40:8500"
    prefix: "upstreams"
```

然后重启 APISIX，接着向 APISIX 中添加如下路由：

```
$ curl -X PUT http://127.0.0.1:9180/apisix/admin/routes/44 \
    -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -i -d '
{
    "methods": ["GET"],
    "uri": "/consul_kv",
    "plugins": {
        "proxy-rewrite" : {
            "regex_uri": ["/consul_kv", "/"]
        }
    },
    "upstream": {
        "type": "roundrobin",
        "discovery_type": "consul_kv",
		"service_name": "http://192.168.1.40:8500/v1/kv/upstreams/consul-kv-client/"
    }
}'
```

注意这里的 `service_name` 参数需要设置为 KV 的 URL 路径，访问 APISIX 的 `/consul_kv` 地址验证一下：

```
$ curl http://127.0.0.1:9080/consul_kv
Hello, I'm consul_kv client.
```

另一点需要注意的是，这种方式注册的服务没有健康检查机制，服务退出后需要手工删除对应的 KV：

```
$ curl -X DELETE http://127.0.0.1:8500/v1/kv/upstreams/consul-kv-client/192.168.1.40:8084
```

关于 APISIX 集成 Consul KV 的更多信息，可以参考官方文档 [基于 Consul KV 的服务发现](https://apisix.apache.org/zh/docs/apisix/discovery/consul_kv/) 和官方博客 [Apache APISIX 集成 Consul KV，服务发现能力再升级](https://www.apiseven.com/blog/integrate-consul-kv-with-apache-apisix)。

## 基于 DNS 的服务发现

Consul 不仅支持 HTTP API，而且还支持 DNS API，它内置了一个小型的 DNS 服务器，默认端口为 8600，我们以上面的 `consul-client` 为例，介绍如何在 APISIX 中集成 DNS 的服务发现。

注册到 Consul 中的服务默认会在 Consul DNS 中添加一条 `<服务名>.service.consul` 这样的域名记录，使用 `dig` 命令可以查询该域名的信息：

```
$ dig @192.168.1.40 -p 8600 consul-client.service.consul

; <<>> DiG 9.11.3-1ubuntu1.17-Ubuntu <<>> @192.168.1.40 -p 8600 consul-client.service.consul
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 32989
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;consul-client.service.consul.  IN      A

;; ANSWER SECTION:
consul-client.service.consul. 0 IN      A       192.168.1.40

;; Query time: 4 msec
;; SERVER: 192.168.1.40#8600(192.168.1.40)
;; WHEN: Tue Mar 21 07:17:40 CST 2023
;; MSG SIZE  rcvd: 73
```

上面的查询结果中只包含 `A` 记录，`A` 记录中只有 IP 地址，没有服务端口，如果用 `A` 记录来做服务发现，服务的端口必须得固定；好在 Consul 还支持 `SRV` 记录，`SRV` 记录中包含了服务的 IP 和端口信息：

```
$ dig @192.168.1.40 -p 8600 consul-client.service.consul SRV

; <<>> DiG 9.11.3-1ubuntu1.17-Ubuntu <<>> @192.168.1.40 -p 8600 consul-client.service.consul SRV
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41141
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 3
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;consul-client.service.consul.  IN      SRV

;; ANSWER SECTION:
consul-client.service.consul. 0 IN      SRV     1 1 8083 c0a80128.addr.dc1.consul.

;; ADDITIONAL SECTION:
c0a80128.addr.dc1.consul. 0     IN      A       192.168.1.40
agent-one.node.dc1.consul. 0    IN      TXT     "consul-network-segment="

;; Query time: 3 msec
;; SERVER: 192.168.1.40#8600(192.168.1.40)
;; WHEN: Tue Mar 21 07:18:22 CST 2023
;; MSG SIZE  rcvd: 168
```

我们在 APISIX 的配置文件 `config.yaml` 中添加如下内容：

```
discovery:
  dns:
    servers:
      - "192.168.1.40:8600"
```

然后重启 APISIX，接着向 APISIX 中添加如下路由：

```
$ curl -X PUT http://127.0.0.1:9180/apisix/admin/routes/55 \
    -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -i -d '
{
    "methods": ["GET"],
    "uri": "/dns",
    "plugins": {
        "proxy-rewrite" : {
            "regex_uri": ["/dns", "/"]
        }
    },
    "upstream": {
        "type": "roundrobin",
        "discovery_type": "dns",
		"service_name": "consul-client.service.consul"
    }
}'
```

访问 APISIX 的 `/dns` 地址验证一下：

```
$ curl http://127.0.0.1:9080/dns
Hello, I'm consul client.
```

关于 Consul DNS 的更多信息，可以参考官方文档 [Discover services with DNS](https://developer.hashicorp.com/consul/docs/services/discovery/dns-overview)，除了 Consul DNS，我们也可以使用其他的 DNS 服务器来做服务发现，比如 [CoreDNS](https://coredns.io/) 就是 Kubernetes 环境下的服务发现默认实现。

关于 APISIX 集成 DNS 的更多信息，可以参考官方文档 [基于 DNS 的服务发现](https://apisix.apache.org/zh/docs/apisix/discovery/dns/) 和官方博客 [API 网关 Apache APISIX 携手 CoreDNS 打开服务发现新大门](https://www.apiseven.com/blog/apisix-uses-coredns-enable-service-discovery)。

## 基于 APISIX-Seed 架构的控制面服务发现

上面所介绍的所有服务发现机制都是在 APISIX 上进行的，我们需要修改 APISIX 的配置，并重启 APISIX 才能生效，这种直接在网关上实现的服务发现也被称为 **数据面服务发现**，APISIX 还支持另一种服务发现机制，称为 **控制面服务发现**。

控制面服务发现不直接对 APISIX 进行修改，而是将服务发现结果保存到 Etcd 中，APISIX 实时监听 Etcd 的数据变化，从而实现服务发现：

![](./images/control-plane-service-discovery.png)

APISIX 通过 [APISIX-Seed](https://github.com/api7/apisix-seed) 项目实现了控制面服务发现，这样做有下面几个好处：

* 简化了 APISIX 的网络拓扑，APISIX 只需要关注 Etcd 的数据变化即可，不再和每个注册中心保持网络连接；
* APISIX 不用额外存储注册中心的服务数据，减小内存占用；
* APISIX 的配置变得简单，更容易管理；

虽然如此，目前 APISIX-Seed 还只是一个实验性的项目，从 GitHub 上的活跃度来看，官方似乎对它的投入并不是很高，目前只支持 [ZooKeeper](https://github.com/api7/apisix-seed/blob/main/docs/zh/latest/zookeeper.md) 和 [Nacos](https://github.com/api7/apisix-seed/blob/main/docs/zh/latest/nacos.md) 两种服务发现，而且官方也没有提供 APISIX-Seed 安装包的下载，需要我们自己通过源码来构建：

```
$ git clone https://github.com/api7/apisix-seed.git
$ make build
```

构建完成后，可以得到一个 `apisix-seed` 可执行文件，然后我们以上面的 Nacos 为例，介绍如何通过 APISIX-Seed 来实现控制面服务发现。

首先，我们将 APISIX 的配置文件中所有服务发现相关的配置都删掉，并重启 APISIX，接着打开 `conf/conf.yaml` 配置文件，文件中已经提前配置好了 Etcd、ZooKeeper、Nacos 等相关的配置，我们对其做一点裁剪，只保留下面这些信息：

```
etcd:
  host:
    - "http://127.0.0.1:2379"
  prefix: /apisix
  timeout: 30
    
log:
  level: warn
  path: apisix-seed.log
  maxage: 168h
  maxsize: 104857600
  rotation_time: 1h

discovery:
  nacos:
    host:
      - "http://127.0.0.1:8848"
    prefix: /nacos
```

然后启动 `apisix-seed`：

```
$ ./apisix-seed
panic: no discoverer with key: dns

goroutine 15 [running]:
github.com/api7/apisix-seed/internal/discoverer.GetDiscoverer(...)
        D:/code/apisix-seed/internal/discoverer/discovererhub.go:42
        D:/code/apisix-seed/internal/core/components/watcher.go:84 +0x1d4
created by github.com/api7/apisix-seed/internal/core/components.(*Watcher).Init
        D:/code/apisix-seed/internal/core/components/watcher.go:48 +0x2b6
panic: no discoverer with key: consul

goroutine 13 [running]:
github.com/api7/apisix-seed/internal/discoverer.GetDiscoverer(...)
        D:/code/apisix-seed/internal/discoverer/discovererhub.go:42
github.com/api7/apisix-seed/internal/core/components.(*Watcher).handleQuery(0x0?, 0xc000091200, 0x0?)
        D:/code/apisix-seed/internal/core/components/watcher.go:84 +0x1d4
created by github.com/api7/apisix-seed/internal/core/components.(*Watcher).Init
        D:/code/apisix-seed/internal/core/components/watcher.go:48 +0x2b6
```

不过由于上面我们在路由中添加了 dns、consul 这些服务发现类型，这些 APISIX-Seed 是不支持的，所以启动会报错，我们需要将这些路由删掉：

```
$ curl -X DELETE http://127.0.0.1:9180/apisix/admin/routes/11 -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1'
$ curl -X DELETE http://127.0.0.1:9180/apisix/admin/routes/33 -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1'
$ curl -X DELETE http://127.0.0.1:9180/apisix/admin/routes/44 -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1'
$ curl -X DELETE http://127.0.0.1:9180/apisix/admin/routes/55 -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1'
```

只保留一条 `/nacos` 的路由，然后重启 `apisix-seed` 即可：

```
$ ./apisix-seed
2023-03-22T07:49:53.849+0800    INFO    naming_client/push_receiver.go:80       udp server start, port: 55038
```

访问 APISIX 的 `/nacos` 地址验证一下：

```
$ curl http://127.0.0.1:9080/nacos
Hello, I'm nacos client.
```

关于 APISIX-Seed 的更多信息，可以参考官方文档 [基于 APISIX-Seed 架构的控制面服务发现](https://apisix.apache.org/zh/docs/apisix/discovery/control-plane-service-discovery/) 和 [APISIX-Seed 项目文档](https://github.com/api7/apisix-seed)。

## 基于 Kubernetes 的服务发现

我们的服务还可能部署在 Kubernetes 集群中，这时，不用依赖外部的服务注册中心也可以实现服务发现，因为 Kubernetes 提供了强大而丰富的监听资源的接口，我们可以通过监听 Kubernetes 集群中 Services 或 Endpoints 等资源的实时变化来实现服务发现，APISIX 就是这样做的。

我们以 [week013-playing-with-kubernetes](../week013-playing-with-kubernetes/README.md) 中的 `kubernetes-bootcamp` 为例，体验一下 APISIX 基于 Kubernetes 的服务发现。

首先在 Kubernetes 集群中创建对应的 Deployment 和 Service：

```
$ kubectl create deployment kubernetes-bootcamp --image=jocatalin/kubernetes-bootcamp:v1
deployment.apps/kubernetes-bootcamp created

$ kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080
service/kubernetes-bootcamp exposed
```

通过 `kubectl get svc` 获取 NodePort 端口，并验证服务能正常访问：

```
$ kubectl get svc
NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes            ClusterIP   10.96.0.1       <none>        443/TCP          115d
kubernetes-bootcamp   NodePort    10.101.31.128   <none>        8080:32277/TCP   59s

$ curl http://192.168.1.40:32277
Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-857b45f5bb-jtzs4 | v=1
```

接下来，为了让 APISIX 能查询和监听 Kubernetes 的 Endpoints 资源变动，我们需要创建一个 `ServiceAccount`：

```
kind: ServiceAccount
apiVersion: v1
metadata:
 name: apisix-test
 namespace: default
```

以及一个具有集群级查询和监听 Endpoints 资源权限的 `ClusterRole`：

```
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: apisix-test
rules:
- apiGroups: [ "" ]
  resources: [ endpoints ]
  verbs: [ get,list,watch ]
```

再将这个 `ServiceAccount` 和 `ClusterRole` 关联起来：

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: apisix-test
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: apisix-test
subjects:
  - kind: ServiceAccount
    name: apisix-test
    namespace: default
```

然后我们需要获取这个 ServiceAccount 的 token 值，如果 Kubernetes 是 v1.24 之前的版本，可以通过下面的方法获取 token 值：

```
$ kubectl get secrets | grep apisix-test
$ kubectl get secret apisix-test-token-c64cv -o jsonpath={.data.token} | base64 -d
```

Kubernetes 从 v1.24 版本开始，不能再通过 `kubectl get secret` 获取 token 了，需要使用 `TokenRequest API` 来获取，首先开启代理：

```
$ kubectl proxy --port=8001
Starting to serve on 127.0.0.1:8001
```

然后调用 `TokenRequest API` 生成一个 token：

```
$ curl 'http://127.0.0.1:8001/api/v1/namespaces/default/serviceaccounts/apisix-test/token' \
  -H "Content-Type:application/json" -X POST -d '{}'
{
  "kind": "TokenRequest",
  "apiVersion": "authentication.k8s.io/v1",
  "metadata": {
    "name": "apisix-test",
    "namespace": "default",
    "creationTimestamp": "2023-03-22T23:57:20Z",
    "managedFields": [
      {
        "manager": "curl",
        "operation": "Update",
        "apiVersion": "authentication.k8s.io/v1",
        "time": "2023-03-22T23:57:20Z",
        "fieldsType": "FieldsV1",
        "fieldsV1": {
          "f:spec": {
            "f:expirationSeconds": {}
          }
        },
        "subresource": "token"
      }
    ]
  },
  "spec": {
    "audiences": [
      "https://kubernetes.default.svc.cluster.local"
    ],
    "expirationSeconds": 3600,
    "boundObjectRef": null
  },
  "status": {
    "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImtLdHRyVzFmNTRHWGFVUjVRS3hrLVJMSElNaXM4aENLMnpfSGk1SUJhbVkifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjc5NTMzMDQwLCJpYXQiOjE2Nzk1Mjk0NDAsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0Iiwic2VydmljZWFjY291bnQiOnsibmFtZSI6ImFwaXNpeC10ZXN0IiwidWlkIjoiMzVjZWJkYTEtNGZjNC00N2JlLWIxN2QtZDA4NWJlNzU5ODRlIn19LCJuYmYiOjE2Nzk1Mjk0NDAsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmFwaXNpeC10ZXN0In0.YexM_VoumpdwZNbSkwh6IbEu59PCtZrG1lkTnCqG24G-TC0U1sGxgbXf6AnUQ5ybh-CHWbJ7oewhkg_J4j7FiSAnV_yCcEygLkaCveGIQbWldB3phDlcJ52f8YDpHFtN2vdyVTm79ECwEInDsqKhn4n9tPY4pgTodI6D9j-lcK0ywUdbdlL5VHiOw9jlnS7b60fKWBwCPyW2uohX5X43gnUr3E1Wekgpo47vx8lahTZQqnORahTdl7bsPsu_apf7LMw40FLpspVO6wih-30Ke8CNBxjpORtX2n3oteE1fi2vxYHoyJSeh1Pro_Oykauch0InFUNyEVI4kJQ720glOw",
    "expirationTimestamp": "2023-03-23T00:57:20Z"
  }
}
```

默认的 token 有效期只有一个小时，可以通过参数改为一年：

```
$ curl 'http://127.0.0.1:8001/api/v1/namespaces/default/serviceaccounts/apisix-test/token' \
  -H "Content-Type:application/json" -X POST \
  -d '{"kind":"TokenRequest","apiVersion":"authentication.k8s.io/v1","metadata":{"name":"apisix-test","namespace":"default"},"spec":{"audiences":["https://kubernetes.default.svc.cluster.local"],"expirationSeconds":31536000}}'
```

我们在 APISIX 的配置文件 `config.yaml` 中添加如下内容（ 将上面生成的 token 填写到 `token` 字段 ）：

```
discovery:
  kubernetes:
    service:
      schema: https
      host: 127.0.0.1
      port: "6443"
    client:
      token: ...
```

>
> 这里有一个比较坑的地方，`port` 必须是字符串，否则会导致 APISIX 启动报错：
> 
> ```
> invalid discovery kubernetes configuration: object matches none of the required
> ```
> 

然后重启 APISIX，接着向 APISIX 中添加如下路由：

```
$ curl -X PUT http://127.0.0.1:9180/apisix/admin/routes/66 \
    -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -i -d '
{
    "methods": ["GET"],
    "uri": "/kubernetes",
    "plugins": {
        "proxy-rewrite" : {
            "regex_uri": ["/kubernetes", "/"]
        }
    },
    "upstream": {
        "type": "roundrobin",
        "discovery_type": "kubernetes",
        "service_name": "kubernetes-bootcamp"
    }
}'
```

访问 APISIX 的 `/kubernetes` 地址验证一下：

```
$ curl http://127.0.0.1:9080/kubernetes
```

不过，如果你的 APISIX 运行在 Kubernetes 集群之外，大概率是访问不通的，因为 APISIX 监听的 Endpoints 地址是 Kubernetes 集群内的 Pod 地址：

```
$ kubectl describe endpoints/kubernetes-bootcamp
Name:         kubernetes-bootcamp
Namespace:    default
Labels:       app=kubernetes-bootcamp
Annotations:  endpoints.kubernetes.io/last-change-trigger-time: 2023-03-25T00:31:43Z
Subsets:
  Addresses:          10.1.5.12
  NotReadyAddresses:  <none>
  Ports:
    Name     Port  Protocol
    ----     ----  --------
    <unset>  8080  TCP

Events:  <none>
```

所以想使用基于 Kubernetes 的服务发现，最佳做法是将 APISIX 部署在 Kubernetes 中，或者使用 [APISIX Ingress](https://apisix.apache.org/zh/docs/ingress-controller/getting-started/)，关于 APISIX 集成 Kubernetes 的更多信息，可以参考官方文档 [基于 Kubernetes 的服务发现](https://apisix.apache.org/zh/docs/apisix/discovery/kubernetes/) 和官方博客 [借助 APISIX Ingress，实现与注册中心的无缝集成](https://www.apiseven.com/blog/apisix-ingress-integrates-with-service-discovery)。

## 参考

* [集成服务发现注册中心](https://apisix.apache.org/zh/docs/apisix/discovery/)
* [API 网关 Apache APISIX 集成 Eureka 作为服务发现](https://www.apiseven.com/blog/apigateway-integration-eureka-service-discovery)
* [API 网关 Apache APISIX 携手 CoreDNS 打开服务发现新大门](https://www.apiseven.com/blog/apisix-uses-coredns-enable-service-discovery)
* [Nacos 在 API 网关中的服务发现实践](https://www.apiseven.com/blog/nacos-api-gateway)
* [SpringBoot使用Nacos进行服务注册发现与配置管理](https://cloud.tencent.com/developer/article/1650073)
* [springcloud(十三)：注册中心 Consul 使用详解](http://www.ityouknow.com/springcloud/2018/07/20/spring-cloud-consul.html)
* [Spring Cloud Consul 官方文档](https://docs.spring.io/spring-cloud-consul/docs/current/reference/html/)
* [Consul 简介和快速入门](https://book-consul-guide.vnzmi.com/)

## 更多

### 实现自定义服务发现

https://apisix.apache.org/zh/docs/apisix/discovery/


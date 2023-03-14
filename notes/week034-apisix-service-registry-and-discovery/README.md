# WEEK034 - 实战 APISIX 服务注册和发现

在 [week030-apisix-notes](../week030-apisix-notes/README.md) 中，我们通过 APISIX 官方提供的入门示例学习了 APISIX 的基本概念，并使用 Admin API 和 Dashboard 两种方法创建路由。在创建路由时，我们必须明确地知道服务的 IP 和端口，这给运维人员带来了一定的负担，因为服务的重启或扩缩容都可能会导致服务的 IP 和端口发生变化，当服务数量非常多的时候，维护成本将急剧升高。

APISIX 集成了多种服务发现机制来解决这个问题，通过服务注册中心，APISIX 可以动态地获取服务的实例信息，这样我们就不用在路由中写死固定的 IP 和端口了：

![](./images/discovery-cn.png)

## 服务发现

### 基于 Eureka 的服务发现

https://apisix.apache.org/zh/docs/apisix/discovery/

### 基于 Consul 的服务发现

https://apisix.apache.org/zh/docs/apisix/discovery/consul/

### 基于 Nacos 的服务发现

https://apisix.apache.org/zh/docs/apisix/discovery/nacos/

### 基于 DNS 的服务发现

https://apisix.apache.org/zh/docs/apisix/discovery/dns/

### 基于 APISIX-Seed 架构的控制面服务发现

https://apisix.apache.org/zh/docs/apisix/discovery/control-plane-service-discovery/

### 基于 Kubernetes 的服务发现

https://apisix.apache.org/zh/docs/apisix/discovery/kubernetes/

## 实现自定义服务发现

https://apisix.apache.org/zh/docs/apisix/discovery/

## 服务注册

## 参考

* [集成服务发现注册中心](https://apisix.apache.org/zh/docs/apisix/discovery/)
* [API 网关 Apache APISIX 集成 Eureka 作为服务发现](https://www.apiseven.com/blog/apigateway-integration-eureka-service-discovery)
* [API 网关 Apache APISIX 携手 CoreDNS 打开服务发现新大门](https://www.apiseven.com/blog/apisix-uses-coredns-enable-service-discovery)
* [Nacos 在 API 网关中的服务发现实践](https://www.apiseven.com/blog/nacos-api-gateway)
* [借助 APISIX Ingress，实现与注册中心的无缝集成](https://www.apiseven.com/blog/apisix-ingress-integrates-with-service-discovery)
* [APISIX Blog](https://apisix.apache.org/zh/blog/)
* [API7.ai Blog](https://www.apiseven.com/blog)

# WEEK007 CNCF 项目学习笔记（Envoy）

[Envoy](https://www.envoyproxy.io/) 是一款专为大型的 SOA 架构（面向服务架构，service oriented architectures）设计的 L7 代理和通信总线，它的诞生源于以下理念：

> 对应用程序而言，网络应该是透明的。当网络和应用程序出现故障时，应该能够很容易确定问题的根源。

要实现上面的目标是非常困难的，为了做到这一点，Envoy 提供了以下特性：

* **进程外架构**

Envoy 是一个独立的进程，伴随着每个应用程序运行。所有的 Envoy 形成一个透明的通信网络，每个应用程序发送消息到本地主机或从本地主机接收消息，不需要知道网络拓扑。进程外架构的好处是与应用程序的语言无关，Envoy 可以和任意语言的应用程序一起工作，另外，Envoy 的部署和升级也非常方便。

这种模式也被称为 **边车模式（Sidecar）**。

* **L3/L4 过滤器架构**

Envoy 是一个 L3/L4 网络代理，通过插件化的 **过滤器链（filter chain）** 机制处理各种 TCP/UDP 代理任务，支持 TCP 代理，UDP 代理，TLS 证书认证，Redis 协议，MongoDB 协议，Postgres 协议等。

* **HTTP L7 过滤器架构**

Envoy 不仅支持 L3/L4 代理，也支持 HTTP L7 代理，通过 **HTTP 连接管理子系统（HTTP connection management subsystem）** 可以实现诸如缓存、限流、路由等代理任务。

* **支持 HTTP/2**

在 HTTP 模式下，Envoy 同时支持 HTTP/1.1 和 HTTP/2。在 `service to service` 配置中，官方也推荐使用 HTTP/2 协议。

* **支持 HTTP/3（alpha）**

从 1.19.0 版本开始，Envoy 支持 HTTP/3。

* **HTTP L7 路由**

Envoy 可以根据请求的路径（path）、认证信息（authority）、Content Type、运行时参数等来配置路由和重定向。这在 Envoy 作为前端代理或边缘代理时非常有用。

* **支持 gRPC**

gRPC 是 Google 基于 HTTP/2 开发的一个 RPC 框架。Envoy 完美的支持 HTTP/2，也可以很方便的支持 gRPC。

* **服务发现和动态配置**

Envoy 可以通过一套动态配置 API 来进行中心化管理，这套 API 被称为 **[xDS](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/operations/dynamic_configuration)**：EDS（Endpoint Discovery Service）、CDS（Cluster Discovery Service）、RDS（Route Discovery Service）、VHDS（Virtual Host Discovery Service）、LDS（Listener Discovery Service）、SDS（Secret Discovery Service）等等。

* **健康状态检查**

Envoy 通过对上游服务集群进行健康状态检查，并根据服务发现和健康检查的结果来决定负载均衡的目标。

* **高级负载均衡**

Envoy 支持很多高级负载均衡功能，比如：自动重试、熔断、全局限流、流量跟踪（request shadowing）、异常检测（outlier detection）等。

* **支持前端代理和边缘代理**

* **可观测性**

Envoy 的主要目标是使网络透明，可以生成许多流量方面的统计数据，这是其它代理软件很难取代的地方，内置 `stats` 模块，可以集成诸如 prometheus/statsd 等监控方案。还可以集成分布式追踪系统，对请求进行追踪。

## 安装 Envoy



## 参考

1. [What is Envoy](https://www.envoyproxy.io/docs/envoy/latest/intro/what_is_envoy)

https://cloud.tencent.com/developer/article/1554609
https://www.jianshu.com/p/d9db52330c0f
https://github.com/yangchuansheng/envoy-handbook
https://www.bbsmax.com/A/Ae5RK6VLdQ/
https://www.linux-note.cn/?p=1543


https://www.envoyproxy.io/docs/envoy/latest/
https://cloudnative.to/envoy/

https://jimmysong.io/envoy-handbook/
https://jimmysong.io/kubernetes-handbook/usecases/envoy.html

https://www.servicemesher.com/istio-handbook/concepts/envoy.html


## 更多


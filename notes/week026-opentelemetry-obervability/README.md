# WEEK026 - 基于 OpenTelemetry 的可观测性实战

[可观测性](https://en.wikipedia.org/wiki/Observability)（Observability）这个词来源于控制理论，它是由匈牙利裔美国工程师 [Rudolf E. Kálmán](https://en.wikipedia.org/wiki/Rudolf_E._K%C3%A1lm%C3%A1n) 针对线性动态控制系统所提出的一个概念，表示 **通过系统外部输出推到其内部状态的程度**。

> Observability is a measure of how well internal states of a system can be inferred from knowledge of its external outputs.

在可观测性这个概念被引入软件行业之前，我们对一个软件系统的观测一般都是从日志、指标和链路跟踪三个方面独立进行，并且在每个领域都积累了丰富的经验，也诞生了大量优秀的产品。比如说到日志收集和分析方面，大家基本上都会想到 [Elastic Stack](https://www.elastic.co/elastic-stack) 技术栈（ELK、EFK）；而对于指标监控，[Prometheus](https://prometheus.io/) 差不多已经成为了这方面的事实标准；另外，还有 [SkyWalking](https://skywalking.apache.org/)、[Zipkin](https://zipkin.io/)、[Jaeger](https://www.jaegertracing.io/) 这些链路跟踪的开源项目。

渐渐地，大家也意识到这三个方面并不是完全独立的，而是存在互相重合的现象，比如运维人员在查看系统 CPU 或内存等指标的图表时，如果发现异常，我们希望能快速定位到这个时间段的日志，看看有没有什么错误信息（从指标到日志）；或者在日志系统中看到一条错误日志时，我们希望追踪到链路的入口位置，看看最源头的请求参数是什么（从日志到链路）。

![](./images/metrics-to-logs.png)

2017 年，德国工程师 [Peter Bourgon](https://peter.bourgon.org/about/) 写了一篇非常有名的博客文章[《Metrics, Tracing, and Logging》](https://peter.bourgon.org/blog/2017/02/21/metrics-tracing-and-logging.html)，他在这篇文章中系统阐述了指标、日志和链路跟踪三者的定义和它们之间的关系：

![](./images/metrics-logging-tracing.png)

他总结到：

* 指标的特点是 **它是可聚合的（Aggregatable）**，比如接收的 HTTP 请求数这个指标我们可以建模为计数器（counter），每次 HTTP 请求就是对其做加法聚合;
* 日志的特点是 **它是对离散事件的处理（Events）**，比如我们经常在代码中打印的调试日志或错误日志，系统的审计日志等；
* 链路跟踪的特点是 **它是对请求范围内的信息的处理（Request-scoped）**，任何数据都可以绑定到这个事务对象的生命周期中，比如对于一个 HTTP 请求的链路，我们可以记录每个请求节点的状态，节点的耗时，谁接收了这个请求等等；

我们从图中可以看到这三者之间是有部分重合的，比如上面讲的 HTTP 请求数这个指标，很显然可以绑定到这个请求的链路中，这被称为 **请求范围内的指标（Request-scoped metrics）**，当然也有些指标不是请求范围内的，比如机器的 CPU 利用率、内存占用、磁盘空间等。而对于一些日志，比如请求报错，也可以绑定到请求链路中，称为 **请求范围内的事件（Request-scoped events）**。

通过这样的划分，我们可以对系统中的日志和指标等数据进行更合理地设计，也对后来所有的可观测性产品提供了边界。2018 年，Apple 的工程师 Cindy Sridharan 在他新出版的书籍 [《
Distributed Systems Observability》](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/) 中正式提出了分布式系统可观测性的概念，介绍了可观测性和传统监控的区别，以及如何通过可观测性的三大支柱（日志、指标监控和链路跟踪）构建完整的观测模型，从而实现分布式系统的故障诊断、根因分析和快速恢复。同年，CNCF 社区也将可观测性引入 [Cloud Native Landscape](https://landscape.cncf.io/) 作为云原生领域不可或缺的一部分。

## OpenTelemetry

## 快速开始

为了让用户能快速地体验和上手 OpenTelemetry，官方提供了一个名为 [Astronomy Shop](https://github.com/open-telemetry/opentelemetry-demo) 的 Demo 服务，接下来我们就按照 [Quick Start](https://github.com/open-telemetry/opentelemetry-demo/blob/main/docs/docker_deployment.md) 的步骤，部署这个 Demo 服务并体验 OpenTelemetry。

## 参考

1. [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
1. [OpenTelemetry 中文文档](https://github.com/open-telemetry/docs-cn)
1. [OpenTelemetry 可观测性的未来](https://lib.jimmysong.io/opentelemetry-obervability/) - 作者 Ted Young，译者 Jimmy Song
1. [OpenTelemetry 简析](https://mp.weixin.qq.com/s/n4eVf2KZRIp2yKACk88qJA) -  阿里云云原生
1. [End-to-end tracing with OpenTelemetry](https://blog.frankel.ch/end-to-end-tracing-opentelemetry/) - Nicolas Fränkel
1. [OpenTelemetry初體驗：實踐Chaos Engineering來Drive the Observability's best practice](https://engineering.linecorp.com/zh-hant/blog/opentelemetry-chaos-engineering-drive-the-observability-best-practice/) - Johnny Pan
1. [淺談DevOps與Observability 系列](https://ithelp.ithome.com.tw/users/20104930/ironman/4960)
1. [可观测性](http://icyfenix.cn/distribution/observability/) - 凤凰架构

## 更多

1. [Kratos 学习笔记 - 基于 OpenTelemetry 的链路追踪](https://go-kratos.dev/blog/go-kratos-opentelemetry-practice/)
1. [使用 OpenTelemetry Collector 来收集追踪信息，发送至 AppInsights](https://docs.dapr.io/zh-hans/operations/monitoring/tracing/open-telemetry-collector-appinsights/) - Dapr 文档库
1. [一文读懂可观测性与Opentelemetry](https://mp.weixin.qq.com/s/TUH3rlbSqYoPaeyMCbfRTQ)
1. [可观测性 — Overview](https://is-cloud.blog.csdn.net/article/details/126337586)

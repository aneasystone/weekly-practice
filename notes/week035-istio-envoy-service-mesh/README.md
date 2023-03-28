# WEEK035 - 使用 Istio 和 Envoy 打造 Service Mesh 微服务架构

[周志明](https://github.com/fenixsoft) 老师在他的 [《凤凰架构》](http://icyfenix.cn/immutable-infrastructure/mesh/communication.html) 中将分布式服务通信的演化历史分成五个阶段：

* 第一阶段：将通信的非功能性需求视作业务需求的一部分，通信的可靠性由程序员来保障

* 第二阶段：将代码中的通信功能抽离重构成公共组件库，通信的可靠性由专业的平台程序员来保障

* 第三阶段：将负责通信的公共组件库分离到进程之外，程序间通过网络代理来交互，通信的可靠性由专门的网络代理提供商来保障

* 第四阶段：将网络代理以边车的形式注入到应用容器，自动劫持应用的网络流量，通信的可靠性由专门的通信基础设施来保障

* 第五阶段：将边车代理统一管控起来实现安全、可控、可观测的通信，将数据平面与控制平面分离开来，实现通用、透明的通信，这项工作就由专门的服务网格框架来保障

## 参考

* [透明通信的涅槃 | 凤凰架构](http://icyfenix.cn/immutable-infrastructure/mesh/communication.html)
* [服务网格与生态 | 凤凰架构](http://icyfenix.cn/immutable-infrastructure/mesh/ecosystems.html)
* [Pattern: Service Mesh](https://philcalcado.com/2017/08/03/pattern_service_mesh.html)
* [什么是Service Mesh（服务网格）？](https://jimmysong.io/blog/what-is-a-service-mesh/)
* [Istio 服务网格](https://istio.io/latest/zh/about/service-mesh/)
* [服务网格终极指南第二版——下一代微服务开发](https://cloudnative.to/blog/service-mesh-ultimate-guide-e2/)
* [Istio Handbook——Istio 服务网格进阶实战](http://www.zhaowenyu.com/istio-doc/)
* [谈谈微服务架构中的基础设施：Service Mesh与Istio](https://www.zhaohuabing.com/2018/03/29/what-is-service-mesh-and-istio/)
* [Jimmy Song 的原创博客](https://jimmysong.io/blog/)
* [云原生社区博客](https://cloudnative.to/blog/)

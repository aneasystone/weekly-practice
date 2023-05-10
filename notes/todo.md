# TODO LIST

## Java

### 学习 JNI

* [Guide to JNI (Java Native Interface)](https://www.baeldung.com/jni)

### 学习 JUnit

* [Best Practices for Unit Testing in Java](https://www.baeldung.com/java-unit-testing-best-practices)

### Java 性能调优

* [Unleash the Power of Open Source Java Profilers: Comparing VisualVM, JMC, and async-profiler](https://www.infoq.com/articles/open-source-java-profilers/)

### Java 排错技巧

* [CPU爆了，你却连那个线程出问题都不知道？](https://mp.weixin.qq.com/s/FvmlnV-oKNxrK5glrFKPHA)

### Spring Boot 启动优化

* [7min到40s：SpringBoot启动优化实践](https://juejin.cn/post/7181342523728592955)

### Reactor 响应式编程

* [Flux、Mono、Reactor 实战（史上最全）](https://blog.csdn.net/crazymakercircle/article/details/124120506)

## 聊聊 Java 中的锁技术

* [聊聊 13 种锁的实现方式](https://mp.weixin.qq.com/s/AOshaWGmLw6uw92xKhLAvQ)

### Java 动态代理

* [动态代理大揭秘，带你彻底弄清楚动态代理！](https://my.oschina.net/u/1584523/blog/5261706)

### JMX

* [Calling JMX MBean Method From a Shell Script](https://www.baeldung.com/jmx-mbean-shell-access)

### 实现 Spring Boot 3 应用的可观测性

* [Observability with Spring Boot 3](https://spring.io/blog/2022/10/12/observability-with-spring-boot-3)
* [OpenTelemetry Setup in Spring Boot Application](https://www.baeldung.com/spring-boot-opentelemetry-setup)
* [Micrometer Documentation](https://micrometer.io/docs)
	* [Micrometer Observation](https://micrometer.io/docs/observation)
	* [Micrometer Tracing](https://micrometer.io/docs/tracing)
	* [Micrometer Context Propagation](https://micrometer.io/docs/contextPropagation)

### 使用 Picocli 打造一个命令行程序

* [picocli - a mighty tiny command line interface](https://picocli.info/)
* [Picocli 2.0: 以少求多](https://picocli.info/zh/picocli-2.0-do-more-with-less.html)
* [Java命令行界面（第10部分）：picocli](https://blog.csdn.net/dnc8371/article/details/106702365)
* [Picocli 2.0: Steroids上的Groovy脚本](https://picocli.info/zh/picocli-2.0-groovy-scripts-on-steroids.html)
* [从Commons CLI迁移到Picocli](https://blog.csdn.net/Tybyqi/article/details/85787550)
* [如何借助 Graalvm 和 Picocli 构建 Java 编写的原生 CLI 应用](https://www.infoq.cn/article/4RRJuxPRE80h7YsHZJtX)

## Kubernetes

### 学习 Kubernetes 的用户认证

* [为Kubernetes集群添加用户](https://zhuanlan.zhihu.com/p/43237959)
* [创建用户认证授权的 kubeconfig 文件](https://jimmysong.io/kubernetes-handbook/guide/kubectl-user-authentication-authorization.html)

### 学习 Kubernetes 的准入控制

* [Admission Controllers Reference](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)
* [云原生策略引擎 Kyverno （上）](https://moelove.info/2022/03/02/%E4%BA%91%E5%8E%9F%E7%94%9F%E7%AD%96%E7%95%A5%E5%BC%95%E6%93%8E-Kyverno-%E4%B8%8A/)

### Kubernetes 故障排查

* [排障技能](https://imroc.cc/kubernetes/troubleshooting/skill/index.html)
* [监控、日志和调试](https://kubernetes.io/zh-cn/docs/tasks/debug/)

### 学习 Kubernetes 的工作负载

* [StatefulSet 的使用场景](https://kuboard.cn/learning/k8s-intermediate/workload/wl-statefulset/)

### etcd for Kubernetes

* [为 Kubernetes 运行 etcd 集群](https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/configure-upgrade-etcd/)
* [使用 etcdctl 访问 Kubernetes 数据](https://jimmysong.io/kubernetes-handbook/guide/using-etcdctl-to-access-kubernetes-data.html)
* [Using Fio to Tell Whether Your Storage is Fast Enough for Etcd](https://www.ibm.com/cloud/blog/using-fio-to-tell-whether-your-storage-is-fast-enough-for-etcd)
* [Hardware guidelines for administering etcd clusters](https://etcd.io/docs/v3.6/op-guide/hardware/)

## 数据库

### 数据库分片

* [数据库分片（Database Sharding)详解](https://zhuanlan.zhihu.com/p/57185574)
* [图解数据库分片技术](https://posts.careerengine.us/p/641433ce681dcb4a7b7d6da4)

### 缓存同步

* [MySQL 与 Redis 缓存的同步方案](https://mp.weixin.qq.com/s/e4qJp4zcXHJQycJwq1mgzQ)

## Linux

### 学习 tcpdump

* [tcpdump is amazing](https://jvns.ca/blog/2016/03/16/tcpdump-is-amazing/)

### Linux Shell 技巧总结

* [Shell test 单中括号[] 双中括号[[]] 的区别](https://www.cnblogs.com/zeweiwu/p/5485711.html)

## 其他

### WebAssembly

* [WebAssembly 助力云原生：APISIX 如何借助 Wasm 插件实现扩展功能？](https://apisix.apache.org/zh/blog/2023/03/30/what-is-wasm-and-how-does-apache-apisix-support-it/)

#### Wasm in Dapr

* [second-state/dapr-wasm](https://github.com/second-state/dapr-wasm) - A template project to demonstrate how to run WebAssembly functions as sidecar microservices in dapr

#### Wasmer

* [Wasmer examples](https://docs.wasmer.io/integrations/examples)

### mTLS

* [A Kubernetes engineer’s guide to mTLS](https://buoyant.io/mtls-guide)
* [mTLS everywhere!](https://blog.frankel.ch/mtls-everywhere/)
* [Mutual TLS Authentication](https://apisix.apache.org/docs/apisix/mtls/)
* [如何理解 Istio 中的 MTLS 流量加密？](https://jimmysong.io/blog/understanding-the-tls-encryption-in-istio/)
* [写给 Kubernetes 工程师的 mTLS 指南](https://lib.jimmysong.io/blog/mtls-guide/)

### 开发一个 Vue 组件

* [vue组件库开发](https://zq99299.gitbooks.io/vue-note/content/chapter/vu_components_lib/)
* [从零到一教你基于vue开发一个组件库](https://juejin.cn/post/6844904085808742407)

### ElasticSearch 查询指南

* [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
* [Search your data](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-your-data.html)
* [Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
* [Aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html)

### Go 学习笔记

* [Go-CRUD-demo](https://github.com/Conqueror712/Go-CRUD-demo) - Gin + Gorm + MySQL + Navicat

### 监控告警

* [夜莺 - All-in-one 的开源观测平台](https://github.com/ccfos/nightingale)

### Nginx

* [Nginx 常用配置及和基本功能讲解](https://my.oschina.net/u/4090830/blog/8694569)

### 算法

* [Building a Bloom filter](https://luminousmen.com/post/building-a-bloom-filter)

## 技术大会

* [可观测性峰会 2023 回顾及 PPT 下载](https://github.com/cloudnativeto/academy/tree/master/observability-summit/2023)

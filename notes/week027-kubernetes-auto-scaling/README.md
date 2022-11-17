# WEEK027 - 实战 Kubernetes 的动态扩缩容

在 [week013-playing-with-kubernetes](../week013-playing-with-kubernetes/README.md) 中，我们学习了 Kubernetes 中的 Pod、Deployment 和 Service 的一些基础知识，还学习了如何通过 `kubectl scale` 命令对应用进行扩容或缩容，以及 Kubernetes 的滚动更新机制。

虽然通过 `kubectl scale` 命令可以实现扩缩容功能，但是这个操作需要运维人员手工进行干预，不仅可能处理不及时，而且还可能误操作导致生产事故。如果我们能够根据系统当前的运行状态自动进行扩缩容，比如当检测到某个应用负载过高时自动对其扩容，这样就可以给运维人员带来极大的方便。为此，Kubernetes 提供了一种新的资源对象：[Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)（Pod 水平自动伸缩，简称 HPA），HPA 通过监控 Pod 的负载变化来确定是否需要调整 Pod 的副本数量，从而实现动态扩缩容。

## Metrics Server

## 基于 CPU 自动扩缩容

## 基于内存自动扩缩容

## 基于自定义指标自动扩缩容

## 参考

1. [Kubernetes：HPA 详解-基于 CPU、内存和自定义指标自动扩缩容](https://blog.csdn.net/fly910905/article/details/105375822/)
1. [自动伸缩 | Kuboard](https://kuboard.cn/learning/k8s-advanced/hpa/hpa.html)
1. [自动伸缩-例子 | Kuboard](https://kuboard.cn/learning/k8s-advanced/hpa/walkthrough.html)

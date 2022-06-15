# WEEK013 - Kubernetes 使用小记

Kubernetes 常常被简称为 K8S（发音：Kate's），是 Google 在 2014 年发布的一个开源容器编排引擎。它诞生自 Google 内部的一款容器管理系统 [Borg](https://research.google/pubs/pub43438/)，据说，Borg 管理着 Google 数据中心里 20 多亿个容器服务。自发布以来，Kubernetes 迅速获得开源社区的追捧，包括 Red Hat、VMware、Canonical 在内的很多有影响力的公司都加入到它的开发和推广阵营中，目前，AWS、Azure、Google、阿里云、腾讯云等厂商都推出了基于 Kubernetes 的 CaaS 或 PaaS 产品。

Kubernetes 属于平台级技术，覆盖的技术范围非常广，包括计算、网络、存储、高可用、监控、日志等多个方面，而且在 Kubernetes 中有很多新的概念和设计理念，所以有一定的入门门槛。

在 WEEK010 中，我们学习了如何使用 kind、minikube 和 kubeadmin 安装一个 Kubernetes 集群。这一节我们将照着 [官方教程](https://kubernetes.io/docs/tutorials/)，学习如何使用它，了解并掌握 Kubernetes 的基本概念。

## 使用 Minikube 创建集群

https://kubernetes.io/zh-cn/docs/tutorials/kubernetes-basics/create-cluster/cluster-intro/

## 使用 kubectl 创建 Deployment

https://kubernetes.io/zh-cn/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/

## 查看 Pod 和工作节点

https://kubernetes.io/zh-cn/docs/tutorials/kubernetes-basics/explore/explore-intro/

## 使用 Service 暴露你的应用

https://kubernetes.io/zh-cn/docs/tutorials/kubernetes-basics/expose/expose-intro/

## 运行应用程序的多个实例

https://kubernetes.io/zh-cn/docs/tutorials/kubernetes-basics/scale/scale-intro/

## 执行滚动更新

https://kubernetes.io/zh-cn/docs/tutorials/kubernetes-basics/update/update-intro/

## 参考

1. [学习 Kubernetes 基础知识](https://kubernetes.io/zh-cn/docs/tutorials/kubernetes-basics/)
1. [Kubernetes 术语表](https://kubernetes.io/docs/reference/glossary/)
1. [Play with Kubernetes](https://labs.play-with-k8s.com/)

## 更多

### Kubernetes 其他教程

https://kubernetes.io/docs/tutorials/

### Kubernetes 任务

https://kubernetes.io/docs/tasks/

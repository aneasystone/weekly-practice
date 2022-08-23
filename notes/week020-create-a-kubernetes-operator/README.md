# WEEK020 - 写一个简单的 Kubernetes Operator

[Kubernetes Operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) 这一概念是由 CoreOS 的工程师于 2016 年提出的，它是一种通过 [自定义资源](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)（custom resource、CR）来包装、运行和管理 Kubernetes 应用的方式。Kubernetes Operator 遵循 [control loop](https://kubernetes.io/docs/concepts/architecture/controller/) 原则，这是 Kubernetes 的核心原则之一，也是机器人和自动化领域中一种常见的持续运行动态系统的机制。它依赖于一种快速调整工作负载需求的能力，进而能够尽可能准确地适应现有资源。

![](./images/reconciliation-loop.png)

在 Kubernetes 中，这个循环被称为 `reconciliation loop`。在这个循环中，有一个非常重要的角色：`控制器`（Controller），它可以对集群的变化做出响应，并执行相应的动作。控制器首先观察 Kubernetes 对象的当前状态，然后通过 Kubernetes API 进行持续调整，直到将对象的当前状态变成所需状态为止。

第一个 Kubernetes Controller 是 `kube-controller-manager`，它被认为是所有 Operator 的鼻祖。

## 参考

1. [Kubernetes 文档 / 概念 / 扩展 Kubernetes / Operator 模式](https://kubernetes.io/zh-cn/docs/concepts/extend-kubernetes/operator/)
1. [Kubernetes Operator 基础入门](https://www.infoq.cn/article/3jrwfyszlu6jatbdrtov)
1. [Kubernetes Operator 快速入门教程](https://www.qikqiak.com/post/k8s-operator-101/)
1. [What is a Kubernetes operator?](https://www.redhat.com/en/topics/containers/what-is-a-kubernetes-operator)
1. [Kubernetes Operators 101, Part 1: Overview and key features](https://developers.redhat.com/articles/2021/06/11/kubernetes-operators-101-part-1-overview-and-key-features)
1. [Kubernetes Operators 101, Part 2: How operators work](https://developers.redhat.com/articles/2021/06/22/kubernetes-operators-101-part-2-how-operators-work)
1. [Download and install - The Go Programming Language](https://go.dev/doc/install)
1. [kubernetes-sigs/kubebuilder](https://github.com/kubernetes-sigs/kubebuilder) - SDK for building Kubernetes APIs using CRDs

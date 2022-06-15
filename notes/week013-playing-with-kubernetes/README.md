# WEEK013 - Kubernetes 使用小记

Kubernetes 常常被简称为 K8S（发音：Kate's），是 Google 在 2014 年发布的一个开源容器编排引擎。它诞生自 Google 内部的一款容器管理系统 [Borg](https://research.google/pubs/pub43438/)，据说，Borg 管理着 Google 数据中心里 20 多亿个容器服务。自发布以来，Kubernetes 迅速获得开源社区的追捧，包括 Red Hat、VMware、Canonical 在内的很多有影响力的公司都加入到它的开发和推广阵营中，目前，AWS、Azure、Google、阿里云、腾讯云等厂商都推出了基于 Kubernetes 的 CaaS 或 PaaS 产品。

Kubernetes 属于平台级技术，覆盖的技术范围非常广，包括计算、网络、存储、高可用、监控、日志等多个方面，而且在 Kubernetes 中有很多新的概念和设计理念，所以有一定的入门门槛。

在 WEEK010 中，我们学习了如何使用 Kind、Minikube 和 Kubeadmin 安装一个 Kubernetes 集群。这一节我们将照着 [官方教程](https://kubernetes.io/docs/tutorials/)，学习如何使用它，了解并掌握 Kubernetes 的基本概念。

## 使用 Minikube 创建集群

一个 Kubernetes 集群包含两种类型的资源：

* Master（也被称为控制平面 `Control Plane`）

用于管理整个集群，比如调度应用、维护应用状态、应用扩容和更新等。

* Node

每个 Node 上都运行着 `Kubelet` 程序，它负责运行应用，并且是和 Master 通信的代理。每个 Node 上还要有运行容器的工具，如 Docker 或 rkt。

我们可以使用 Minikube 创建一个单节点的简单集群。首先确保机器上已经安装 Minikube（安装步骤参考 WEEK010）：

```
$ minikube version
minikube version: v1.18.0
commit: ec61815d60f66a6e4f6353030a40b12362557caa-dirty
```

然后执行 `minikube start` 启动一个 Kubernetes 集群：

```
$ minikube start
* minikube v1.18.0 on Ubuntu 18.04 (amd64)
* Using the none driver based on existing profile

X The requested memory allocation of 2200MiB does not leave room for system overhead (total system memory: 2460MiB). You may face stability issues.
* Suggestion: Start minikube with less memory allocated: 'minikube start --memory=2200mb'

* Starting control plane node minikube in cluster minikube
* Running on localhost (CPUs=2, Memory=2460MB, Disk=194868MB) ...
* OS release is Ubuntu 18.04.5 LTS
* Preparing Kubernetes v1.20.2 on Docker 19.03.13 ...
  - kubelet.resolv-conf=/run/systemd/resolve/resolv.conf
  - Generating certificates and keys ...
  - Booting up control plane ...-
  - Configuring RBAC rules ...
* Configuring local host environment ...
* Verifying Kubernetes components...
  - Using image gcr.io/k8s-minikube/storage-provisioner:v4
* Enabled addons: default-storageclass, storage-provisioner
* Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

这样一个 Kubernetes 集群就安装好了，接下来我们就可以使用 `kubectl` 来管理这个集群。使用 `kubectl version` 查看客户端和服务端的版本信息：

```
$ kubectl version
Client Version: version.Info{Major:"1", Minor:"20", GitVersion:"v1.20.4", GitCommit:"e87da0bd6e03ec3fea7933c4b5263d151aafd07c", GitTreeState:"clean", BuildDate:"2021-02-18T16:12:00Z", GoVersion:"go1.15.8", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"20", GitVersion:"v1.20.2", GitCommit:"faecb196815e248d3ecfb03c680a4507229c2a56", GitTreeState:"clean", BuildDate:"2021-01-13T13:20:00Z", GoVersion:"go1.15.5", Compiler:"gc", Platform:"linux/amd64"}
```

使用 `kubectl cluster-info` 查看集群详情：

```
$ kubectl cluster-info
Kubernetes control plane is running at https://10.0.0.8:8443
KubeDNS is running at https://10.0.0.8:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

使用 `kubectl get nodes` 查看集群中的节点信息：

```
$ kubectl get nodes
NAME       STATUS   ROLES                  AGE     VERSION
minikube   Ready    control-plane,master   4m51s   v1.20.2
```

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

# WEEK031 - Helm 学习笔记

在 [week013-playing-with-kubernetes](../week013-playing-with-kubernetes/README.md) 中我们学习了如何通过 `Deployment` 部署一个简单的应用服务并通过 `Service` 来暴露它，在真实的场景中，一套完整的应用服务可能还会包含很多其他的 Kubernetes 资源，比如 `DaemonSet`、`Ingress`、`ConfigMap`、`Secret` 等，当用户部署这样一套完整的服务时，他就不得不关注这些底层的 Kubernetes 概念，这对用户非常不友好。

我们知道，几乎每个操作系统都内置了一套软件包管理器，用来方便用户安装、配置、卸载或升级各种系统软件和应用软件，比如 Debian 和 Ubuntu 使用的是 DEB 包管理器 `dpkg` 和 `apt`，CentOS 使用的是 RPM 包管理器 `yum`，Mac OS 有 `Homebrew`，Windows 有 `WinGet` 和 `Chocolatey` 等，另外很多系统还内置了图形界面的应用市场方便用户安装应用，比如 Windows 应用商店、Apple Store、安卓应用市场等，这些都可以算作是包管理器。

使用包管理器安装应用大大降低了用户的使用门槛，他只需要执行一句命令或点击一个安装按钮即可，而不用去关心这个应用需要哪些依赖和哪些配置。那么在 Kubernetes 下能不能也通过这种方式来部署应用服务呢？[Helm](https://helm.sh/zh/) 作为 Kubernetes 的包管理器，解决了这个问题。

## Helm 简介



https://helm.sh/zh/docs/community/history/

## 快速开始

### 安装 Helm

### 使用 Helm

## 制作自己的 Helm Chart

## 参考

1. [Helm | 快速入门指南](https://helm.sh/zh/docs/intro/quickstart/)
1. [Helm | 项目历史](https://helm.sh/zh/docs/community/history/)
1. [Helm Dashboard](https://github.com/komodorio/helm-dashboard)
1. [Kubernetes Tutorials ｜ k8s 教程](https://github.com/guangzhengli/k8s-tutorials#helm)

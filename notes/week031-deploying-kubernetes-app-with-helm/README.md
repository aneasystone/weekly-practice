# WEEK031 - 使用 Helm 部署 Kubernetes 应用

在 [week013-playing-with-kubernetes](../week013-playing-with-kubernetes/README.md) 中我们学习了如何通过 `Deployment` 部署一个简单的应用服务并通过 `Service` 来暴露它，在真实的场景中，一套完整的应用服务可能还会包含很多其他的 Kubernetes 资源，比如 `DaemonSet`、`Ingress`、`ConfigMap`、`Secret` 等，当用户部署这样一套完整的服务时，他就不得不关注这些底层的 Kubernetes 概念，这对用户非常不友好。

我们知道，几乎每个操作系统都内置了一套软件包管理器，用来方便用户安装、配置、卸载或升级各种系统软件和应用软件，比如 Debian 和 Ubuntu 使用的是 DEB 包管理器 `dpkg` 和 `apt`，CentOS 使用的是 RPM 包管理器 `yum`，Mac OS 有 `Homebrew`，Windows 有 `WinGet` 和 `Chocolatey` 等，另外很多系统还内置了图形界面的应用市场方便用户安装应用，比如 Windows 应用商店、Apple Store、安卓应用市场等，这些都可以算作是包管理器。

使用包管理器安装应用大大降低了用户的使用门槛，他只需要执行一句命令或点击一个安装按钮即可，而不用去关心这个应用需要哪些依赖和哪些配置。那么在 Kubernetes 下能不能也通过这种方式来部署应用服务呢？[Helm](https://helm.sh/zh/) 作为 Kubernetes 的包管理器，解决了这个问题。

## Helm 简介

Helm 是 [Deis 团队](https://deislabs.io/) 于 2015 年发布的一个 Kubernetes 包管理工具，当时 Deis 团队还没有被微软收购，他们在一家名为 Engine Yard 的公司里从事 PaaS 产品 Deis Workflow 的开发，在开发过程中，他们需要将众多的微服务部署到 Kubernetes 集群中，由于在 Kubernetes 里部署服务需要开发者手动编写和维护数量繁多的 Yaml 文件，并且服务的分发和安装也比较繁琐，Matt Butcher 和另外几个同事于是在一次 Hackthon 团建中发起了 Helm 项目。

> Helm 的取名非常有意思，Kubernetes 是希腊语 “舵手” 的意思，而 Helm 是舵手操作的 “船舵”，用来控制船的航行方向。

Helm 引入了 [Chart](https://helm.sh/zh/docs/topics/charts/) 的概念，它也是 Helm 所使用的包格式，可以把它理解成一个描述 Kubernetes 相关资源的文件集合。开发者将自己的应用配置文件打包成 Helm chart 格式，然后发布到 [ArtifactHub](https://artifacthub.io/)，这和你使用 `docker push` 将镜像推送到 DockerHub 镜像仓库一样，之后用户安装你的 Kubernetes 应用只需要一条简单的 Helm 命令就能搞定，极大程度上解决了 Kubernetes 应用维护、分发、安装等问题。

Helm 在 2018 年 6 月加入 CNCF，并在 2020 年 4 月正式毕业，目前已经是 Kubernetes 生态里面不可或缺的明星级项目。

## 快速开始

### 安装 Helm

### 使用 Helm

## 制作自己的 Helm Chart

## 参考

1. [Helm | 快速入门指南](https://helm.sh/zh/docs/intro/quickstart/)
1. [Helm | 项目历史](https://helm.sh/zh/docs/community/history/)
1. [微软 Deis Labs 的传奇故事](https://zhuanlan.zhihu.com/p/496603933)
1. [Helm Dashboard](https://github.com/komodorio/helm-dashboard)
1. [Kubernetes Tutorials ｜ k8s 教程](https://github.com/guangzhengli/k8s-tutorials#helm)

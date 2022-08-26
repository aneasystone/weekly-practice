# WEEK020 - 写一个简单的 Kubernetes Operator

[Kubernetes Operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) 这一概念是由 CoreOS 的工程师于 2016 年提出的，它是一种通过 [自定义资源](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)（`custom resource`、`CR`）来包装、运行和管理 Kubernetes 应用的方式。Kubernetes 1.7 版本以来就引入了自定义资源的概念，该功能可以让开发人员扩展新功能或更新现有功能，并且可以自动执行一些管理任务，这些自定义资源就像 Kubernetes 的原生组件一样。

通过自定义资源，我们可以将应用抽象为一个整体，而不用去关心该应用是由哪些 Kubernetes 原生组件构成的，什么 Pods、Deployments、Services 或 ConfigMaps 统统交给 Operator 来管理。创建 Operator 的关键是自定义资源的设计，通过直接调用 Kubernetes API，编写自定义规则自动管理和维护 Kubernetes 集群中的应用，包括自动化安装、配置、更新、故障转移、备份恢复等等。这样的应用也被称为 Kubernetes 原生应用（`Kubernetes-native application`）。Operator 可以帮我们实现下面这些功能：

![](./images/operator-capabilitiy-model.png)

这个图也被称为 [Operator 的能力模型](https://operatorframework.io/operator-capabilities/)，将 Operator 的能力由低到高分成了 5 个等级。

## 控制器循环

Kubernetes Operator 遵循 [control loop](https://kubernetes.io/docs/concepts/architecture/controller/) 原则，这是 Kubernetes 的核心原则之一，也是机器人和自动化领域中一种常见的持续运行动态系统的机制。它依赖于一种快速调整工作负载需求的能力，进而能够尽可能准确地适应现有资源。

![](./images/reconciliation-loop.png)

在 Kubernetes 中，这个循环被称为 `reconciliation loop`。在这个循环中，有一个非常重要的角色：`控制器`（Controller），它可以对集群的变化做出响应，并执行相应的动作。控制器首先观察 Kubernetes 对象的当前状态，然后通过 Kubernetes API 进行持续调整，直到将对象的当前状态变成所需状态为止。

第一个 Kubernetes Controller 是 `kube-controller-manager`，它被认为是所有 Operator 的鼻祖。

## Operator Framework

[Operator Framework](https://operatorframework.io/) 是 CoreOS 开源的一个用于快速开发或管理 Operator 的工具包，主要分为三大部分：

* [Operator SDK](https://sdk.operatorframework.io/)：`Build, test, iterate.` 你无需了解复杂的 Kubernetes API 特性，就可以根据你自己的专业知识构建一个 Operator 应用。
* [Operator Lifecycle Manager](https://olm.operatorframework.io/)：`install, manage, update.` OLM 是一款帮助你安装、更新和管理 Kubernetes Operator 的工具。
* [OperatorHub.io](http://operatorhub.io/)：`Publish & share.` OperatorHub 是一个类似 DockerHub 的仓库，你可以在这里搜索你想要的 Operator，或者将你的 Operator 发布并分享给其他人。

通过 Operator SDK 我们可以快速开发一个 Kubernetes Operator，它不仅提供了一套 High level API 来方便我们处理业务逻辑，还提供了一个命令行工具用于快速生成一个 Operator 的脚手架项目。

### 安装 `operator-sdk`

在开发 Operator 之前，先确保你已经有一个能访问的 Kubernetes 集群环境，Kubernetes 的安装可以参考 [week010-install-kubernetes](../week010-install-kubernetes/README.md)。查看 Kubernetes 集群信息：

```
$ kubectl cluster-info
Kubernetes control plane is running at https://kubernetes.docker.internal:6443
CoreDNS is running at https://kubernetes.docker.internal:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

另外，Go 的开发环境也是必不可少的，可以参考 Go 的 [官方文档](https://go.dev/doc/install) 下载并安装。

```
$ curl -LO https://go.dev/dl/go1.19.linux-amd64.tar.gz
$ sudo tar -C /usr/local -xzf go1.19.linux-amd64.tar.gz
```

将路径 `/usr/local/go/bin` 添加到 `PATH` 环境变量，或者将下面这行添加到 ` ~/.profile` 文件中：

```
$ export PATH=$PATH:/usr/local/go/bin
```

查看 Go 版本：

```
$ go version
go version go1.19 linux/amd64
```

接下来，我们继续安装 Operator SDK。我们在 Operator SDK 的 [Releases 页面](https://github.com/operator-framework/operator-sdk/releases) 找到合适的版本并下载：

```
$ curl -LO https://github.com/operator-framework/operator-sdk/releases/download/v1.23.0/operator-sdk_linux_amd64
```

将其移动到 `/usr/local/bin/` 目录即可完成安装：

```
$ chmod +x operator-sdk_linux_amd64 && sudo mv operator-sdk_linux_amd64 /usr/local/bin/operator-sdk
```

查看已安装的 `operator-sdk` 版本：

```
$ operator-sdk version
operator-sdk version: "v1.23.0", commit: "1eaeb5adb56be05fe8cc6dd70517e441696846a4", kubernetes version: "1.24.2", go version: "go1.18.5", GOOS: "linux", GOARCH: "amd64"
```

### 使用 `operator-sdk` 初始化 Operator 项目

Operator SDK 提供了三种方式开发 Operator：

* [Ansible](https://sdk.operatorframework.io/docs/building-operators/ansible/quickstart/)
* [Helm](https://sdk.operatorframework.io/docs/building-operators/helm/quickstart/)
* [Go](https://sdk.operatorframework.io/docs/building-operators/golang/quickstart/)

我们这里将使用 Go 来开发 Operator，这种方式也是最灵活的，你可以使用 client-go 调用 Kubernetes API 来对 Kubernetes 对象进行操作。首先使用 `operator-sdk init` 初始化项目结构：

```
$ operator-sdk init --domain example.com --project-name memcached-operator --repo github.com/example/memcached-operator
Writing kustomize manifests for you to edit...
Writing scaffold for you to edit...
Get controller runtime:
$ go get sigs.k8s.io/controller-runtime@v0.12.2
Update dependencies:
$ go mod tidy
Next: define a resource with:
$ operator-sdk create api
```

其中 `--project-name` 参数可以省略，默认项目名称就是目录名。`--domain` 和 `--project-name` 两个参数用于组成 Operator 的镜像名称 `example.com/memcached-operator`，而 `--repo` 参数用于定义 Go 模块名：

```
module github.com/example/memcached-operator
```

初始化后的完整项目结构如下：

```
$ tree .
.
├── Dockerfile
├── Makefile
├── PROJECT
├── README.md
├── config
│   ├── default
│   │   ├── kustomization.yaml
│   │   ├── manager_auth_proxy_patch.yaml
│   │   └── manager_config_patch.yaml
│   ├── manager
│   │   ├── controller_manager_config.yaml
│   │   ├── kustomization.yaml
│   │   └── manager.yaml
│   ├── manifests
│   │   └── kustomization.yaml
│   ├── prometheus
│   │   ├── kustomization.yaml
│   │   └── monitor.yaml
│   ├── rbac
│   │   ├── auth_proxy_client_clusterrole.yaml
│   │   ├── auth_proxy_role.yaml
│   │   ├── auth_proxy_role_binding.yaml
│   │   ├── auth_proxy_service.yaml
│   │   ├── kustomization.yaml
│   │   ├── leader_election_role.yaml
│   │   ├── leader_election_role_binding.yaml
│   │   ├── role_binding.yaml
│   │   └── service_account.yaml
│   └── scorecard
│       ├── bases
│       │   └── config.yaml
│       ├── kustomization.yaml
│       └── patches
│           ├── basic.config.yaml
│           └── olm.config.yaml
├── go.mod
├── go.sum
├── hack
│   └── boilerplate.go.txt
└── main.go
```

主要包括以下几个文件：

* `go.mod` - 用于定义 Go 项目的依赖信息
* `PROJECT` - 用于保存项目的配置信息
* `Makefile` - 包含一些有用的项目构建目标（*make targets*）
* `config` - 该目录下包含一些用于项目部署的 YAML 文件
* `main.go` - Operator 的主程序入口

### 开发 Operator 工作流

Operator SDK 提供以下工作流来开发一个新的 Operator：

1. 使用 SDK 创建一个新的 Operator 项目
2. 通过添加自定义资源（CRD）定义新的资源 API
3. 指定使用 SDK API 来 watch 的资源
4. 定义 Operator 的协调（reconcile）逻辑
5. 使用 Operator SDK 构建并生成 Operator 部署清单文件

## 参考

1. [Kubernetes 文档 / 概念 / 扩展 Kubernetes / Operator 模式](https://kubernetes.io/zh-cn/docs/concepts/extend-kubernetes/operator/)
1. [Kubernetes Operator 基础入门](https://www.infoq.cn/article/3jrwfyszlu6jatbdrtov)
1. [Kubernetes Operator 快速入门教程](https://www.qikqiak.com/post/k8s-operator-101/)
1. [What is a Kubernetes operator?](https://www.redhat.com/en/topics/containers/what-is-a-kubernetes-operator)
1. [Kubernetes Operators 101, Part 1: Overview and key features](https://developers.redhat.com/articles/2021/06/11/kubernetes-operators-101-part-1-overview-and-key-features)
1. [Kubernetes Operators 101, Part 2: How operators work](https://developers.redhat.com/articles/2021/06/22/kubernetes-operators-101-part-2-how-operators-work)
1. [kubernetes-sigs/kubebuilder](https://github.com/kubernetes-sigs/kubebuilder) - SDK for building Kubernetes APIs using CRDs

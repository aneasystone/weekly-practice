# WEEK010 - Kubernetes 安装小记

Kubernetes 集群环境的安装比较复杂，需要考虑网络、存储等一系列的问题，在这篇笔记中，我们先学习使用 kind 或 minikube 安装单机环境，在对 Kubernetes 的组件和基本概念有一定认识之后，再尝试部署集群环境。

## 安装 kubectl 

在安装 Kubernetes 之前，我们首先需要安装 `kubectl`，这是 Kubernetes 的命令行工具，用来在 Kubernetes 集群上运行命令，你可以使用 `kubectl` 来部署应用、监测和管理集群资源以及查看日志。安装 `kubectl` 最简单的方式是使用 curl 命令，首先执行下面的命令下载 `kubectl`：

```
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

然后将 `kubectl` 安装到 `/usr/local/bin` 目录：

```
$ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

`install` 和 `cp` 命令类似，都可以将文件或目录拷贝到指定的地方，不过 `install` 允许你控制文件的属性。`-o, --owner` 参数用来设置所有者，`-g, --group` 参数用来设置组，`-m, --mode` 类似于 chmod 的设定文件权限模式。

安装完成后，运行 `kubectl version` 查看版本的详细信息：

```
[root@localhost ~]# kubectl version --client --output=json
{
  "clientVersion": {
    "major": "1",
    "minor": "24",
    "gitVersion": "v1.24.0",
    "gitCommit": "4ce5a8954017644c5420bae81d72b09b735c21f0",
    "gitTreeState": "clean",
    "buildDate": "2022-05-03T13:46:05Z",
    "goVersion": "go1.18.1",
    "compiler": "gc",
    "platform": "linux/amd64"
  },
  "kustomizeVersion": "v4.5.4"
}
```

## 使用 kind 安装 Kubernetes

https://kind.sigs.k8s.io/docs/user/quick-start/

## 使用 minikube 安装 Kubernetes

https://minikube.sigs.k8s.io/docs/start/

## 使用 kubeadm 安装 Kubernetes

https://kubernetes.io/zh/docs/setup/production-environment/tools/kubeadm/install-kubeadm/

## 使用 sealos 安装 Kubernetes

https://github.com/labring/sealos

## 参考

1. [Kubernetes Documentation / Tasks / Install Tools](https://kubernetes.io/docs/tasks/tools/)
1. [Kubernetes Documentation / Reference / Command line tool (kubectl)](https://kubernetes.io/docs/reference/kubectl/)

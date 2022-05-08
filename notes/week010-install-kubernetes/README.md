# WEEK010 - Kubernetes 安装小记

Kubernetes 集群环境的安装比较复杂，需要考虑网络、存储等一系列的问题，在这篇笔记中，我们先学习使用 kind 或 minikube 安装单机环境，在对 Kubernetes 的组件和基本概念有一定认识之后，再尝试部署集群环境。

## 安装 kubectl 

在安装 Kubernetes 之前，我们首先需要安装 `kubectl`，这是 Kubernetes 的命令行工具，用来在 Kubernetes 集群上运行命令，你可以使用 `kubectl` 来部署应用、监测和管理集群资源以及查看日志。安装 `kubectl` 最简单的方式是使用 `curl` 命令，首先执行下面的命令下载 `kubectl`：

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

由于此时还没有安装 Kubernetes，所以使用 `--client` 仅显示客户端的版本。

## 使用 kind 安装 Kubernetes

[`kind`](https://kind.sigs.k8s.io/) 是 Kubernetes IN Docker 的简写，是一个使用 Docker 容器作为 Nodes，在本地创建和运行 Kubernetes 集群的工具。适用于在本机创建 Kubernetes 集群环境进行开发和测试。

### 安装 kind

和安装 `kubectl` 类似，首先使用 `curl` 下载：

```
$ curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.12.0/kind-linux-amd64
```

再使用 `install` 安装：

```
$ sudo install -o root -g root -m 0755 kind /usr/local/bin/kind
```

使用 `kind --help` 查看帮助：

```
[root@localhost ~]# kind --help
kind creates and manages local Kubernetes clusters using Docker container 'nodes'

Usage:
  kind [command]

Available Commands:
  build       Build one of [node-image]
  completion  Output shell completion code for the specified shell (bash, zsh or fish)
  create      Creates one of [cluster]
  delete      Deletes one of [cluster]
  export      Exports one of [kubeconfig, logs]
  get         Gets one of [clusters, nodes, kubeconfig]
  help        Help about any command
  load        Loads images into nodes
  version     Prints the kind CLI version

Flags:
  -h, --help              help for kind
      --loglevel string   DEPRECATED: see -v instead
  -q, --quiet             silence all stderr output
  -v, --verbosity int32   info log verbosity, higher value produces more output
      --version           version for kind

Use "kind [command] --help" for more information about a command.
```

### 创建 Kubernetes 集群

使用简单的一句命令 `kind create cluster` 就可以在本地创建一整套 Kubernetes 集群，这样的环境用于实验再合适不过：

```
[root@localhost ~]# kind create cluster
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.23.4) 🖼 
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Thanks for using kind! 😊
```

此时再运行 `kubectl version` 命令，就可以看到 Kubernetes 服务端的信息了：

```
[root@localhost ~]# kubectl version --output=json
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
  "kustomizeVersion": "v4.5.4",
  "serverVersion": {
    "major": "1",
    "minor": "23",
    "gitVersion": "v1.23.4",
    "gitCommit": "e6c093d87ea4cbb530a7b2ae91e54c0842d8308a",
    "gitTreeState": "clean",
    "buildDate": "2022-03-06T21:32:53Z",
    "goVersion": "go1.17.7",
    "compiler": "gc",
    "platform": "linux/amd64"
  }
}
```

使用 `docker ps` 可以看到一个名为 `kind-control-plane` 的容器，他暴露出来的端口 `127.0.0.1:45332` 就是我们 `kubectl` 访问的端口。

```
[root@localhost ~]# docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED       STATUS       PORTS                       NAMES
2d2f2ed13eaa   kindest/node:v1.23.4   "/usr/local/bin/entr…"   2 hours ago   Up 2 hours   127.0.0.1:45332->6443/tcp   kind-control-plane
```

`kind` 将整个 Kubernetes 组件内置在 `kindest/node` 镜像中，可以使用该镜像创建多个 Kubernetes 集群。默认创建的集群名为 `kind`，也可以使用 `--name` 参数指定集群名：

```
[root@localhost ~]# kind create cluster --name kind-2
```

获取集群列表：

```
[root@localhost ~]# kind get clusters
kind
kind2
```

使用 `kubectl cluster-info` 切换集群：

```
kubectl cluster-info --context kind-kind
kubectl cluster-info --context kind-kind-2
```

我们使用 `docker exec` 进入容器内部看看：

```
[root@localhost ~]# docker exec -it 2d2 bash
root@kind-control-plane:/# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.1  16544  1084 ?        Ss   09:43   0:00 /sbin/init
root         192  0.0  0.1  19448  1504 ?        S<s  09:44   0:00 /lib/systemd/systemd-journald
root         204  3.3  2.2 1437696 23204 ?       Ssl  09:44   4:09 /usr/local/bin/containerd
root         310  0.0  0.3 713276  3600 ?        Sl   09:44   0:02 /usr/local/bin/containerd-shim-runc-v2 -namespace k8s.io -id 6e308f31e4045e7f5e3f8ab7
root         317  0.0  0.3 713276  3428 ?        Sl   09:44   0:01 /usr/local/bin/containerd-shim-runc-v2 -namespace k8s.io -id 9de51bcebdf67ce484709b90
root         351  0.0  0.3 713276  3432 ?        Sl   09:44   0:02 /usr/local/bin/containerd-shim-runc-v2 -namespace k8s.io -id b0094313aab3af65958f7a74
root         363  0.0  0.4 713276  4060 ?        Sl   09:44   0:01 /usr/local/bin/containerd-shim-runc-v2 -namespace k8s.io -id 12136290af44076c5b5faa19
root         483  3.1  4.1 11214772 41872 ?      Ssl  09:44   3:56 etcd --advertise-client-urls=https://172.18.0.2:2379 --cert-file=/etc/kubernetes/pki/
root         562  6.5 18.7 1056224 190292 ?      Ssl  09:44   8:08 kube-apiserver --advertise-address=172.18.0.2 --allow-privileged=true --authorization
root         651  3.1  4.3 1402784 44492 ?       Ssl  09:44   3:55 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kube
root         899  0.0  0.3 713276  3284 ?        Sl   09:46   0:01 /usr/local/bin/containerd-shim-runc-v2 -namespace k8s.io -id 383bf2636b6a0b1e14b8cd08
root         915  0.0  0.3 713020  3596 ?        Sl   09:46   0:01 /usr/local/bin/containerd-shim-runc-v2 -namespace k8s.io -id b0fc9bc1eaf15846855b4e5e
root         983  0.0  0.7 733188  7908 ?        Ssl  09:46   0:04 /bin/kindnetd
root        1023  0.0  1.0 748152 11136 ?        Ssl  09:46   0:04 /usr/local/bin/kube-proxy --config=/var/lib/kube-proxy/config.conf --hostname-overrid
root        1234  2.9  4.1 767820 42316 ?        Ssl  09:47   3:34 kube-controller-manager --allocate-node-cidrs=true --authentication-kubeconfig=/etc/k
root        1274  0.4  1.9 754000 19516 ?        Ssl  09:47   0:34 kube-scheduler --authentication-kubeconfig=/etc/kubernetes/scheduler.conf --authoriza
root        1367  0.0  0.3 713020  3772 ?        Sl   09:47   0:01 /usr/local/bin/containerd-shim-runc-v2 -namespace k8s.io -id dc694d8f939cfec4277911fe
root        1371  0.0  0.4 713276  4848 ?        Sl   09:47   0:01 /usr/local/bin/containerd-shim-runc-v2 -namespace k8s.io -id 41b361804234b5c0fc353ff6
root        1393  0.0  0.3 713276  4044 ?        Sl   09:47   0:01 /usr/local/bin/containerd-shim-runc-v2 -namespace k8s.io -id e4befc1237963effcb2a594b
root        1499  0.1  1.1 750568 11884 ?        Ssl  09:47   0:12 /coredns -conf /etc/coredns/Corefile
root        1526  0.1  1.1 750568 11772 ?        Ssl  09:47   0:13 /coredns -conf /etc/coredns/Corefile
root        2904  0.2  0.1   4580  1040 pts/1    Ss   11:47   0:00 bash
root        2980  0.6  0.6 136664  6392 ?        Ssl  11:48   0:00 local-path-provisioner --debug start --helper-image k8s.gcr.io/build-image/debian-bas
root        3010  0.0  0.1   6900  1420 pts/1    R+   11:48   0:00 ps aux
```

可以看到这些进程：

* kindnetd - *一款简单的 CNI 插件*
* containerd - *使用 containerd 作为容器运行时，弃用 Dockershim 对 kind 没有影响*
* containerd-shim-runc-v2
* coredns - *为集群提供 DNS 和服务发现的功能*
* etcd - *服务发现的后端，并存储集群状态和配置*
* kubelet - *运行在每个节点上的代理，用来处理 Master 节点下发到本节点的任务*
* kube-apiserver - *提供集群管理的 REST API 接口，是模块之间的数据交互和通信的枢纽，只有 apiserver 能访问 etcd*
* kube-proxy - *实现 Kubernetes Service 的通信与负载均衡*
* kube-controller-manager - *是 Kubernetes 的大脑，它通过 apiserver 监控整个集群的状态，并确保集群处于预期的工作状态*
* kube-scheduler - *负责分配调度 Pod 到集群内的节点上，它监听 apiserver，查询还未分配 Node 的 Pod，然后根据调度策略为这些 Pod 分配节点*
* local-path-provisioner - *本地持久化存储*

## 使用 minikube 安装 Kubernetes

https://minikube.sigs.k8s.io/docs/start/

## 使用 kubeadm 安装 Kubernetes

https://kubernetes.io/zh/docs/setup/production-environment/tools/kubeadm/install-kubeadm/

## 使用 sealos 安装 Kubernetes

https://github.com/labring/sealos

## 参考

1. [kubectl 安装文档](https://kubernetes.io/docs/reference/kubectl/)
1. [kind 官网文档](https://kind.sigs.k8s.io/docs/user/quick-start/)
1. [kind：Kubernetes in Docker，单机运行 Kubernetes 群集的最佳方案](https://sysin.org/blog/kind/)

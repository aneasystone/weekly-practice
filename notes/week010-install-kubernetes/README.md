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
 ✓ Starting control-plane 🕹️
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
* pause
* coredns - *为集群提供 DNS 和服务发现的功能*
* etcd - *服务发现的后端，并存储集群状态和配置*
* kubelet - *运行在每个节点上的代理，用来处理 Master 节点下发到本节点的任务*
* kube-apiserver - *提供集群管理的 REST API 接口，是模块之间的数据交互和通信的枢纽，只有 apiserver 能访问 etcd*
* kube-proxy - *实现 Kubernetes Service 的通信与负载均衡*
* kube-controller-manager - *是 Kubernetes 的大脑，它通过 apiserver 监控整个集群的状态，并确保集群处于预期的工作状态*
* kube-scheduler - *负责分配调度 Pod 到集群内的节点上，它监听 apiserver，查询还未分配 Node 的 Pod，然后根据调度策略为这些 Pod 分配节点*
* local-path-provisioner - *本地持久化存储*

## 使用 minikube 安装 Kubernetes

[minikube](https://minikube.sigs.k8s.io/docs/) 是由 Google 发布的一款轻量级工具，让开发者可以在本机上轻易运行一个 Kubernetes 集群，快速上手 Kubernetes 的指令与环境。`minikube` 会在本机运行一个容器或虚拟机，并且在这个容器或虚拟机中启动一个 single-node Kubernetes 集群，它不支持 HA，不推荐在生产环境使用。

### 安装 minikube

`minikube` 的安装也和上面的 `kind` 和 `kubectl` 一样，先使用 `curl` 下载：

```
$ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
```

再通过 `install` 将其安装到 `/usr/local/bin` 目录：

```
$ sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### 创建 Kubernetes 集群

使用 `minikube` 创建 Kubernetes 集群比 `kind` 稍微多一些限制：

* 2 CPUs or more
* 2GB of free memory
* 20GB of free disk space

否则会报下面这些错误。

CPU 核数不够：

```
X Exiting due to RSRC_INSUFFICIENT_CORES: Requested cpu count 2 is greater than the available cpus of 1
```

内存不够：

```
X Exiting due to RSRC_INSUFFICIENT_CONTAINER_MEMORY: docker only has 990MiB available, less than the required 1800MiB for Kubernetes
```

另外，当我们使用 Docker 作为驱动时，需要以非 root 用户运行：

```
X Exiting due to DRV_AS_ROOT: The "docker" driver should not be used with root privileges.
```

Docker 在安装时会默认创建一个叫 `docker` 的用户组，可以在 `/etc/group` 文件中找到 `docker` 用户组的 id，然后使用 `adduser` 在该用户组下添加一个 `docker` 用户，`su - docker` 切换到 `docker` 用户就可以以非 root 用户运行 Docker 了：

```
[root@localhost ~]# grep docker /etc/group
docker:x:995:

[root@localhost ~]# adduser -g 995 -c "Docker" docker

[root@localhost ~]# id docker
uid=1000(docker) gid=995(docker) 组=995(docker)

[root@localhost ~]# su - docker
```

一切准备就绪，执行 `minikube start` 创建 Kubernetes 集群：

```
[docker@localhost ~]$ minikube start
* Centos 7.9.2009 上的 minikube v1.25.2
* 根据现有的配置文件使用 docker 驱动程序
* Starting control plane node minikube in cluster minikube
* Pulling base image ...
    > index.docker.io/kicbase/sta...: 0 B [____________________] ?% ? p/s 6m29s
! minikube was unable to download gcr.io/k8s-minikube/kicbase:v0.0.30, but successfully downloaded docker.io/kicbase/stable:v0.0.30 as a fallback image
* Creating docker container (CPUs=2, Memory=2200MB) ...

X Docker is nearly out of disk space, which may cause deployments to fail! (90% of capacity)
* 建议：

    Try one or more of the following to free up space on the device:
    
    1. Run "docker system prune" to remove unused Docker data (optionally with "-a")
    2. Increase the storage allocated to Docker for Desktop by clicking on:
    Docker icon > Preferences > Resources > Disk Image Size
    3. Run "minikube ssh -- docker system prune" if using the Docker container runtime
* Related issue: https://github.com/kubernetes/minikube/issues/9024

! This container is having trouble accessing https://k8s.gcr.io
* To pull new external images, you may need to configure a proxy: https://minikube.sigs.k8s.io/docs/reference/networking/proxy/
* 正在 Docker 20.10.12 中准备 Kubernetes v1.23.3…
  - kubelet.housekeeping-interval=5m
  - Generating certificates and keys ...
  - Booting up control plane ...
  - Configuring RBAC rules ...
* Verifying Kubernetes components...
  - Using image gcr.io/k8s-minikube/storage-provisioner:v5
* Enabled addons: default-storageclass, storage-provisioner
* Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

使用 `docker ps` 可以看到 `minikube` 使用 `kicbase/stable` 镜像启动了一个容器，该容器暴露了以下几个端口：

* 49157->22
* 49156->2376
* 49155->5000
* 49154->8443
* 49153->32443

```
[docker@localhost ~]$ docker ps -a
CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS         PORTS                                                                                                                                  NAMES
d7e2ffaba188   kicbase/stable:v0.0.30   "/usr/local/bin/entr…"   2 minutes ago   Up 2 minutes   127.0.0.1:49157->22/tcp, 127.0.0.1:49156->2376/tcp, 127.0.0.1:49155->5000/tcp, 127.0.0.1:49154->8443/tcp, 127.0.0.1:49153->32443/tcp   minikube
```

我们进到容器内部看看：

```
[docker@localhost ~]$ docker exec -it minikube bash
root@minikube:/# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.7  0.2  21848  8112 ?        Ss   00:44   0:01 /sbin/init
root         178  0.3  0.1  29028  5956 ?        S<s  00:44   0:00 /lib/systemd/systemd-journald
message+     189  0.0  0.0   6992  2048 ?        Ss   00:44   0:00 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activ
root         194  0.9  0.9 1493012 36696 ?       Ssl  00:44   0:01 /usr/bin/containerd
root         201  0.0  0.1  12168  3888 ?        Ss   00:44   0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
root         445  2.6  1.9 1900036 74280 ?       Ssl  00:44   0:04 /usr/bin/dockerd -H tcp://0.0.0.0:2376 -H unix:///var/run/docker.sock --default-ulimi
root        1205  0.0  0.1 711432  6092 ?        Sl   00:44   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id d7248cb46ce6675cd8571237b2d97b14
root        1234  0.0  0.1 711432  5916 ?        Sl   00:44   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id c64eab39fcc84a16cf781946b19208a8
root        1235  0.0  0.1 711688  6052 ?        Sl   00:44   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 160d78a5a6af0460766ea18b52712194
root        1248  0.0  0.1 711432  5540 ?        Sl   00:44   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 60addc91e8a0ac5163c7aec249d4df17
root        1385  0.0  0.2 711176 10580 ?        Sl   00:44   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id dacd9db0524cde32c07b69922e85eb22
root        1386  0.0  0.1 712840  6084 ?        Sl   00:44   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 9d6e09b49fe389729643b4c000132fab
root        1426  0.0  0.1 712840  5892 ?        Sl   00:44   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id c72e327a1759494f99936930c846abda
root        1439  0.0  0.1 711176  5880 ?        Sl   00:44   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 8ffdf3f55725c550e703a3d9f3d0f5b3
root        1458  3.2  0.8 754020 32528 ?        Ssl  00:44   0:04 kube-scheduler --authentication-kubeconfig=/etc/kubernetes/scheduler.conf --authoriza
root        1477 14.6  8.0 1110392 312444 ?      Ssl  00:44   0:21 kube-apiserver --advertise-address=192.168.49.2 --allow-privileged=true --authorizati
root        1494  7.4  1.9 824644 76552 ?        Ssl  00:44   0:11 kube-controller-manager --allocate-node-cidrs=true --authentication-kubeconfig=/etc/k
root        1506 12.1  0.9 11214516 38160 ?      Ssl  00:44   0:17 etcd --advertise-client-urls=https://192.168.49.2:2379 --cert-file=/var/lib/minikube/
root        1733  5.2  1.8 1862712 71784 ?       Ssl  00:45   0:06 /var/lib/minikube/binaries/v1.23.3/kubelet --bootstrap-kubeconfig=/etc/kubernetes/boo
root        1999  0.0  0.1 711688  7116 ?        Sl   00:45   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 6bcfb5ef991c43859df52e82267a4ea2
root        2097  0.0  0.1 711432  5820 ?        Sl   00:45   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id acee309420d41df02c11a0c5b581527e
root        2142  0.0  0.1 711432  5676 ?        Sl   00:45   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 4c4d52d6bb2f9d2a1ca9f198c6d7e61f
root        2162  0.3  0.5 748424 21668 ?        Ssl  00:45   0:00 /usr/local/bin/kube-proxy --config=/var/lib/kube-proxy/config.conf --hostname-overrid
root        2195  0.0  0.1 710920  5932 ?        Sl   00:45   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id c1fcfbe957680299873562cfb7d3d8a3
root        2337  0.0  0.1 711688  5708 ?        Sl   00:45   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id d7dafa8e76578114f8aeaff1a4e6edd0
root        2357  0.5  0.6 750824 24468 ?        Ssl  00:45   0:00 /coredns -conf /etc/coredns/Corefile
root        2436  0.0  0.1 711432  5688 ?        Sl   00:45   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 7d3a10b807c67b41603e66b2a1527e4d
root        2457  1.4  0.4 735712 16776 ?        Ssl  00:45   0:01 /storage-provisioner
root        2673  1.0  0.0   4236  2232 pts/1    Ss   00:47   0:00 bash
root        2687  0.0  0.0   5888  1520 pts/1    R+   00:47   0:00 ps aux
```

可以看到下面这些进程和 `kind` 一样：

* containerd
* containerd-shim-runc-v2
* pause
* coredns
* etcd
* kubelet
* kube-apiserver
* kube-proxy
* kube-controller-manager
* kube-scheduler

下面这些进程不一样：

* dbus-daemon
* sshd
* dockerd
* storage-provisioner

少了这两个进程：

* kindnetd
* local-path-provisioner

## 使用 kubeadm 安装 Kubernetes

`kubeadm` 是 Kubernetes 社区提供的集群构建工具，它负责构建一个最小化可用集群并执行启动等必要的基本步骤，简单来讲，`kubeadm` 是 Kubernetes 集群全生命周期管理工具，可用于实现集群的部署、升级/降级及卸载等。按照设计，它只关注启动引导，而非配置机器。同样的，安装各种 “锦上添花” 的扩展，例如 Kubernetes Dashboard、监控方案、以及特定云平台的扩展，都不在讨论范围内。

### 安装 kubeadm、kubelet 和 kubectl

首先我们需要安装这三个组件：

* `kubeadm` - 用于启动集群
* `kubelet` - 运行在集群中的每一台机器上，用于启动 Pod 和 容器
* `kubectl` - 用于管理集群

虽然官方提供了 [yum 和 apt-get 的安装方式](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#installing-kubeadm-kubelet-and-kubectl)，但是这里我打算手工安装下，这样可以更好的加深理解。

#### 下载 CNI 插件

绝大多数 Pod 网络都需要 CNI 插件。

```
[root@localhost ~]# mkdir -p /opt/cni/bin
[root@localhost ~]# curl -L "https://github.com/containernetworking/plugins/releases/download/v0.8.2/cni-plugins-linux-amd64-v0.8.2.tgz" | sudo tar -C /opt/cni/bin -xz
```

可以看到这里提供了很多不同的 CNI 插件：

```
[root@localhost ~]# ls /opt/cni/bin/
bandwidth  bridge  dhcp  firewall  flannel  host-device  host-local  ipvlan  loopback  macvlan  portmap  ptp  sbr  static  tuning  vlan
```

#### 安装 crictl

`crictl` 是 `CRI` 兼容的容器运行时命令行接口。你可以使用它来检查和调试 Kubernetes 节点上的容器运行时和应用程序。

```
[root@localhost ~]# curl -L "https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.22.0/crictl-v1.22.0-linux-amd64.tar.gz" | sudo tar -C /usr/local/bin -xz
```

使用 `crictl --help` 查看帮助：

```
[root@localhost ~]# crictl --help
NAME:
   crictl - client for CRI

USAGE:
   crictl [global options] command [command options] [arguments...]

VERSION:
   v1.22.0

COMMANDS:
   attach              Attach to a running container
   create              Create a new container
   exec                Run a command in a running container
   version             Display runtime version information
   images, image, img  List images
   inspect             Display the status of one or more containers
   inspecti            Return the status of one or more images
   imagefsinfo         Return image filesystem info
   inspectp            Display the status of one or more pods
   logs                Fetch the logs of a container
   port-forward        Forward local port to a pod
   ps                  List containers
   pull                Pull an image from a registry
   run                 Run a new container inside a sandbox
   runp                Run a new pod
   rm                  Remove one or more containers
   rmi                 Remove one or more images
   rmp                 Remove one or more pods
   pods                List pods
   start               Start one or more created containers
   info                Display information of the container runtime
   stop                Stop one or more running containers
   stopp               Stop one or more running pods
   update              Update one or more running containers
   config              Get and set crictl client configuration options
   stats               List container(s) resource usage statistics
   completion          Output shell completion code
   help, h             Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --config value, -c value            Location of the client config file. If not specified and the default does not exist, the program's directory is searched as well (default: "/etc/crictl.yaml") [$CRI_CONFIG_FILE]
   --debug, -D                         Enable debug mode (default: false)
   --image-endpoint value, -i value    Endpoint of CRI image manager service (default: uses 'runtime-endpoint' setting) [$IMAGE_SERVICE_ENDPOINT]
   --runtime-endpoint value, -r value  Endpoint of CRI container runtime service (default: uses in order the first successful one of [unix:///var/run/dockershim.sock unix:///run/containerd/containerd.sock unix:///run/crio/crio.sock]). Default is now deprecated and the endpoint should be set instead. [$CONTAINER_RUNTIME_ENDPOINT]
   --timeout value, -t value           Timeout of connecting to the server in seconds (e.g. 2s, 20s.). 0 or less is set to default (default: 2s)
   --help, -h                          show help (default: false)
   --version, -v                       print the version (default: false)
```

不过在执行 `crictl ps` 的时候报错了：

```
[root@localhost ~]# crictl ps
WARN[0000] runtime connect using default endpoints: [unix:///var/run/dockershim.sock unix:///run/containerd/containerd.sock unix:///run/crio/crio.sock]. As the default settings are now deprecated, you should set the endpoint instead. 
ERRO[0002] connect endpoint 'unix:///var/run/dockershim.sock', make sure you are running as root and the endpoint has been started: context deadline exceeded 
WARN[0002] image connect using default endpoints: [unix:///var/run/dockershim.sock unix:///run/containerd/containerd.sock unix:///run/crio/crio.sock]. As the default settings are now deprecated, you should set the endpoint instead. 
ERRO[0004] connect endpoint 'unix:///var/run/dockershim.sock', make sure you are running as root and the endpoint has been started: context deadline exceeded 
FATA[0004] listing containers: rpc error: code = Unimplemented desc = unknown service runtime.v1alpha2.RuntimeService 
```

我们检查 containerd 的配置文件 `/etc/containerd/config.toml`：

```
[root@localhost ~]# cat /etc/containerd/config.toml
#   Copyright 2018-2020 Docker Inc.

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

disabled_plugins = ["cri"]

#root = "/var/lib/containerd"
#state = "/run/containerd"
#subreaper = true
#oom_score = 0

#[grpc]
#  address = "/run/containerd/containerd.sock"
#  uid = 0
#  gid = 0

#[debug]
#  address = "/run/containerd/debug.sock"
#  uid = 0
#  gid = 0
#  level = "info"
```

发现里面有一行 `disabled_plugins = ["cri"]`，这是 Docker 默认安装时的配置，我们将这个配置删除，并重启 containerd：

```
[root@localhost ~]# rm /etc/containerd/config.toml
[root@localhost ~]# systemctl restart containerd
```

#### 安装 kubeadm、kubelet 和 kubectl

```
[root@localhost ~]# cd /usr/local/bin
[root@localhost bin]# curl -L --remote-name-all https://storage.googleapis.com/kubernetes-release/release/v1.24.0/bin/linux/amd64/{kubeadm,kubelet,kubectl}
[root@localhost bin]# chmod +x {kubeadm,kubelet,kubectl}
```

这三个组件安装好之后，我们需要将 `kubelet` 添加到 systemd 服务。首先直接从官方下载服务定义的模板，修改其中 kubelet 的路径：

```
[root@localhost ~]# curl -sSL "https://raw.githubusercontent.com/kubernetes/release/v0.4.0/cmd/kubepkg/templates/latest/deb/kubelet/lib/systemd/system/kubelet.service" | sed "s:/usr/bin:/usr/local/bin:g" | tee /etc/systemd/system/kubelet.service

[Unit]
Description=kubelet: The Kubernetes Node Agent
Documentation=https://kubernetes.io/docs/home/
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=/usr/local/bin/kubelet
Restart=always
StartLimitInterval=0
RestartSec=10

[Install]
WantedBy=multi-user.target
```

然后再下载 kubeadm 的配置文件：

```
[root@localhost ~]# mkdir -p /etc/systemd/system/kubelet.service.d
[root@localhost ~]# curl -sSL "https://raw.githubusercontent.com/kubernetes/release/v0.4.0/cmd/kubepkg/templates/latest/deb/kubeadm/10-kubeadm.conf" | sed "s:/usr/bin:/usr/local/bin:g" | tee /etc/systemd/system/kubelet.service.d/10-kubeadm.conf

# Note: This dropin only works with kubeadm and kubelet v1.11+
[Service]
Environment="KUBELET_KUBECONFIG_ARGS=--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf"
Environment="KUBELET_CONFIG_ARGS=--config=/var/lib/kubelet/config.yaml"
# This is a file that "kubeadm init" and "kubeadm join" generates at runtime, populating the KUBELET_KUBEADM_ARGS variable dynamically
EnvironmentFile=-/var/lib/kubelet/kubeadm-flags.env
# This is a file that the user can use for overrides of the kubelet args as a last resort. Preferably, the user should use
# the .NodeRegistration.KubeletExtraArgs object in the configuration files instead. KUBELET_EXTRA_ARGS should be sourced from this file.
EnvironmentFile=-/etc/default/kubelet
ExecStart=
ExecStart=/usr/local/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS
```

最后，启动 `kubelet` 服务：

```
[root@localhost ~]# systemctl enable --now kubelet
Created symlink from /etc/systemd/system/multi-user.target.wants/kubelet.service to /etc/systemd/system/kubelet.service.
```

### 使用 kubeadm 创建 Kubernetes 集群

接下来我们使用 `kubeadm init` 来初始化 Kubernetes 集群，这个命令的作用是帮助你启动和 master 节点相关的组件：`kube-apiserver`、`kube-controller-manager`、`kube-scheduler` 和 `etcd` 等。在运行之前，我们可以使用 `kubeadm config images list` 命令查看使用 kubeadm 创建 Kubernetes 集群所需要的镜像：

```
[root@localhost ~]# kubeadm config images list
k8s.gcr.io/kube-apiserver:v1.24.0
k8s.gcr.io/kube-controller-manager:v1.24.0
k8s.gcr.io/kube-scheduler:v1.24.0
k8s.gcr.io/kube-proxy:v1.24.0
k8s.gcr.io/pause:3.7
k8s.gcr.io/etcd:3.5.3-0
k8s.gcr.io/coredns/coredns:v1.8.6
```

使用 `kubeadm config images pull` 提前将镜像下载下来：

```
[root@localhost ~]# kubeadm config images pull
failed to pull image "k8s.gcr.io/kube-apiserver:v1.24.0": output: time="2022-05-15T12:18:29+08:00" level=fatal msg="pulling image: rpc error: code = Unimplemented desc = unknown service runtime.v1alpha2.ImageService"
, error: exit status 1
To see the stack trace of this error execute with --v=5 or higher
```

我们发现下载镜像报错，这是因为国内没办法访问 `k8s.gcr.io`，而且无论是在环境变量中设置代理，还是为 Docker Daemon 设置代理，都不起作用。后来才意识到，`kubeadm config images pull` 命令貌似不走 docker 服务，而是直接请求 containerd 服务，所以我们为 containerd 服务设置代理：

```
[root@localhost ~]# mkdir /etc/systemd/system/containerd.service.d
[root@localhost ~]# vi /etc/systemd/system/containerd.service.d/http_proxy.conf
```

文件内容如下：

```
[Service]
Environment="HTTP_PROXY=192.168.1.36:10809"
Environment="HTTPS_PROXY=192.168.1.36:10809"
```

重启 containerd 服务：

```
[root@localhost ~]# systemctl daemon-reload
[root@localhost ~]# systemctl restart containerd
```

然后重新下载镜像：

```
[root@localhost ~]# kubeadm config images pull
[config/images] Pulled k8s.gcr.io/kube-apiserver:v1.24.0
[config/images] Pulled k8s.gcr.io/kube-controller-manager:v1.24.0
[config/images] Pulled k8s.gcr.io/kube-scheduler:v1.24.0
[config/images] Pulled k8s.gcr.io/kube-proxy:v1.24.0
[config/images] Pulled k8s.gcr.io/pause:3.7
[config/images] Pulled k8s.gcr.io/etcd:3.5.3-0
[config/images] Pulled k8s.gcr.io/coredns/coredns:v1.8.6
```

接下来使用 `kubeadm init` 初始化 Kubernetes 的控制平面：

```
[root@localhost ~]# kubeadm init
W0515 14:36:22.763487   21958 version.go:103] could not fetch a Kubernetes version from the internet: unable to get URL "https://dl.k8s.io/release/stable-1.txt": Get "https://dl.k8s.io/release/stable-1.txt": x509: certificate has expired or is not yet valid: current time 2022-05-15T14:36:22+08:00 is before 2022-05-17T21:21:32Z
W0515 14:36:22.763520   21958 version.go:104] falling back to the local client version: v1.24.0
[init] Using Kubernetes version: v1.24.0
[preflight] Running pre-flight checks
	[WARNING Firewalld]: firewalld is active, please ensure ports [6443 10250] are open or your cluster may not function correctly
	[WARNING Swap]: swap is enabled; production deployments should disable swap unless testing the NodeSwap feature gate of the kubelet
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
[preflight] You can also perform this action in beforehand using 'kubeadm config images pull'
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local localhost.localdomain] and IPs [10.96.0.1 10.0.2.10]
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [localhost localhost.localdomain] and IPs [10.0.2.10 127.0.0.1 ::1]
[certs] Generating "etcd/peer" certificate and key
[certs] etcd/peer serving cert is signed for DNS names [localhost localhost.localdomain] and IPs [10.0.2.10 127.0.0.1 ::1]
[certs] Generating "etcd/healthcheck-client" certificate and key
[certs] Generating "apiserver-etcd-client" certificate and key
[certs] Generating "sa" key and public key
[kubeconfig] Using kubeconfig folder "/etc/kubernetes"
[kubeconfig] Writing "admin.conf" kubeconfig file
[kubeconfig] Writing "kubelet.conf" kubeconfig file
[kubeconfig] Writing "controller-manager.conf" kubeconfig file
[kubeconfig] Writing "scheduler.conf" kubeconfig file
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Starting the kubelet
[control-plane] Using manifest folder "/etc/kubernetes/manifests"
[control-plane] Creating static Pod manifest for "kube-apiserver"
[control-plane] Creating static Pod manifest for "kube-controller-manager"
[control-plane] Creating static Pod manifest for "kube-scheduler"
[etcd] Creating static Pod manifest for local etcd in "/etc/kubernetes/manifests"
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests". This can take up to 4m0s
[kubelet-check] Initial timeout of 40s passed.
[kubelet-check] It seems like the kubelet isn't running or healthy.
[kubelet-check] The HTTP call equal to 'curl -sSL http://localhost:10248/healthz' failed with error: Get "http://localhost:10248/healthz": dial tcp [::1]:10248: connect: connection refused.
[kubelet-check] It seems like the kubelet isn't running or healthy.
[kubelet-check] The HTTP call equal to 'curl -sSL http://localhost:10248/healthz' failed with error: Get "http://localhost:10248/healthz": dial tcp [::1]:10248: connect: connection refused.
[kubelet-check] It seems like the kubelet isn't running or healthy.
[kubelet-check] The HTTP call equal to 'curl -sSL http://localhost:10248/healthz' failed with error: Get "http://localhost:10248/healthz": dial tcp [::1]:10248: connect: connection refused.
[kubelet-check] It seems like the kubelet isn't running or healthy.
[kubelet-check] The HTTP call equal to 'curl -sSL http://localhost:10248/healthz' failed with error: Get "http://localhost:10248/healthz": dial tcp [::1]:10248: connect: connection refused.
[kubelet-check] It seems like the kubelet isn't running or healthy.
[kubelet-check] The HTTP call equal to 'curl -sSL http://localhost:10248/healthz' failed with error: Get "http://localhost:10248/healthz": dial tcp [::1]:10248: connect: connection refused.

Unfortunately, an error has occurred:
	timed out waiting for the condition

This error is likely caused by:
	- The kubelet is not running
	- The kubelet is unhealthy due to a misconfiguration of the node in some way (required cgroups disabled)

If you are on a systemd-powered system, you can try to troubleshoot the error with the following commands:
	- 'systemctl status kubelet'
	- 'journalctl -xeu kubelet'

Additionally, a control plane component may have crashed or exited when started by the container runtime.
To troubleshoot, list all containers using your preferred container runtimes CLI.
Here is one example how you may list all running Kubernetes containers by using crictl:
	- 'crictl --runtime-endpoint unix:///var/run/containerd/containerd.sock ps -a | grep kube | grep -v pause'
	Once you have found the failing container, you can inspect its logs with:
	- 'crictl --runtime-endpoint unix:///var/run/containerd/containerd.sock logs CONTAINERID'
error execution phase wait-control-plane: couldn't initialize a Kubernetes cluster
To see the stack trace of this error execute with --v=5 or higher
```

根据报错信息，应该是 `swap` 的问题，通过下面的命令关闭 `swap`：

```
[root@localhost ~]# swapoff  -a
```

然后重新执行 `kubeadm init`，注意要先执行 `kubeadm reset`：

```
[root@localhost ~]# kubeadm reset
[reset] Reading configuration from the cluster...
[reset] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
W0515 15:03:11.771080   25796 reset.go:103] [reset] Unable to fetch the kubeadm-config ConfigMap from cluster: failed to get config map: Get "https://10.0.2.10:6443/api/v1/namespaces/kube-system/configmaps/kubeadm-config?timeout=10s": dial tcp 10.0.2.10:6443: connect: connection refused
W0515 15:03:11.773814   25796 preflight.go:55] [reset] WARNING: Changes made to this host by 'kubeadm init' or 'kubeadm join' will be reverted.
[reset] Are you sure you want to proceed? [y/N]: y
[preflight] Running pre-flight checks
W0515 15:03:13.272040   25796 removeetcdmember.go:84] [reset] No kubeadm config, using etcd pod spec to get data directory
[reset] Stopping the kubelet service
[reset] Unmounting mounted directories in "/var/lib/kubelet"
[reset] Deleting contents of directories: [/etc/kubernetes/manifests /etc/kubernetes/pki]
[reset] Deleting files: [/etc/kubernetes/admin.conf /etc/kubernetes/kubelet.conf /etc/kubernetes/bootstrap-kubelet.conf /etc/kubernetes/controller-manager.conf /etc/kubernetes/scheduler.conf]
[reset] Deleting contents of stateful directories: [/var/lib/etcd /var/lib/kubelet /var/lib/dockershim /var/run/kubernetes /var/lib/cni]

The reset process does not clean CNI configuration. To do so, you must remove /etc/cni/net.d

The reset process does not reset or clean up iptables rules or IPVS tables.
If you wish to reset iptables, you must do so manually by using the "iptables" command.

If your cluster was setup to utilize IPVS, run ipvsadm --clear (or similar)
to reset your system's IPVS tables.

The reset process does not clean your kubeconfig files and you must remove them manually.
Please, check the contents of the $HOME/.kube/config file.
```

再次执行 `kubeadm init` 成功：

```
[root@localhost ~]# kubeadm init
W0515 15:03:21.229843   25821 version.go:103] could not fetch a Kubernetes version from the internet: unable to get URL "https://dl.k8s.io/release/stable-1.txt": Get "https://dl.k8s.io/release/stable-1.txt": x509: certificate has expired or is not yet valid: current time 2022-05-15T15:03:21+08:00 is before 2022-05-17T21:21:32Z
W0515 15:03:21.229869   25821 version.go:104] falling back to the local client version: v1.24.0
[init] Using Kubernetes version: v1.24.0
[preflight] Running pre-flight checks
	[WARNING Firewalld]: firewalld is active, please ensure ports [6443 10250] are open or your cluster may not function correctly
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
[preflight] You can also perform this action in beforehand using 'kubeadm config images pull'
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local localhost.localdomain] and IPs [10.96.0.1 10.0.2.10]
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [localhost localhost.localdomain] and IPs [10.0.2.10 127.0.0.1 ::1]
[certs] Generating "etcd/peer" certificate and key
[certs] etcd/peer serving cert is signed for DNS names [localhost localhost.localdomain] and IPs [10.0.2.10 127.0.0.1 ::1]
[certs] Generating "etcd/healthcheck-client" certificate and key
[certs] Generating "apiserver-etcd-client" certificate and key
[certs] Generating "sa" key and public key
[kubeconfig] Using kubeconfig folder "/etc/kubernetes"
[kubeconfig] Writing "admin.conf" kubeconfig file
[kubeconfig] Writing "kubelet.conf" kubeconfig file
[kubeconfig] Writing "controller-manager.conf" kubeconfig file
[kubeconfig] Writing "scheduler.conf" kubeconfig file
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Starting the kubelet
[control-plane] Using manifest folder "/etc/kubernetes/manifests"
[control-plane] Creating static Pod manifest for "kube-apiserver"
[control-plane] Creating static Pod manifest for "kube-controller-manager"
[control-plane] Creating static Pod manifest for "kube-scheduler"
[etcd] Creating static Pod manifest for local etcd in "/etc/kubernetes/manifests"
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests". This can take up to 4m0s
[apiclient] All control plane components are healthy after 22.259518 seconds
[upload-config] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config" in namespace kube-system with the configuration for the kubelets in the cluster
[upload-certs] Skipping phase. Please see --upload-certs
[mark-control-plane] Marking the node localhost.localdomain as control-plane by adding the labels: [node-role.kubernetes.io/control-plane node.kubernetes.io/exclude-from-external-load-balancers]
[mark-control-plane] Marking the node localhost.localdomain as control-plane by adding the taints [node-role.kubernetes.io/master:NoSchedule node-role.kubernetes.io/control-plane:NoSchedule]
[bootstrap-token] Using token: cjpeqg.yvf2lka5i5epqcis
[bootstrap-token] Configuring bootstrap tokens, cluster-info ConfigMap, RBAC Roles
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to get nodes
[bootstrap-token] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstrap-token] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstrap-token] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstrap-token] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[kubelet-finalize] Updating "/etc/kubernetes/kubelet.conf" to point to a rotatable kubelet client certificate and key
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 10.0.2.10:6443 --token cjpeqg.yvf2lka5i5epqcis \
	--discovery-token-ca-cert-hash sha256:2c662bccbb9491d97b141a2b4b578867f240614ddcc399949c803d1f5093bba5 
```

根据提示，我们将配置文件复制到 `~/.kube` 目录：

```
[root@localhost ~]# mkdir -p $HOME/.kube
[root@localhost ~]# sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
[root@localhost ~]# sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

然后安装一个 [Pod 网络插件](https://kubernetes.io/docs/concepts/cluster-administration/addons/)，这里我们选择安装 `flannel`：

```
[root@localhost ~]# curl -LO https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml

[root@localhost ~]# kubectl apply -f kube-flannel.yml
Warning: policy/v1beta1 PodSecurityPolicy is deprecated in v1.21+, unavailable in v1.25+
podsecuritypolicy.policy/psp.flannel.unprivileged created
clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.apps/kube-flannel-ds created
```

然后在另一台机器上执行 `kubeadm join` 将工作节点加入 Kubernetes 集群（这台机器也需要提前安装好 kubeadm）：

```
[root@localhost ~]# kubeadm join 10.0.2.10:6443 --token cjpeqg.yvf2lka5i5epqcis \
	--discovery-token-ca-cert-hash sha256:2c662bccbb9491d97b141a2b4b578867f240614ddcc399949c803d1f5093bba5 
```

## 其他安装或管理 Kubernetes 的工具

* [Kubernetes Dashboard](https://github.com/kubernetes/dashboard)
* [sealos](https://github.com/labring/sealos)
* [Rancher](https://rancher.com/quick-start)
* [Kuboard](https://kuboard.cn/)
* [Kubernetes Web View](https://kube-web-view.readthedocs.io/en/latest/index.html)

## 参考

1. [kubectl 安装文档](https://kubernetes.io/docs/reference/kubectl/)
1. [kind 官方文档](https://kind.sigs.k8s.io/docs/user/quick-start/)
1. [kind：Kubernetes in Docker，单机运行 Kubernetes 群集的最佳方案](https://sysin.org/blog/kind/)
1. [minikube 官方文档](https://minikube.sigs.k8s.io/docs/start/)
1. [Bootstrapping clusters with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/)
1. [一文搞懂容器运行时 Containerd](https://www.qikqiak.com/post/containerd-usage/)

## 更多

### 1. 为 Docker 设置代理

第一种情况是 [为 Docker Daemon 设置代理](https://docs.docker.com/config/daemon/systemd/#httphttps-proxy)，影响 docker pull 下载镜像。首先创建如下目录：

```
[root@localhost ~]# mkdir -p /etc/systemd/system/docker.service.d
```

在该目录下创建文件 `http-proxy.conf`：

```
[root@localhost ~]# cd /etc/systemd/system/docker.service.d
[root@localhost docker.service.d]# vi http-proxy.conf
```

文件内容如下：

```
[Service]
Environment="HTTP_PROXY=192.168.1.36:10809"
Environment="HTTPS_PROXY=192.168.1.36:10809"
```

重启 Docker 服务：

```
[root@localhost ~]# systemctl daemon-reload
[root@localhost ~]# systemctl restart docker
```

验证代理设置是否生效：

```
[root@localhost ~]# systemctl show --property=Environment docker
Environment=HTTP_PROXY=192.168.1.36:10809 HTTPS_PROXY=192.168.1.36:10809
```

第二种情况是 [为 Docker 容器设置代理](https://docs.docker.com/network/proxy/)，影响容器内访问外部网络。这个配置比较简单，只需要在用户目录下创建一个 `~/.docker/config.json` 文件：

```
[root@localhost ~]# mkdir -p ~/.docker
[root@localhost ~]# vi ~/.docker/config.json
```

文件内容如下：

```
{
  "proxies":
  {
    "default":
    {
      "httpProxy": "192.168.1.36:10809",
      "httpsProxy": "192.168.1.36:10809"
    }
  }
}
```

使用 `alpine/curl` 镜像启动一个容器，验证配置是否生效：

```
[root@localhost ~]# docker run --rm alpine/curl -fsSL ifconfig.me
103.168.154.81
```

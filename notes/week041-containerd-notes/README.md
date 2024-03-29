# WEEK041 - 容器运行时 containerd 学习笔记

2016 年 12 月，Docker 公司宣布将 [containerd](https://containerd.io/) 项目从 Docker Engine 中分离出来，形成一个独立的开源项目，并捐赠给 CNCF 基金会，旨在打造一个符合工业标准的容器运行时。Docker 公司之所以做出这样的决定，是因为当时在容器编排的市场上 Docker 面临着 Kubernetes 的极大挑战，将 containerd 分离，是为了方便开展 Docker Swarm 项目，不过结果大家都知道，Docker Swarm 在 Kubernetes 面前以惨败收场。

containerd 并不是直接面向最终用户的，而是主要用于集成到更上层的系统里，比如 Docker Swarm、Kubernetes 或 Mesos 等容器编排系统。containerd 通过 unix domain docket 暴露很低层的 gRPC API，上层系统可以通过这些 API 对机器上的容器整个生命周期进行管理，包括镜像的拉取、容器的启动和停止、以及底层存储和网络的管理等。下面是 containerd 官方提供的架构图：

![](./images/containerd-architecture.png)

从上图可以看出，containerd 的核心主要由一堆的 [Services](https://github.com/containerd/containerd/tree/main/api/services) 组成，通过 Content Store、Snapshotter 和 Runtime 三大技术底座，实现了 Containers、Content、Images、Leases、Namespaces 和 Snapshots 等的管理。

其中 Runtime 部分和容器的关系最为紧密，可以看到 containerd 通过 containerd-shim 来支持多种不同的 OCI runtime，其中最为常用的 OCI runtime 就是 [runc](https://github.com/opencontainers/runc)，所以只要是符合 OCI 标准的容器，都可以由 containerd 进行管理，值得一提的是 runc 也是由 Docker 开源的。

> [OCI](https://opencontainers.org/) 的全称为 Open Container Initiative，也就是开放容器标准，主要致力于创建一套开放的容器格式和运行时行业标准，目前包括了 Runtime、Image 和 Distribution 三大标准。

## containerd 与 Docker 和 Kubernetes 的关系

仔细观察 containerd 架构图的上面部分，可以看出 containerd 通过提供 gRPC API 来供上层应用调用，上层应用可以直接集成 containerd client 来访问它的接口，诸如 Docker Engine、BuildKit 以及 containerd 自带的命令行工具 ctr 都是这样实现的；所以从 Docker 1.11 开始，当我们执行 `docker run` 命令时，整个流程大致如下：

![](./images/docker-to-containerd.png)

Docker Client 和 Docker Engine 是典型的 CS 架构，当用户执行 `docker run` 命令时，Docker Client 调用 Docker Engine 的接口，但是 Docker Engine 并不负责容器相关的事情，而是调用 containerd 的 gRPC 接口交给 containerd 来处理；不过 containerd 收到请求后，也并不会直接去创建容器，因为我们在上面提到，创建容器实际上已经有一个 OCI 标准了，这个标准有很多实现，其中 runc 是最常用的一个，所以 containerd 也不用再去实现这套标准了，而是直接调用这些现成的 OCI Runtime 即可。

不过创建容器有一点特别需要注意的地方，我们创建的容器进程需要一个父进程来做状态收集、维持 stdin 等工作的，这个父进程如果是 containerd 的话，那么如果 containerd 挂掉的话，整个机器上的所有容器都得退出了，为了解决这个问题，containerd 引入了 containerd-shim 组件；shim 的意思是垫片，正如它的名字所示，它其实是一个代理，充当着容器进程和 containerd 之间的桥梁；每当用户启动容器时，都会先启动一个 containerd-shim 进程，containerd-shim 然后调用 runc 来启动容器，之后 runc 会退出，而 containerd-shim 则会成为容器进程的父进程，负责收集容器进程的状态，上报给 containerd，并在容器中 PID 为 1 的进程退出后接管容器中的子进程进行清理，确保不会出现僵尸进程。

介绍完 containerd 与 Docker 之间的关系，我们再来看看它与 Kuberntes 的关系，从历史上看，Kuberntes 和 Docker 相爱相杀多年，一直是开源社区里热门的讨论话题。

在 Kubernetes 早期的时候，由于 Docker 风头正盛，所以 Kubernetes 选择通过直接调用 Docker API 来管理容器：

![](./images/kubelet-to-docker.png)

后来随着容器技术的发展，出现了很多其他的容器运行时，为了让 Kubernetes 平台支持更多的容器运行时，而不仅仅是和 Docker 绑定，Google 于是联合 Red Hat 一起推出了 [CRI](https://kubernetes.io/docs/concepts/architecture/cri/) 标准。CRI 的全称为 Container Runtime Interface，也就是容器运行时接口，它是 Kubernetes 定义的一组与容器运行时进行交互的接口，只要你实现了这套接口，就可以对接到 Kubernetes 平台上来。不过在那个时候，并没有多少容器运行时会直接去实现 CRI 接口，而是通过 shim 来适配不同的容器运行时，其中 dockershim 就是 Kubernetes 将 Docker 适配到 CRI 接口的一个实现：

![](./images/kubelet-to-docker-shim.png)

很显然，这个链路太长了，好在 Docker 将 containerd 项目独立出来了，那么 Kubernetes 是否可以绕过 Docker 直接与 containerd 通信呢？答案当然是肯定的，从 containerd 1.0 开始，containerd 开发了 CRI-Containerd，可以直接与 containerd 通信，从而取代了 dockershim（[从 Kubernetes 1.24 开始](https://kubernetes.io/zh-cn/blog/2022/05/03/dockershim-historical-context/)，dockershim 已经从 Kubernetes 的代码中删除了，[cri-dockerd](https://github.com/Mirantis/cri-dockerd) 目前交由社区维护）：

![](./images/kubelet-cri-containerd.png)

到了 containerd 1.1 版本，containerd 又进一步将 CRI-Containerd 直接以插件的形式集成到了 containerd 主进程中，也就是说 containerd 已经原生支持 CRI 接口了，这使得调用链路更加简洁：

![](./images/kubelet-to-containerd.png)

这也是目前 Kubernetes 默认的容器运行方案。不过，这条调用链路还可以继续优化下去，在 CNCF 中，还有另一个和 containerd 齐名的容器运行时项目 [cri-o](https://cri-o.io/)，它不仅支持 CRI 接口，而且创建容器的逻辑也更简单，通过 cri-o，kubelet 可以和 OCI 运行时直接对接，减少任何不必要的中间开销：

![](./images/kubelet-to-crio.png)

## 快速开始

这一节主要学习 containerd 的安装和使用。

### 安装 containerd

首先从 containerd 的 [Release 页面](https://github.com/containerd/containerd/releases) 下载最新版本：

```
$ curl -LO https://github.com/containerd/containerd/releases/download/v1.7.2/containerd-1.7.2-linux-amd64.tar.gz
```

然后将其解压到 `/usr/local/bin` 目录：

```
$ tar Cxzvf /usr/local containerd-1.7.2-linux-amd64.tar.gz 
bin/
bin/containerd-shim-runc-v1
bin/containerd-shim-runc-v2
bin/containerd-stress
bin/containerd
bin/containerd-shim
bin/ctr
```

其中，`containerd` 是服务端，我们可以直接运行：

```
$ containerd
INFO[2023-06-18T14:28:14.867212652+08:00] starting containerd revision=0cae528dd6cb557f7201036e9f43420650207b58 version=v1.7.2
...
INFO[2023-06-18T14:28:14.922388455+08:00] serving... address=/run/containerd/containerd.sock.ttrpc
INFO[2023-06-18T14:28:14.922477258+08:00] serving... address=/run/containerd/containerd.sock
INFO[2023-06-18T14:28:14.922529910+08:00] Start subscribing containerd event
INFO[2023-06-18T14:28:14.922570820+08:00] Start recovering state
INFO[2023-06-18T14:28:14.922636858+08:00] Start event monitor
INFO[2023-06-18T14:28:14.922653276+08:00] Start snapshots syncer
INFO[2023-06-18T14:28:14.922662467+08:00] Start cni network conf syncer for default
INFO[2023-06-18T14:28:14.922671149+08:00] Start streaming server
INFO[2023-06-18T14:28:14.922689846+08:00] containerd successfully booted in 0.060348s
```

`ctr` 是客户端，运行 `ctr version` 确认 containerd 是否安装成功：

```
$ ctr version
Client:
  Version:  v1.7.2
  Revision: 0cae528dd6cb557f7201036e9f43420650207b58
  Go version: go1.20.4

Server:
  Version:  v1.7.2
  Revision: 0cae528dd6cb557f7201036e9f43420650207b58
  UUID: 9eb2cbd4-8c1d-4321-839b-a8a4fc498de8
```

#### 以 systemd 方式启动 containerd

官方已经为我们准备好了 [containerd.service](https://raw.githubusercontent.com/containerd/containerd/main/containerd.service) 文件，我们只需要将其下载下来，放在 systemd 的配置目录下即可：

```
$ mkdir -p /usr/local/lib/systemd/system/
$ curl -L https://raw.githubusercontent.com/containerd/containerd/main/containerd.service -o /usr/local/lib/systemd/system/containerd.service
```

containerd.service 文件内容如下：

```
[Unit]
Description=containerd container runtime
Documentation=https://containerd.io
After=network.target local-fs.target

[Service]
#uncomment to enable the experimental sbservice (sandboxed) version of containerd/cri integration
#Environment="ENABLE_CRI_SANDBOXES=sandboxed"
ExecStartPre=-/sbin/modprobe overlay
ExecStart=/usr/local/bin/containerd

Type=notify
Delegate=yes
KillMode=process
Restart=always
RestartSec=5
# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNPROC=infinity
LimitCORE=infinity
LimitNOFILE=infinity
# Comment TasksMax if your systemd version does not supports it.
# Only systemd 226 and above support this version.
TasksMax=infinity
OOMScoreAdjust=-999

[Install]
WantedBy=multi-user.target
```

其中有两个配置很重要，`Delegate=yes` 表示允许 containerd 管理自己创建容器的 cgroups，否则 systemd 会将进程移到自己的 cgroups 中，导致 containerd 无法正确获取容器的资源使用情况；默认情况下，systemd 在停止或重启服务时会在进程的 cgroup 中查找并杀死所有子进程，`KillMode=process` 表示让 systemd 只杀死主进程，这样可以确保升级或重启 containerd 时不影响现有的容器。

然后我们使用 systemd 守护进程的方式启动 containerd 服务：

```
$ systemctl enable --now containerd
```

这样当系统重启后，containerd 服务也会自动启动了。

#### 安装 runc

安装好 containerd 之后，我们就可以使用 ctr 执行一些基本操作了，比如使用 `ctr image pull` 下载镜像：

```
$ ctr image pull docker.io/library/nginx:alpine
docker.io/library/nginx:alpine:                                                   resolved
index-sha256:2d194184b067db3598771b4cf326cfe6ad5051937ba1132b8b7d4b0184e0d0a6:    exists  
manifest-sha256:2d4efe74ef541248b0a70838c557de04509d1115dec6bfc21ad0d66e41574a8a: exists  
layer-sha256:768e67c521a97f2acf0382a9750c4d024fc1e541e22bab2dec1aad36703278f1:    exists  
config-sha256:4937520ae206c8969734d9a659fc1e6594d9b22b9340bf0796defbea0c92dd02:   exists  
layer-sha256:4db1b89c0bd13344176ddce2d093b9da2ae58336823ffed2009a7ea4b62d2a95:    exists  
layer-sha256:bd338968799fef766509223449d72392692f1f56802da9059ae3f0965c2885e2:    exists  
layer-sha256:6a107772494d184e0fddf5d99c877e2fa8d07d1d47b714c17b7d20eba1da01c6:    exists  
layer-sha256:9f05b0cc5f6e8010689a6331bad9ca02c62caa226b7501a64d50dcca0847dcdb:    exists  
layer-sha256:4c5efdb87c4a2350cc1c2781a80a4d3e895447007d9d8eac1e743bf80dd75c84:    exists  
layer-sha256:c8794a7158bff7f518985e76c590029ccc6b4c0f6e66e82952c3476c095225c9:    exists  
layer-sha256:8de2a93581dcb1cc62dd7b6e1620bc8095befe0acb9161d5f053a9719e145678:    exists  
elapsed: 2.8 s                                                                    total:   0.0 B (0.0 B/s)
unpacking linux/amd64 sha256:2d194184b067db3598771b4cf326cfe6ad5051937ba1132b8b7d4b0184e0d0a6...
done: 23.567287ms    

```

> 注意这里和 docker pull 的不同，镜像名称需要写全称。

不过这个时候，我们还不能运行镜像，我们不妨用 `ctr run` 命令运行一下试试：

```
$ ctr run docker.io/library/nginx:alpine nginx
ctr: failed to create shim task: 
    OCI runtime create failed: 
        unable to retrieve OCI runtime error (open /run/containerd/io.containerd.runtime.v2.task/default/nginx/log.json: no such file or directory):
            exec: "runc": executable file not found in $PATH: unknown
```

正如前文所述，这是因为 containerd 依赖 OCI runtime 来进行容器管理，containerd 默认的 OCI runtime 是 runc，我们还没有安装它。runc 的安装也非常简单，直接从其项目的 [Releases 页面](https://github.com/opencontainers/runc/releases) 下载最新版本：

```
$ curl -LO https://github.com/opencontainers/runc/releases/download/v1.1.7/runc.amd64
```

并将其安装到 `/usr/local/sbin` 目录即可：

```
$ install -m 755 runc.amd64 /usr/local/sbin/runc
```

使用 `ctr container rm` 删除刚刚运行失败的容器：

```
$ ctr container rm nginx
```

然后再使用 `ctr run` 重新运行：

```
$ ctr run docker.io/library/nginx:alpine nginx
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2023/06/18 07:04:52 [notice] 1#1: using the "epoll" event method
2023/06/18 07:04:52 [notice] 1#1: nginx/1.25.1
2023/06/18 07:04:52 [notice] 1#1: built by gcc 12.2.1 20220924 (Alpine 12.2.1_git20220924-r4) 
2023/06/18 07:04:52 [notice] 1#1: OS: Linux 3.10.0-1160.el7.x86_64
2023/06/18 07:04:52 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1024:1024
2023/06/18 07:04:52 [notice] 1#1: start worker processes
2023/06/18 07:04:52 [notice] 1#1: start worker process 30
```

可以看到此时容器正常启动了，不过目前这个容器还不具备网络能力，所以我们无法从外部访问它，可以使用 `ctr task exec` 进入容器：

```
$ ctr task exec -t --exec-id nginx nginx sh
```

在容器内部验证 nginx 服务是否正常：

```
/ # curl localhost:80
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

#### 安装 CNI 插件

正如上一节所示，默认情况下 containerd 创建的容器只有 lo 网络，无法从容器外部访问，如果希望将容器内的网络端口暴露出来，我们还需要安装 [CNI 插件](https://github.com/containernetworking/plugins)。和 CRI 一样，[CNI](https://github.com/containernetworking/cni/) 也是一套规范接口，全称为 Container Network Interface，即容器网络接口，它提供了一种将容器网络插件化的解决方案。CNI 涉及两个基本概念：容器和网络，它的接口也是围绕着这两个基本概念进行设计的，主要有两个：`ADD` 负责将容器加入网络，`DEL` 负责将容器从网络中删除，有兴趣的同学可以阅读 [CNI Specification](https://github.com/containernetworking/cni/blob/main/SPEC.md) 了解更具体的信息。

> 在 [week032-docker-network-in-action](../week032-docker-network-in-action/README.md) 这篇笔记中，我们曾经学习过 Docker 的 CNM 网络模型，它和 CNI 相比要复杂一些。CNM 和 CNI 是目前最流行的两种容器网络方案，关于他俩的区别，可以参考 [docker的网络-Container network interface(CNI)与Container network model(CNM)](https://xuxinkun.github.io/2016/07/22/cni-cnm/)。

官方提供了很多 CNI 接口的实现，比如 `bridge`、`ipvlan`、`macvlan` 等，这些都被称为 CNI 插件，此外，很多开源的容器网络项目，比如 `calico`、`flannel`、`weave` 等也实现了 CNI 插件。其实，CNI 插件就是一堆的可执行文件，我们可以从 [CNI 插件的 Releases 页面](https://github.com/containernetworking/plugins/releases) 下载最新版本：

```
$ curl -LO https://github.com/containernetworking/plugins/releases/download/v1.3.0/cni-plugins-linux-amd64-v1.3.0.tgz
```

然后将其解压到 `/opt/cni/bin` 目录（这是 CNI 插件的默认目录）：

```
$ mkdir -p /opt/cni/bin
$ tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.3.0.tgz 
./
./loopback
./bandwidth
./ptp
./vlan
./host-device
./tuning
./vrf
./sbr
./tap
./dhcp
./static
./firewall
./macvlan
./dummy
./bridge
./ipvlan
./portmap
./host-local
```

可以看到目录中包含了很多插件，这些插件按功能可以分成三大类：Main、IPAM 和 Meta：

* Main：负责创建网络接口，支持 `bridge`、`ipvlan`、`macvlan`、`ptp`、`host-device` 和 `vlan` 等类型的网络；
* IPAM：负责 IP 地址的分配，支持 `dhcp`、`host-local` 和 `static` 三种分配方式；
* Meta：包含一些其他配置插件，比如 `tuning` 用于配置网络接口的 sysctl 参数，`portmap` 用于主机和容器之间的端口映射，`bandwidth` 用于限流等等。

CNI 插件是通过 JSON 格式的文件进行配置的，我们首先创建 CNI 插件的配置目录 `/etc/cni/net.d`：

```
$ mkdir -p /etc/cni/net.d
```

然后在这个目录下新建一个配置文件：

```
$ vi /etc/cni/net.d/10-mynet.conf
{
    "cniVersion": "0.2.0",
    "name": "mynet",
    "type": "bridge",
    "bridge": "cni0",
    "isGateway": true,
    "ipMasq": true,
    "ipam": {
        "type": "host-local",
        "subnet": "10.22.0.0/16",
        "routes": [
            { "dst": "0.0.0.0/0" }
        ]
    }
}
```

其中 `"name": "mynet"` 表示网络的名称，`"type": "bridge"` 表示创建的是一个网桥网络，`"bridge": "cni0"` 表示创建网桥的名称，`isGateway` 表示为网桥分配 IP 地址，`ipMasq` 表示开启 IP Masquerade 功能，关于 `bridge` 插件的更多配置，可以参考 [bridge plugin 文档](https://www.cni.dev/plugins/current/main/bridge/)。

下面的 `ipam` 部分是 IP 地址分配的相关配置，`"type": "host-local"` 表示将使用 `host-local` 插件来分配 IP，这是一种简单的本地 IP 地址分配方式，它会从一个地址范围内来选择分配 IP，关于 `host-local` 插件的更多配置，可以参考 [host-local 文档](https://www.cni.dev/plugins/current/ipam/host-local/)。

除了网桥网络，我们再新建一个 `loopback` 网络的配置文件：

```
$ vi /etc/cni/net.d/99-loopback.conf
{
    "cniVersion": "0.2.0",
    "name": "lo",
    "type": "loopback"
}
```

CNI 项目中内置了一些简单的 Shell 脚本用于测试 CNI 插件的功能：

```
$ git clone https://github.com/containernetworking/cni.git
$ cd cni/scripts/
$ ls
docker-run.sh  exec-plugins.sh  priv-net-run.sh  release.sh
```

其中 `exec-plugins.sh` 脚本用于执行 CNI 插件，创建网络，并将某个容器加入该网络：

```
$ ./exec-plugins.sh 
Usage: ./exec-plugins.sh add|del CONTAINER-ID NETNS-PATH
  Adds or deletes the container specified by NETNS-PATH to the networks
  specified in $NETCONFPATH directory
```

该脚本有三个参数，第一个参数为 `add` 或 `del` 表示将容器添加到网络或将容器从网络中删除，第二个参数 `CONTAINER-ID` 表示容器 ID，一般没什么要求，保证唯一即可，第三个参数 `NETNS-PATH` 表示这个容器进程的网络命名空间位置，一般位于 `/proc/${PID}/ns/net`，所以，想要将上面运行的 nginx 容器加入网络中，我们需要知道这个容器进程的 PID，这个可以通过 `ctr task list` 得到：

```
$ ctr task ls
TASK     PID      STATUS    
nginx    20350    RUNNING
```

然后执行下面的命令：

```
$ CNI_PATH=/opt/cni/bin ./exec-plugins.sh add nginx /proc/20350/ns/net
```

前面的 `CNI_PATH=/opt/cni/bin` 是必不可少的，告诉脚本从这里执行 CNI 插件，执行之后，我们可以在主机上执行 `ip addr` 进行确认：

```
$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 08:00:27:7f:8e:9a brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 brd 10.0.2.255 scope global noprefixroute dynamic enp0s3
       valid_lft 72476sec preferred_lft 72476sec
    inet6 fe80::e0ae:69af:54a5:f8d0/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
3: cni0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 72:87:b6:07:19:07 brd ff:ff:ff:ff:ff:ff
    inet 10.22.0.1/16 brd 10.22.255.255 scope global cni0
       valid_lft forever preferred_lft forever
    inet6 fe80::7087:b6ff:fe07:1907/64 scope link 
       valid_lft forever preferred_lft forever
11: vethc5e583fc@if4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master cni0 state UP group default 
    link/ether 92:5c:c3:6a:a0:56 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet6 fe80::905c:c3ff:fe6a:a056/64 scope link 
       valid_lft forever preferred_lft forever
```

可以看出主机上多了一个名为 `cni0` 的网桥设备，这个就对应我们创建的网络，执行 `ip route` 也可以看到主机上多了一条到 cni0 的路由：

```
$ ip route
default via 10.0.2.2 dev enp0s3 proto dhcp metric 100 
10.0.2.0/24 dev enp0s3 proto kernel scope link src 10.0.2.15 metric 100 
10.22.0.0/16 dev cni0 proto kernel scope link src 10.22.0.1
```

另外，我们还能看到一个 veth 设备，在 [week032-docker-network-in-action](../week032-docker-network-in-action/README.md) 这篇笔记中我们已经学习过 veth 是一种虚拟的以太网隧道，其实就是一根网线，网线一头插在主机的 `cni0` 网桥上，另一头则插在容器里。我们可以进到容器里面进一步确认：

```
$ ctr task exec -t --exec-id nginx nginx sh
/ # ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
4: eth0@if11: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP 
    link/ether 0a:c2:11:63:ea:8c brd ff:ff:ff:ff:ff:ff
    inet 10.22.0.9/16 brd 10.22.255.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::8c2:11ff:fe63:ea8c/64 scope link 
       valid_lft forever preferred_lft forever
```

容器除了 `lo` 网卡之外，多了一张 `eth0` 网卡，它的 IP 地址是 10.22.0.9，这个正是我们在 `10-mynet.conf` 配置文件中定义的范围。这时，我们就可以在主机上通过这个 IP 来访问容器内部了：

```
$ curl 10.22.0.9:80
```

> `exec-plugins.sh` 脚本会遍历 `/etc/cni/net.d/` 目录下的所有配置来创建网络接口，我们也可以使用 [cnitool](https://github.com/containernetworking/cni/tree/main/cnitool) 来创建特定的网络接口。

> 通过将容器添加到指定网络，可以让容器具备和外界通信的能力，除了这种方式之外，我们也可以直接以主机网络模式启动容器：
> 
> ```
> $ ctr run --net-host docker.io/library/nginx:alpine nginx
> ```

### 使用 ctr 操作 containerd

经过上面的步骤，containerd 服务已经在我们的系统中安装和配置好了，接下来我们将学习命令行工具 `ctr` 对 containerd 进行操作，ctr 是 containerd 部署包中内置的命令行工具，功能比较简单，一般用于 containerd 的调试，其实在上面的安装步骤中已经多次使用过它，这一节对 ctr 做个简单的总结。

#### `ctr image` 命令

| 命令 | 含义 |
| --- | --- |
| `ctr image list` | 查看镜像列表 |
| `ctr image list -q` | 查看镜像列表，只显示镜像名称 |
| `ctr image pull docker.io/library/nginx:alpine` | 拉取镜像，注意镜像名称的前缀不能少 |
| `ctr image pull --platform linux/amd64 docker.io/library/nginx:alpine` | 拉取指定平台的镜像 |
| `ctr image pull --all-platforms docker.io/library/nginx:alpine` | 拉取所有平台的镜像 |
| `ctr image tag docker.io/library/nginx:alpine 192.168.1.109:5000/nginx:alpine` | 给镜像打标签 |
| `ctr image push 192.168.1.109:5000/nginx:alpine` | 推送镜像 |
| `ctr image push --user username:password 192.168.1.109:5000/nginx:alpine` | 推送镜像到带认证的镜像仓库 |
| `ctr image rm 192.168.1.109:5000/nginx:alpine` | 删除镜像 |
| `ctr image export nginx.tar docker.io/library/nginx:alpine` | 导出镜像 |
| `ctr image import hello.tar` | 导入镜像 |
| `ctr image import --platform linux/amd64 hello.tar` | 导入指定平台的镜像，如果导出的镜像文件只包含一个平台，导入时可能会报错 `ctr: content digest sha256:xxx: not found`，必须带上 `--platform` 这个参数 |
| `ctr image mount docker.io/library/nginx:alpine ./nginx` | 将镜像挂载到主机目录 |
| `ctr image unmount ./nginx` | 将镜像从主机目录卸载 |

#### `ctr container` 命令

| 命令 | 含义 |
| --- | --- |
| `ctr container list` | 查看容器列表 |
| `ctr container list -q` | 查看容器列表，只显示容器名称 |
| `ctr container create docker.io/library/nginx:alpine nginx` | 创建容器 |
| `ctr container info nginx` | 查看容器详情，类似于 `docker inspect` |
| `ctr container rm nginx` | 删除容器 |

#### `ctr task` 命令

| 命令 | 含义 |
| --- | --- |
| `ctr task list` | 查看任务列表，使用 `ctr container create` 创建容器时并没有运行，它只是一个静态的容器，包含了容器运行所需的资源和配置数据 |
| `ctr task start nginx` | 启动容器 |
| `ctr task exec -t --exec-id nginx nginx sh` | 进入容器进行操作，注意 `--exec-id` 参数随便写，只要唯一就行 |
| `ctr task metrics nginx` | 查看容器的 CPU 和内存使用情况 |
| `ctr task ps nginx` | 查看容器中的进程对应宿主机中的 PID |
| `ctr task pause nginx` | 暂停容器，暂停后容器状态变成 `PAUSED` |
| `ctr task resume nginx` | 恢复容器继续运行 |
| `ctr task kill nginx` | 停止容器，停止后容器状态变成 `STOPPED` |
| `ctr task rm nginx` | 删除任务 |

#### `ctr run` 命令

| 命令 | 含义 |
| --- | --- |
| `ctr run docker.io/library/nginx:alpine nginx` | 创建容器并运行，相当于 `ctr container create` + `ctr task start` |
| `ctr run --rm docker.io/library/nginx:alpine nginx` | 退出容器时自动删除容器 |
| `ctr run -d docker.io/library/nginx:alpine nginx` | 运行容器，运行之后从终端退出（detach）但容器不停止 |
| `ctr run --mount type=bind,src=/root/test,dst=/test,options=rbind:rw docker.io/library/nginx:alpine nginx` | 挂载本地目录或文件到容器 |
| `ctr run --env USER=root docker.io/library/nginx:alpine nginx` | 为容器设置环境变量 |
| `ctr run --null-io docker.io/library/nginx:alpine nginx` | 运行容器，并将控制台输出重定向到 /dev/null |
| `ctr run --log-uri file:///var/log/nginx.log docker.io/library/nginx:alpine nginx` | 运行容器，并将控制台输出写到文件中 |
| `ctr run --net-host docker.io/library/nginx:alpine nginx` | 使用主机网络运行容器 |
| `ctr run --with-ns=network:/var/run/netns/nginx docker.io/library/nginx:alpine nginx` | 使用指定命名空间文件运行容器 |

#### 命名空间

| 命令 | 含义 |
| --- | --- |
| `ctr ns list` | 查看命名空间列表 |
| `ctr ns create test` | 创建命名空间 |
| `ctr ns rm test` | 删除命名空间 |
| `ctr -n test image list` | 查看特定命名空间下的镜像列表 |
| `ctr -n test container list` | 查看特定命名空间下的容器列表 |

containerd 通过命名空间进行资源隔离，当没有指定命名空间时，默认使用 default 命名空间，Docker 和 Kubernetes 都可以基于 containerd 来管理容器，Docker 使用的是 `moby` 命名空间，Kubernetes 使用的是 `k8s.io` 命名空间，所以如果想查看 Kubernetes 运行的容器，可以通过 `ctr -n k8s.io container list` 查看。

除了上面的一些常用命令，还有一些不常用的命令，比如 `plugins`、`content`、`leases`、`snapshots`、`leases`、`shim` 等，这里就不一一介绍了，感兴趣的同学可以使用 `ctr` 或 `ctr help` 获取更多的帮助信息。

虽然使用 ctr 可以进行大部分 containerd 的日常操作，但是这些操作偏底层，对用户很不友好，比如不支持镜像构建，网络配置非常繁琐，所以 ctr 一般是供开发人员测试 containerd 用的；如果希望找一款更简单的命令行工具，可以使用 [nerdctl](https://github.com/containerd/nerdctl)，它的操作和 Docker 非常类似，对 Docker 用户来说会感觉非常亲近，nerdctl 相对于 ctr 来说，有着以下几点区别：

* nerdctl 支持使用 `Dockerfile` 构建镜像；
* nerdctl 支持使用 `docker-compose.yaml` 定义和管理多个容器；
* nerdctl 支持在容器内运行 systemd；
* nerdctl 支持使用 CNI 插件来配置容器网络；

除了 ctr 和 nerdctl，我们还可以使用 [crictl](https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md) 来操作 containerd，crictl 是 Kubernetes 提供的 CRI 客户端工具，由于 containerd 实现了 CRI 接口，所以 crictl 也可以充当 containerd 的客户端。此外，官方还提供了一份教程可以让我们 [实现自己的 containerd 客户端](https://github.com/containerd/containerd/blob/main/docs/getting-started.md#implementing-your-own-containerd-client)。

## 参考

* [一文搞懂容器运行时 Containerd](https://www.qikqiak.com/post/containerd-usage/)
* [Containerd 使用教程](https://icloudnative.io/posts/getting-started-with-containerd/)
* [Kubernetes 中的容器运行时](https://icloudnative.io/posts/container-runtime/)
* [开放容器标准(OCI) 内部分享](https://xuanwo.io/2019/08/06/oci-intro/)
* [docker、oci、runc以及kubernetes梳理](https://xuxinkun.github.io/2017/12/12/docker-oci-runc-and-kubernetes/)
* [走马观花云原生技术（1）：容器引擎containerd](https://taoofcoding.tech/blogs/2022-07-31/the-overview-of-cloud-native-projects-1)
* [Getting started with containerd](https://github.com/containerd/containerd/blob/main/docs/getting-started.md)
* [Mapping from dockercli to crictl](https://kubernetes.io/docs/reference/tools/map-crictl-dockercli/)
* [Container 命令ctr、crictl 命令使用说明](https://www.akiraka.net/kubernetes/1139.html)
* [Containerd shim 原理深入解读](https://icloudnative.io/posts/shim-shiminey-shim-shiminey/)
* [从零开始入门 K8s：理解 CNI 和 CNI 插件](https://www.infoq.cn/article/6mdfWWGHzAdihiq9lDST)
* [重学容器03: 使用CNI为Containerd容器添加网络能力](https://blog.frognew.com/2021/04/relearning-container-03.html)
* [使用CNI为Containerd创建网络接口](https://bigpigeon.org/post/containerd-tutorial-two/)

## 更多

### 使用 `ctr run --with-ns` 让容器在启动时加入已存在命名空间

上面我们是通过往容器进程的网络命名空间中增加网络接口来实现的，我们也可以先创建网络命名空间：

```
$ ip netns add nginx
```

这个网络命名空间的文件位置位于 `/var/run/netns/nginx`：

```
$ ls /var/run/netns
nginx
```

然后在这个网络命名空间中配置网络接口，可以执行 `exec-plugins.sh` 脚本：

```
$ CNI_PATH=/opt/cni/bin ./exec-plugins.sh add nginx /var/run/netns/nginx
```

或执行 `cnitool` 命令：

```
$ CNI_PATH=/opt/cni/bin cnitool add mynet /var/run/netns/nginx
```

`ctr run` 命令在启动容器的时候可以使用 `--with-ns` 参数让容器在启动时候加入到一个已存在的命名空间，所以可以通过这个参数加入到上面配置好的网络命名空间中：

```
$ ctr run --with-ns=network:/var/run/netns/nginx docker.io/library/nginx:alpine nginx
```

### containerd 的配置文件

使用 `containerd config default` 命令生成默认配置文件：

```
$ mkdir -p /etc/containerd
$ containerd config default > /etc/containerd/config.toml
```

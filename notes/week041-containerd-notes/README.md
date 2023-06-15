# WEEK041 - 容器运行时 containerd 学习笔记

2016 年 12 月，Docker 公司宣布将 [containerd](https://containerd.io/) 项目从 Docker Engine 中分离出来，形成一个独立的开源项目，并捐赠给 CNCF 基金会，旨在打造一个符合工业标准的容器运行时。Docker 公司之所以做出这样的决定，是因为当时在容器编排的市场上 Docker 面临着 Kubernetes 的极大挑战，将 containerd 分离，是为了方便开展 Docker Swarm 项目，不过结果大家都知道，Docker Swarm 在 Kubernetes 面前以惨败收场。

containerd 并不是直接面向最终用户的，而是主要用于集成到更上层的系统里，比如 Docker Swarm、Kubernetes 或 Mesos 等容器编排系统。containerd 通过 unix domain docket 暴露很低层的 gRPC API，上层系统可以通过这些 API 对机器上的容器整个生命周期进行管理，包括镜像的拉取、容器的启动和停止、以及底层存储和网络的管理等。下面是 containerd 官方提供的架构图：

![](./images/containerd-architecture.png)

从上图可以看出，containerd 的核心主要由一堆的 [Services](https://github.com/containerd/containerd/tree/main/api/services) 组成，通过 Content Store、Snapshotter 和 Runtime 三大技术底座，实现了 Containers、Content、Images、Leases、Namespaces 和 Snapshots 等的管理。

其中 Runtime 部分和容器的关系最为紧密，可以看到 containerd 通过 containerd-shim 来支持多种不同的 OCI Runtime，其中最为常用的 OCI Runtime 就是 [runC](https://github.com/opencontainers/runc)，所以只要是符合 OCI 标准的容器，都可以由 containerd 进行管理，值得一提的是 runC 也是由 Docker 开源的。

> [OCI](https://opencontainers.org/) 的全称为 Open Container Initiative，也就是开放容器标准，主要致力于创建一套开放的容器格式和运行时行业标准，目前包括了 Runtime、Image 和 Distribution 三大标准。

从 Docker 1.11 开始，当我们执行 `docker run` 命令时，整个流程大致如下：

![](./images/docker-to-containerd.png)

http://www.dockerinfo.net/4038.html

https://xuanwo.io/2019/08/06/oci-intro/

https://blog.kelu.org/tech/2020/10/09/the-diff-between-docker-containerd-runc-docker-shim.html

https://icloudnative.io/posts/shim-shiminey-shim-shiminey/

https://kubernetes.io/zh-cn/blog/2022/05/03/dockershim-historical-context/

## 参考

* [一文搞懂容器运行时 Containerd](https://www.qikqiak.com/post/containerd-usage/)
* [Containerd 使用教程](https://icloudnative.io/posts/getting-started-with-containerd/)
* [Kubernetes 中的容器运行时](https://icloudnative.io/posts/container-runtime/)
* [走马观花云原生技术（1）：容器引擎containerd](https://taoofcoding.tech/blogs/2022-07-31/the-overview-of-cloud-native-projects-1)
* [Getting started with containerd](https://github.com/containerd/containerd/blob/main/docs/getting-started.md)
* [Mapping from dockercli to crictl](https://kubernetes.io/docs/reference/tools/map-crictl-dockercli/)
* [Container 命令ctr、crictl 命令使用说明](https://www.akiraka.net/kubernetes/1139.html)

# WEEK006 CNCF 项目学习笔记（Dapr）

[Dapr](https://dapr.io/) 的全称为 `Distributed Application Runtime`（分布式应用运行时），顾名思义，它的目的就是为分布式应用提供运行所依赖的的执行环境。Dapr 为开发者提供了服务间调用（`service to service invocation`）、消息队列（`message queue`）和事件驱动（`event driven`）等服务模型，它可以让开发人员更聚焦业务代码，而不用去关心分布式系统所带来的其他复杂挑战，比如：服务发现（`service discovery`）、状态存储（`state management`）、加密数据存储（`secret management`）、可观察性（`observability`）等。

下面这张图说明了 Dapr 在分布式系统中所承担的作用：

![](./images/service-invocation.png)

这是分布式系统中最常用的一种场景，你的应用需要去调用系统中的另一个应用提供的服务。在引入 Dapr 之后，Dapr 通过边车模式运行在你的应用之上，Dapr 会通过服务发现机制为你去调用另一个应用的服务，并使用 mTLS 提供了服务间的安全访问，而且每个 Dapr 会集成 OpenTelemetry 自动为你提供服务之间的链路追踪、日志和指标等可观察性功能。

下图是基于事件驱动模型的另一种调用场景：

![](./images/pubsub.png)

## 安装 Dapr

### 1. 安装 Dapr CLI

首先使用下面的一键安装脚本安装 `Dapr CLI`：

```
[root@localhost ~]# wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
Getting the latest Dapr CLI...
Your system is linux_amd64
Installing Dapr CLI...

Installing v1.6.0 Dapr CLI...
Downloading https://github.com/dapr/cli/releases/download/v1.6.0/dapr_linux_amd64.tar.gz ...
dapr installed into /usr/local/bin successfully.
CLI version: 1.6.0 
Runtime version: n/a

To get started with Dapr, please visit https://docs.dapr.io/getting-started/
```

使用 `dapr -v` 校验是否安装成功：

```
[root@localhost ~]# dapr -v
CLI version: 1.6.0 
Runtime version: n/a
```

注意，这里我们可以看到 `Runtime version` 是 `n/a`，所以下一步我们还需要安装 `Dapr runtime`。

### 2. 初始化 Dapr

虽然 Dapr 也可以在非 Docker 环境下运行，但是官方更推荐使用 Docker，首先确保机器上已经安装有 Docker 环境，然后执行下面的 `dapr init` 命令：

```
[root@localhost ~]# dapr init
> Making the jump to hyperspace...
>> Installing runtime version 1.6.1
Dapr runtime installed to /root/.dapr/bin, you may run the following to add it to your path if you want to run daprd directly:
    export PATH=$PATH:/root/.dapr/bin
> Downloading binaries and setting up components...
> Downloaded binaries and completed components set up.
>> daprd binary has been installed to /root/.dapr/bin.
>> dapr_placement container is running.
>> dapr_redis container is running.
>> dapr_zipkin container is running.
>> Use `docker ps` to check running containers.
> Success! Dapr is up and running. To get started, go here: https://aka.ms/dapr-getting-started
```

从运行结果可以看到，Dapr 的初始化过程包含以下几个部分：

* 安装 Dapr 运行时（`daprd`），安装位置为 `/root/.dapr/bin`，同时会创建一个 `components` 目录用于默认组件的定义
* 运行 `dapr_placement` 容器，[dapr placement 服务](https://docs.dapr.io/concepts/dapr-services/placement/) 用于实现本地 actor 支持
* 运行 `dapr_redis` 容器，用于本地状态存储（`local state store`）和消息代理（`message broker`）
* 运行 `dapr_zipkin` 容器，用于实现服务的可观察性（`observability`）

初始化完成后，再次使用 `dapr -v` 校验是否安装成功：

```
[root@localhost ~]# dapr -v
CLI version: 1.6.0 
Runtime version: 1.6.1
```

并使用 `docker ps` 查看容器运行状态：

```
[root@localhost ~]# docker ps
CONTAINER ID   IMAGE               COMMAND                  CREATED             STATUS                       PORTS                                                 NAMES
63dd751ec5eb   daprio/dapr:1.6.1   "./placement"            About an hour ago   Up About an hour             0.0.0.0:50005->50005/tcp, :::50005->50005/tcp         dapr_placement
a8d3a7c93e12   redis               "docker-entrypoint.s…"   About an hour ago   Up About an hour             0.0.0.0:6379->6379/tcp, :::6379->6379/tcp             dapr_redis
52586882abea   openzipkin/zipkin   "start-zipkin"           About an hour ago   Up About an hour (healthy)   9410/tcp, 0.0.0.0:9411->9411/tcp, :::9411->9411/tcp   dapr_zipkin
```

## 使用 Dapr API

https://docs.dapr.io/getting-started/get-started-api/

## 参考

1. https://github.com/dapr/dapr
1. [Dapa 官方文档](https://docs.dapr.io/getting-started/)
1. [Dapr 知多少 | 分布式应用运行时](https://www.cnblogs.com/sheng-jie/p/how-much-you-know-about-dapr.html)

## 更多


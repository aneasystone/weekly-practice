# WEEK022 - etcd 学习笔记

[etcd](https://etcd.io/) 是一个用于存储分布式系统中的数据的高可用键值数据库（key-value store）。我们知道在 Linux 操作系统中有一个目录叫 `/etc`，它是专门用来存储操作系统配置的地方，`etcd` 这个名词就是源自于此，`etcd = etc + distibuted`，所以它的目的就是用来存储分布式系统中的关键数据。

![](./images/etcd.png)

etcd 内部采用 [Raft 一致性算法](http://thesecretlivesofdata.com/raft/)，以一致和容错的方式存储元数据。利用 etcd 可以实现包括配置管理、服务发现和协调分布式任务这些功能，另外 etcd 还提供了一些常用的分布式模式，包括领导选举，分布式锁和监控机器活动等。

Kubernetes 就是使用 etcd 来存储配置数据的，用于服务发现和集群管理。etcd 的一致性对于正确安排和运行服务至关重要，Kubernetes 的 API Server 将集群状态持久化在 etcd 中，通过 etcd 的 Watch API 监听集群，并发布关键的配置更改。

![](./images/k8s-apiserver-etcd.png)

## 快速开始

## 参考

1. [Etcd Quickstart](https://etcd.io/docs/v3.5/quickstart/) - Get etcd up and running in less than 5 minutes!
1. [Etcd 官方文档中文版](https://doczhcn.gitbook.io/etcd/)
1. [Etcd 教程](http://www.codebaoku.com/etcd/etcd-index.html)
1. [etcd 教程](https://www.tizi365.com/archives/557.html)
1. [七张图了解Kubernetes内部的架构](https://segmentfault.com/a/1190000022973856)

# WEEK046 - 学习 Kubernetes 流量管理之 Service

在 [week013-playing-with-kubernetes](../week013-playing-with-kubernetes/README.md) 这篇笔记中我们学习了 Kubernetes 的基本用法和概念，通过 Deployment 部署应用程序，然后通过 Service 将应用程序暴露给其他人访问。其中 Service 是 Kubernetes 最基础的流量管理机制之一，它的主要目的有：

* 以一个固定的地址来访问应用程序；
* 实现多个副本之间的负载均衡；
* 让应用程序可以在集群外部进行访问；

这篇笔记将继续使用之前的示例，通过一系列的实验更进一步地学习 Service 的工作原理。

## 准备实验环境

首先，创建一个 Deployment 部署应用程序，这里直接使用之前示例中的 `jocatalin/kubernetes-bootcamp:v1` 镜像，副本数设置为 3：

```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: myapp
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - image: jocatalin/kubernetes-bootcamp:v1
        name: myapp
```

确认三个副本都成功启动：

```
# kubectl get deploy myapp -o wide
NAME    READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                             SELECTOR
myapp   3/3     3            3           13m   myapp        jocatalin/kubernetes-bootcamp:v1   app=myapp
```

然后创建一个 Service：

```
apiVersion: v1
kind: Service
metadata:
  labels:
    app: myapp
  name: myapp
spec:
  ports:
  - name: http
    port: 38080
    protocol: TCP
    targetPort: 8080
  selector:
    app: myapp
  type: ClusterIP
```

通过 `kubectl get svc` 查询 Service 的地址和端口：

```
# kubectl get svc myapp -o wide
NAME    TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)     AGE     SELECTOR
myapp   ClusterIP   10.96.3.215   <none>        38080/TCP   7m22s   app=myapp
```

通过 Service 的地址验证服务能正常访问，多请求几次，可以看到会自动在副本之间轮询访问：

```
# curl 10.96.3.215:38080
Hello Kubernetes bootcamp! | Running on: myapp-fdb95659d-fl5c4 | v=1
# curl 10.96.3.215:38080
Hello Kubernetes bootcamp! | Running on: myapp-fdb95659d-dd5vv | v=1
# curl 10.96.3.215:38080
Hello Kubernetes bootcamp! | Running on: myapp-fdb95659d-4xf4g | v=1
# curl 10.96.3.215:38080
Hello Kubernetes bootcamp! | Running on: myapp-fdb95659d-fl5c4 | v=1
```

## Service 配置细节

```
# kubectl describe svc myapp
Name:              myapp
Namespace:         default
Labels:            app=myapp
Annotations:       <none>
Selector:          app=myapp
Type:              ClusterIP
IP Family Policy:  SingleStack
IP Families:       IPv4
IP:                10.96.3.215
IPs:               10.96.3.215
Port:              http  38080/TCP
TargetPort:        8080/TCP
Endpoints:         100.121.213.101:8080,100.121.213.103:8080,100.84.80.80:8080
Session Affinity:  None
Events:            <none>
```

```
# kubectl get endpoints myapp
NAME    ENDPOINTS                                                     AGE
myapp   100.121.213.101:8080,100.121.213.103:8080,100.84.80.80:8080   22m
```

## Service 类型

在 [week013-playing-with-kubernetes](../week013-playing-with-kubernetes/README.md) 这篇笔记中我们了解到，`Service` 有如下几种类型：

* `ClusterIP` - 这是 Service 的默认类型，在集群内部 IP 上公开 Service，这种类型的 Service 只能从集群内部访问；
* `NodePort` - 使用 NAT 在集群中每个选定 Node 的相同端口上公开 Service，可以通过 NodeIP:NodePort 从集群外部访问 Service，是 ClusterIP 的超集；
* `LoadBalancer` - 在集群中创建一个外部负载均衡器（如果支持的话），并为 Service 分配一个固定的外部 IP，是 NodePort 的超集；
* `ExternalName` - 通过返回带有该名称的 CNAME 记录，使用任意名称公开 Service，需要 kube-dns v1.7 或更高版本；

这一节将更深入地学习这几种类型的使用。

### `ClusterIP`

### `NodePort`

### `LoadBalancer`

### `ExternalName`

https://kubernetes.io/docs/concepts/services-networking/service/

https://kuboard.cn/learning/k8s-intermediate/service/service.html

https://kubernetes.feisky.xyz/concepts/objects/service

https://zeusro-awesome-kubernetes-notes.readthedocs.io/zh_CN/latest/chapter_8.html

https://github.com/guangzhengli/k8s-tutorials#service

https://jimmysong.io/kubernetes-handbook/concepts/service.html

https://learn.lianglianglee.com/%e4%b8%93%e6%a0%8f/Kubernetes%20%e5%ae%9e%e8%b7%b5%e5%85%a5%e9%97%a8%e6%8c%87%e5%8d%97/15%20Service%20%e5%b1%82%e5%bc%95%e6%b5%81%e6%8a%80%e6%9c%af%e5%ae%9e%e8%b7%b5.md

https://learn.lianglianglee.com/%e4%b8%93%e6%a0%8f/Kubernetes%20%e5%ae%9e%e8%b7%b5%e5%85%a5%e9%97%a8%e6%8c%87%e5%8d%97/13%20%e7%90%86%e8%a7%a3%e5%af%b9%e6%96%b9%e6%9a%b4%e9%9c%b2%e6%9c%8d%e5%8a%a1%e7%9a%84%e5%af%b9%e8%b1%a1%20Ingress%20%e5%92%8c%20Service.md

## Network Policy

https://kubernetes.feisky.xyz/concepts/objects/network-policy

## CoreDNS

https://learn.lianglianglee.com/%E4%B8%93%E6%A0%8F/Kubernetes%20%E5%AE%9E%E8%B7%B5%E5%85%A5%E9%97%A8%E6%8C%87%E5%8D%97/11%20%E6%9C%8D%E5%8A%A1%E5%8F%91%E7%8E%B0%20DNS%20%E7%9A%84%E8%90%BD%E5%9C%B0%E5%AE%9E%E8%B7%B5.md

## 参考

1. [数据包在 Kubernetes 中的一生（1）](https://blog.fleeto.us/post/life-of-a-packet-in-k8s-1/)
1. [IPVS从入门到精通kube-proxy实现原理](https://zhuanlan.zhihu.com/p/94418251)
1. [Kubernetes（k8s）kube-proxy、Service详解](https://www.cnblogs.com/liugp/p/16372503.html)

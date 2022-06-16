# WEEK013 - Kubernetes 使用小记

Kubernetes 常常被简称为 K8S（发音：Kate's），是 Google 在 2014 年发布的一个开源容器编排引擎。它诞生自 Google 内部的一款容器管理系统 [Borg](https://research.google/pubs/pub43438/)，据说，Borg 管理着 Google 数据中心里 20 多亿个容器服务。自发布以来，Kubernetes 迅速获得开源社区的追捧，包括 Red Hat、VMware、Canonical 在内的很多有影响力的公司都加入到它的开发和推广阵营中，目前，AWS、Azure、Google、阿里云、腾讯云等厂商都推出了基于 Kubernetes 的 CaaS 或 PaaS 产品。

Kubernetes 属于平台级技术，覆盖的技术范围非常广，包括计算、网络、存储、高可用、监控、日志等多个方面，而且在 Kubernetes 中有很多新的概念和设计理念，所以有一定的入门门槛。

在 WEEK010 中，我们学习了如何使用 Kind、Minikube 和 Kubeadmin 安装一个 Kubernetes 集群。这一节我们将照着 [官方教程](https://kubernetes.io/docs/tutorials/)，学习如何使用它，了解并掌握 Kubernetes 的基本概念。

## 使用 Minikube 创建集群

一个 Kubernetes 集群包含两种类型的资源：

* Master（也被称为控制平面 `Control Plane`）

用于管理整个集群，比如调度应用、维护应用状态、应用扩容和更新等。

* Node

每个 Node 上都运行着 `Kubelet` 程序，它负责运行应用，并且是和 Master 通信的代理。每个 Node 上还要有运行容器的工具，如 Docker 或 rkt。

我们可以使用 Minikube 创建一个单节点的简单集群。首先确保机器上已经安装 Minikube（安装步骤参考 WEEK010）：

```
$ minikube version
minikube version: v1.18.0
commit: ec61815d60f66a6e4f6353030a40b12362557caa-dirty
```

然后执行 `minikube start` 启动一个 Kubernetes 集群：

```
$ minikube start
* minikube v1.18.0 on Ubuntu 18.04 (amd64)
* Using the none driver based on existing profile

X The requested memory allocation of 2200MiB does not leave room for system overhead (total system memory: 2460MiB). You may face stability issues.
* Suggestion: Start minikube with less memory allocated: 'minikube start --memory=2200mb'

* Starting control plane node minikube in cluster minikube
* Running on localhost (CPUs=2, Memory=2460MB, Disk=194868MB) ...
* OS release is Ubuntu 18.04.5 LTS
* Preparing Kubernetes v1.20.2 on Docker 19.03.13 ...
  - kubelet.resolv-conf=/run/systemd/resolve/resolv.conf
  - Generating certificates and keys ...
  - Booting up control plane ...-
  - Configuring RBAC rules ...
* Configuring local host environment ...
* Verifying Kubernetes components...
  - Using image gcr.io/k8s-minikube/storage-provisioner:v4
* Enabled addons: default-storageclass, storage-provisioner
* Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

这样一个 Kubernetes 集群就安装好了，接下来我们就可以使用 `kubectl` 来管理这个集群。使用 `kubectl version` 查看客户端和服务端的版本信息：

```
$ kubectl version
Client Version: version.Info{Major:"1", Minor:"20", GitVersion:"v1.20.4", GitCommit:"e87da0bd6e03ec3fea7933c4b5263d151aafd07c", GitTreeState:"clean", BuildDate:"2021-02-18T16:12:00Z", GoVersion:"go1.15.8", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"20", GitVersion:"v1.20.2", GitCommit:"faecb196815e248d3ecfb03c680a4507229c2a56", GitTreeState:"clean", BuildDate:"2021-01-13T13:20:00Z", GoVersion:"go1.15.5", Compiler:"gc", Platform:"linux/amd64"}
```

使用 `kubectl cluster-info` 查看集群详情：

```
$ kubectl cluster-info
Kubernetes control plane is running at https://10.0.0.8:8443
KubeDNS is running at https://10.0.0.8:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

使用 `kubectl get nodes` 查看集群中的节点信息：

```
$ kubectl get nodes
NAME       STATUS   ROLES                  AGE     VERSION
minikube   Ready    control-plane,master   4m51s   v1.20.2
```

## 使用 kubectl 创建 Deployment

一旦我们有了一个可用的 Kubernetes 集群，我们就可以在集群里部署应用程序了。在 Kubernetes 中，Deployment 负责创建和更新应用程序的实例，所以我们需要创建一个 Deployment，然后 Kubernetes Master 就会将应用程序实例调度到集群中的各个节点上。

而且，Kubernetes 还提供了一种自我修复机制，当应用程序实例创建之后，Deployment 控制器会持续监视这些实例，如果托管实例的节点关闭或被删除，则 Deployment 控制器会将该实例替换为集群中另一个节点上的实例。

使用命令行工具 `kubectl` 可以创建和管理 Deployment，它通过 Kubernetes API 与集群进行交互。使用 `kubectl create deployment` 部署我们的第一个应用程序：

```
$ kubectl create deployment kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1
deployment.apps/kubernetes-bootcamp created
```

其中 `kubernetes-bootcamp` 为 Deployment 名称，`--image` 为要运行的应用程序镜像地址。

可以使用 `kubectl get deployments` 查看所有的 Deployment：

```
$ kubectl get deployments
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
kubernetes-bootcamp   1/1     1            1           5m8s
```

可以看到 `kubernetes-bootcamp` 这个 Deployment 里包含了一个应用实例，并且运行在 Pod 中。

```
$ kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
kubernetes-bootcamp-57978f5f5d-fwmqq   1/1     Running   0          19m
```

Pod 处于一个完全隔离的网络，默认情况下，只能从集群内的其他 Pod 或 Service 访问，从集群外面是不能访问的。我们可以使用 `kubectl` 启动一个代理，通过代理我们就可以访问集群内部网络：

```
$ kubectl proxy
Starting to serve on 127.0.0.1:8001
```

使用下面的 API 接口检查代理是否正常运行：

```
$ curl http://localhost:8001/version
{
  "major": "1",
  "minor": "20",
  "gitVersion": "v1.20.2",
  "gitCommit": "faecb196815e248d3ecfb03c680a4507229c2a56",
  "gitTreeState": "clean",
  "buildDate": "2021-01-13T13:20:00Z",
  "goVersion": "go1.15.5",
  "compiler": "gc",
  "platform": "linux/amd64"
}
```

然后通过下面的 API 接口来访问 Pod（其中 `kubernetes-bootcamp-57978f5f5d-fwmqq` 是 Pod 名称，可以通过上面的 `kubectl get pods` 查看）：

```
$ curl http://localhost:8001/api/v1/namespaces/default/pods/kubernetes-bootcamp-57978f5f5d-fwmqq/
{
  "kind": "Pod",
  "apiVersion": "v1",
  "metadata": {
    "name": "kubernetes-bootcamp-57978f5f5d-fwmqq",
    "generateName": "kubernetes-bootcamp-57978f5f5d-",
    "namespace": "default",
    "uid": "7bc3c22e-aa33-4290-a1b4-62b80f593cc9",
    "resourceVersion": "714",
    "creationTimestamp": "2022-06-15T23:39:52Z",
    "labels": {
      "app": "kubernetes-bootcamp",
      "pod-template-hash": "57978f5f5d"
    },
    "ownerReferences": [
      {
        "apiVersion": "apps/v1",
        "kind": "ReplicaSet",
        "name": "kubernetes-bootcamp-57978f5f5d",
        "uid": "a786a3e5-9d41-44be-8b1c-44d38e9bc3db",
        "controller": true,
        "blockOwnerDeletion": true
      }
    ],
    "managedFields": [
      {
        "manager": "kube-controller-manager",
        "operation": "Update",
        "apiVersion": "v1",
        "time": "2022-06-15T23:39:52Z",
        "fieldsType": "FieldsV1",
        "fieldsV1": {"f:metadata":{"f:generateName":{},"f:labels":{".":{},"f:app":{},"f:pod-template-hash":{}},"f:ownerReferences":{".":{},"k:{\"uid\":\"a786a3e5-9d41-44be-8b1c-44d38e9bc3db\"}":{".":{},"f:apiVersion":{},"f:blockOwnerDeletion":{},"f:controller":{},"f:kind":{},"f:name":{},"f:uid":{}}}},"f:spec":{"f:containers":{"k:{\"name\":\"kubernetes-bootcamp\"}":{".":{},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:enableServiceLinks":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}
      },
      {
        "manager": "kubelet",
        "operation": "Update",
        "apiVersion": "v1",
        "time": "2022-06-15T23:39:55Z",
        "fieldsType": "FieldsV1",
        "fieldsV1": {"f:status":{"f:conditions":{"k:{\"type\":\"ContainersReady\"}":{".":{},"f:lastProbeTime":{},"f:lastTransitionTime":{},"f:status":{},"f:type":{}},"k:{\"type\":\"Initialized\"}":{".":{},"f:lastProbeTime":{},"f:lastTransitionTime":{},"f:status":{},"f:type":{}},"k:{\"type\":\"Ready\"}":{".":{},"f:lastProbeTime":{},"f:lastTransitionTime":{},"f:status":{},"f:type":{}}},"f:containerStatuses":{},"f:hostIP":{},"f:phase":{},"f:podIP":{},"f:podIPs":{".":{},"k:{\"ip\":\"172.18.0.6\"}":{".":{},"f:ip":{}}},"f:startTime":{}}}
      }
    ]
  },
  "spec": {
    "volumes": [
      {
        "name": "default-token-cctqg",
        "secret": {
          "secretName": "default-token-cctqg",
          "defaultMode": 420
        }
      }
    ],
    "containers": [
      {
        "name": "kubernetes-bootcamp",
        "image": "gcr.io/google-samples/kubernetes-bootcamp:v1",
        "resources": {
          
        },
        "volumeMounts": [
          {
            "name": "default-token-cctqg",
            "readOnly": true,
            "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
          }
        ],
        "terminationMessagePath": "/dev/termination-log",
        "terminationMessagePolicy": "File",
        "imagePullPolicy": "IfNotPresent"
      }
    ],
    "restartPolicy": "Always",
    "terminationGracePeriodSeconds": 30,
    "dnsPolicy": "ClusterFirst",
    "serviceAccountName": "default",
    "serviceAccount": "default",
    "nodeName": "minikube",
    "securityContext": {
      
    },
    "schedulerName": "default-scheduler",
    "tolerations": [
      {
        "key": "node.kubernetes.io/not-ready",
        "operator": "Exists",
        "effect": "NoExecute",
        "tolerationSeconds": 300
      },
      {
        "key": "node.kubernetes.io/unreachable",
        "operator": "Exists",
        "effect": "NoExecute",
        "tolerationSeconds": 300
      }
    ],
    "priority": 0,
    "enableServiceLinks": true,
    "preemptionPolicy": "PreemptLowerPriority"
  },
  "status": {
    "phase": "Running",
    "conditions": [
      {
        "type": "Initialized",
        "status": "True",
        "lastProbeTime": null,
        "lastTransitionTime": "2022-06-15T23:39:52Z"
      },
      {
        "type": "Ready",
        "status": "True",
        "lastProbeTime": null,
        "lastTransitionTime": "2022-06-15T23:39:55Z"
      },
      {
        "type": "ContainersReady",
        "status": "True",
        "lastProbeTime": null,
        "lastTransitionTime": "2022-06-15T23:39:55Z"
      },
      {
        "type": "PodScheduled",
        "status": "True",
        "lastProbeTime": null,
        "lastTransitionTime": "2022-06-15T23:39:52Z"
      }
    ],
    "hostIP": "10.0.0.9",
    "podIP": "172.18.0.6",
    "podIPs": [
      {
        "ip": "172.18.0.6"
      }
    ],
    "startTime": "2022-06-15T23:39:52Z",
    "containerStatuses": [
      {
        "name": "kubernetes-bootcamp",
        "state": {
          "running": {
            "startedAt": "2022-06-15T23:39:54Z"
          }
        },
        "lastState": {
          
        },
        "ready": true,
        "restartCount": 0,
        "image": "jocatalin/kubernetes-bootcamp:v1",
        "imageID": "docker-pullable://jocatalin/kubernetes-bootcamp@sha256:0d6b8ee63bb57c5f5b6156f446b3bc3b3c143d233037f3a2f00e279c8fcc64af",
        "containerID": "docker://f00a2e64ec2a46d03f98ddd300dffdefde2ef306f545f873e4e596e2fa74c359",
        "started": true
      }
    ],
    "qosClass": "BestEffort"
  }
}
```

## 查看 Pod 和工作节点

https://kubernetes.io/zh-cn/docs/tutorials/kubernetes-basics/explore/explore-intro/

## 使用 Service 暴露你的应用

https://kubernetes.io/zh-cn/docs/tutorials/kubernetes-basics/expose/expose-intro/

## 运行应用程序的多个实例

https://kubernetes.io/zh-cn/docs/tutorials/kubernetes-basics/scale/scale-intro/

## 执行滚动更新

https://kubernetes.io/zh-cn/docs/tutorials/kubernetes-basics/update/update-intro/

## 参考

1. [学习 Kubernetes 基础知识](https://kubernetes.io/zh-cn/docs/tutorials/kubernetes-basics/)
1. [Kubernetes 术语表](https://kubernetes.io/docs/reference/glossary/)
1. [Play with Kubernetes](https://labs.play-with-k8s.com/)

## 更多

### Kubernetes 其他教程

https://kubernetes.io/docs/tutorials/

### Kubernetes 任务

https://kubernetes.io/docs/tasks/

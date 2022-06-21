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

这里的几个字段分别表示：

* `NAME` - Deployment 的名称。
* `READY` - 应用程序的可用副本数，显示格式为：就绪个数/期望个数。
* `UP-TO-DATE` - 显示为了达到期望状态已经更新的副本数。
* `AVAILABLE` - 可供用户使用的副本数。
* `AGE` - 应用程序运行的时间。

可以看到 `kubernetes-bootcamp` 这个 Deployment 里包含了一个应用实例，并且运行在 Pod 中。

```
$ kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
kubernetes-bootcamp-57978f5f5d-fwmqq   1/1     Running   0          19m
```

Pod 处于一个完全隔离的网络，默认情况下，只能从集群内的其他 Pod 或 Service 访问，从集群外面是不能访问的。我们会在后面的内容中学习如何访问 Pod 里的内容。

`kubectl` 是通过 Kubernetes API 来创建和管理我们的 Pod 的，我们可以使用 `kubectl` 启动一个代理，通过代理我们也可以访问 Kubernetes API：

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

然后通过下面的 API 接口获取 Pod 信息（其中 `kubernetes-bootcamp-57978f5f5d-fwmqq` 是 Pod 名称，可以通过上面的 `kubectl get pods` 查看）：

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

在上一节中，我们使用 `kubectl get pods` 查看集群中运行的 `Pod`，`Pod` 是 Kubernetes 中的原子单元，当我们在 Kubernetes 上创建 Deployment 时，该 Deployment 会在其中创建包含容器的 Pod，而不是直接创建容器。每个 Pod 都包含了一组应用程序容器（一个或多个），这些容器之间共享存储和网络，它们始终位于同一位置并且共同调度。

一个 Pod 总是运行在工作节点，工作节点是 Kubernetes 中参与计算的机器，每个工作节点由主节点管理，主节点会根据每个工作节点上的可用资源自动调度 Pod。每个工作节点上至少运行着：

* Kubelet，负责主节点和工作节点之间的通信，它还负责管理工作节点上的 Pod 和容器；
* 容器运行时

接下来我们使用 `kubelctl` 命令对 Pod 展开更深入的了解，大多数命令和 Docker 命令很类似，如果有一定的 Docker 基础，可以很快上手。使用 `kubectl get pods` 可以查看 Pod 列表，列表中显示着 Pod 名称和状态一些简单的信息，如果需要更详细的信息，可以使用 `kubectl describe` 命令：

```
$ kubectl describe pods
Name:         kubernetes-bootcamp-fb5c67579-8sm7d
Namespace:    default
Priority:     0
Node:         minikube/10.0.0.8
Start Time:   Thu, 16 Jun 2022 22:38:03 +0000
Labels:       app=kubernetes-bootcamp
              pod-template-hash=fb5c67579
Annotations:  <none>
Status:       Running
IP:           172.18.0.3
IPs:
  IP:           172.18.0.3
Controlled By:  ReplicaSet/kubernetes-bootcamp-fb5c67579
Containers:
  kubernetes-bootcamp:
    Container ID:   docker://ac8e5d785a8c7d8a550febdec1720f6d2a1ebe66f90ce970a963340b9f33c032
    Image:          gcr.io/google-samples/kubernetes-bootcamp:v1
    Image ID:       docker-pullable://jocatalin/kubernetes-bootcamp@sha256:0d6b8ee63bb57c5f5b6156f446b3bc3b3c143d233037f3a2f00e279c8fcc64af
    Port:           8080/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Thu, 16 Jun 2022 22:38:06 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-rn6wn (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  default-token-rn6wn:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-rn6wn
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                 node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  77s   default-scheduler  Successfully assigned default/kubernetes-bootcamp-fb5c67579-8sm7d to minikube
  Normal  Pulled     75s   kubelet            Container image "gcr.io/google-samples/kubernetes-bootcamp:v1" already present on machine
  Normal  Created    75s   kubelet            Created container kubernetes-bootcamp
  Normal  Started    74s   kubelet            Started container kubernetes-bootcamp
```

这里不仅显示了 Pod 的名称和状态，还显示了 Pod 的 IP 地址，Pod 里的容器信息，以及 Pod 生命周期中的一些关键事件。

我们可以直接使用 Pod 这里的 IP 地址来访问应用程序：

```
$ curl 172.18.0.3:8080
Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-fb5c67579-8sm7d | v=1
```

但是要注意的是，Kubernetes 每次调度 Pod 的时候，都会随机分配一个新的 IP 地址，所以这种做法是不推荐的，后面我们会学习更好的做法。

当我们的应用程序有问题时，查看日志是最常用的排查问题的方法，要查看 Pod 的日志，使用 `kubectl logs` 命令：

```
$ kubectl logs kubernetes-bootcamp-fb5c67579-8sm7d
Kubernetes Bootcamp App Started At: 2022-06-16T22:38:06.372Z | Running On:  kubernetes-bootcamp-fb5c67579-8sm7d 
```

注意由于我们的 Pod 里只有一个容器，所以不需要指定容器名。

当一个 Pod 是运行中状态时，我们可以使用 `kubectl exec` 在 Pod 中直接执行命令，比如下面的命令列出容器内的环境变量：

```
$ kubectl exec kubernetes-bootcamp-fb5c67579-8sm7d -- env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=kubernetes-bootcamp-fb5c67579-8sm7d
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_SERVICE_PORT=443
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
NPM_CONFIG_LOGLEVEL=info
NODE_VERSION=6.3.1
HOME=/root
```

下面的命令在容器内启动一个可交互的 Shell：

```
$ kubectl exec -ti kubernetes-bootcamp-fb5c67579-8sm7d -- bash
```

在这个 Shell 中我们可以做很多事情，和操作远程 SSH 完全一样，比如使用 `cat` 查看 `server.js` 的源码：

```
root@kubernetes-bootcamp-fb5c67579-8sm7d:/# cat server.js
var http = require('http');
var requests=0;
var podname= process.env.HOSTNAME;
var startTime;
var host;
var handleRequest = function(request, response) {
  response.setHeader('Content-Type', 'text/plain');
  response.writeHead(200);
  response.write("Hello Kubernetes bootcamp! | Running on: ");
  response.write(host);
  response.end(" | v=1\n");
  console.log("Running On:" ,host, "| Total Requests:", ++requests,"| App Uptime:", (new Date() - startTime)/1000 , "seconds", "| Log Time:",new Date());
}
var www = http.createServer(handleRequest);
www.listen(8080,function () {
    startTime = new Date();;
    host = process.env.HOSTNAME;
    console.log ("Kubernetes Bootcamp App Started At:",startTime, "| Running On: " ,host, "\n" );
});
```

在容器里使用 `curl` 访问我们的应用：

```
root@kubernetes-bootcamp-fb5c67579-8sm7d:/# curl localhost:8080
Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-fb5c67579-8sm7d | v=1
```

注意这里我们访问的是 `localhost`，这是因为我们现在处于容器内部。最后使用 `exit` 退出 Shell：

```
root@kubernetes-bootcamp-fb5c67579-8sm7d:/# exit
```

## 使用 Service 暴露你的应用

在上一节中，我们了解到我们的应用程序运行在 Pod 中，外部是无法访问的，虽然通过 Pod 的内部 IP 可以访问，但是要注意的是，Pod 是转瞬即逝的，当一个工作节点挂掉后，该工作节点上的 Pod 也会消亡，`ReplicaSet` 会自动地创建新的 Pod 让集群恢复到目标状态，保证应用程序正常运行。所以我们需要一种固定的方式来访问 Pod 中的应用，无论 Pod 如何变化，Kubernetes 通过服务（也就是 `Service`）来实现这一点。

`Service` 有如下几种类型：

* *ClusterIP* - 这是 Service 的默认类型，在集群内部 IP 上公开 Service，这种类型的 Service 只能从集群内部访问。
* *NodePort* - 使用 NAT 在集群中每个选定 Node 的相同端口上公开 Service，可以通过 NodeIP:NodePort 从集群外部访问 Service，是 ClusterIP 的超集。
* *LoadBalancer* - 在集群中创建一个外部负载均衡器（如果支持的话），并为 Service 分配一个固定的外部 IP，是 NodePort 的超集。
* *ExternalName* - 通过返回带有该名称的 CNAME 记录，使用任意名称公开 Service，需要 kube-dns v1.7 或更高版本。

可以使用 `kubectl get services` 命令查看目前集群中的 Service：

```
$ kubectl get services
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   71s
```

从上面可以看出，minikube 在创建集群时默认会创建一个名为 `kubernetes` 的 Service。使用 `kubectl expose` 创建一个新的 Service：

```
$ kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080
service/kubernetes-bootcamp exposed
```

这里使用了 `--type="NodePort"` 参数指定了 Service 的类型为 NodePort，这让我们可以从集群外部访问我们的应用，另外 `--port 8080` 表示希望将 8080 端口暴露出去，暴露出去的端口号随机生成。再次执行 `kubectl get services` 命令：

```
$ kubectl get services
NAME                  TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
kubernetes            ClusterIP   10.96.0.1        <none>        443/TCP          50s
kubernetes-bootcamp   NodePort    10.111.158.145   <none>        8080:31006/TCP   4s
```

此时集群中多了一个名为 `kubernetes-bootcamp` 的 Service，这个 Service 在集群内的 IP 为 `10.111.158.145`，暴露的端口为 `8080:31006`，这两个端口很容易混淆，8080 为集群内端口，31006 为集群外端口。

使用 Service 在集群内的 IP 和端口来访问服务：

```
$ curl 10.111.158.145:8080
Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-fb5c67579-8sm7d | v=1
```

从集群外访问服务：

```
$ curl $(minikube ip):31006
Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-fb5c67579-8sm7d | v=1
```

还可以使用 `kubectl describe` 查看 Service 的详细信息：

```
$ kubectl describe services/kubernetes-bootcamp
Name:                     kubernetes-bootcamp
Namespace:                default
Labels:                   app=kubernetes-bootcamp
Annotations:              <none>
Selector:                 app=kubernetes-bootcamp
Type:                     NodePort
IP Families:              <none>
IP:                       10.111.158.145
IPs:                      10.111.158.145
Port:                     <unset>  8080/TCP
TargetPort:               8080/TCP
NodePort:                 <unset>  31006/TCP
Endpoints:                172.18.0.3:8080
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

注意这里还有一个 IP 地址和上面的 IP 也很容易混淆，那就是 `Endpoints`，这个是 Pod 的地址。

创建 Service 时，该 Service 下的 Pod 是由标签（*Label*）和选择器（*Selector*）来匹配的，可以通过这种方式来对 Kubernetes 中的对象进行逻辑分组。标签（*Label*）是附加在对象上的键值对，可以以多种方式使用：

* 用于区分开发，测试和生产环境
* 用于区分不同的版本
* 使用 Label 将对象进行分类

实际上，当我们创建 Deployment 时，会为我们的 Pod 自带一个默认的 Label，使用 `kubectl describe deployment` 可以看出：

```
$ kubectl describe deployment
Name:                   kubernetes-bootcamp
Namespace:              default
CreationTimestamp:      Sat, 18 Jun 2022 01:24:48 +0000
Labels:                 app=kubernetes-bootcamp
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=kubernetes-bootcamp
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=kubernetes-bootcamp
  Containers:
   kubernetes-bootcamp:
    Image:        gcr.io/google-samples/kubernetes-bootcamp:v1
    Port:         8080/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   kubernetes-bootcamp-fb5c67579 (1/1 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  39m   deployment-controller  Scaled up replica set kubernetes-bootcamp-fb5c67579 to 1
```

执行 `kubectl get` 命令时，通过 `-l` 参数可以按指定标签查询列表，比如查询 Pod 列表：

```
$ kubectl get pods -l app=kubernetes-bootcamp
NAME                                  READY   STATUS    RESTARTS   AGE
kubernetes-bootcamp-fb5c67579-8sm7d   1/1     Running   0          49m
```

同样的，使用标签查询 Service 列表：

```
$ kubectl get services -l app=kubernetes-bootcamp
NAME                  TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
kubernetes-bootcamp   NodePort   10.111.158.145   <none>        8080:31006/TCP   51m
```

当然，我们也可以给某个对象手工指定标签，执行 `kubectl label` 命令：

```
$ kubectl label pods kubernetes-bootcamp-fb5c67579-8sm7d version=v1
pod/kubernetes-bootcamp-fb5c67579-8sm7d labeled
```

执行 `kubectl describe pods` 命令确认标签是否添加成功：

```
$ kubectl describe pods kubernetes-bootcamp-fb5c67579-8sm7d
Name:         kubernetes-bootcamp-fb5c67579-8sm7d
Namespace:    default
Priority:     0
Node:         minikube/10.0.0.8
Start Time:   Thu, 16 Jun 2022 22:38:03 +0000
Labels:       app=kubernetes-bootcamp
              pod-template-hash=fb5c67579
              version=v1
......
```

使用新标签查询 Pod 列表：

```
$ kubectl get pods -l version=v1
NAME                                  READY   STATUS    RESTARTS   AGE
kubernetes-bootcamp-fb5c67579-8sm7d   1/1     Running   0          7m52s
```

最后，使用 `kubectl delete service` 删除刚刚创建的 Service，可以使用 `-l` 根据标签删除指定的 Service：

```
$ kubectl delete service -l app=kubernetes-bootcamp
service "kubernetes-bootcamp" deleted
```

确认下 Service 已经删除：

```
$ kubectl get services
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   8m59s
```

此时，从集群外已经无法访问我们的服务了：

```
$ curl $(minikube ip):31006
curl: (7) Failed to connect to 10.0.0.10 port 31006: Connection refused
```

但是，我们的服务还是处于运行状态的，可以通过 Pod 的 IP 访问或进入 Pod 内部访问：

```
$ kubectl exec -ti kubernetes-bootcamp-fb5c67579-8sm7d -- curl localhost:8080
Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-fb5c67579-8sm7d | v=1
```

如果要停止服务，需要将 Deployment 删除掉才可以。

## 运行应用程序的多个实例

通过上面的学习，我们创建了一个 Deployment，然后通过 Service 让其可以从外部访问。默认情况下，Deployment 为我们的应用程序创建了一个 Pod，当然，我们可以根据需要，对我们的应用程序进行扩缩（扩容或缩容），改变 Pod 的副本集数量。

> ReplicaSet 实现了 Pod 的多副本管理，使用 Deployment 时会自动创建 ReplicaSet，我们通常不需要直接使用 ReplicaSet。Deployment 提供了比 ReplicaSet 更丰富的功能，比如版本记录和回滚等。

使用 `kubectl get rs` 查看集群中运行中的 `ReplicaSet` 列表：

```
$ kubectl get rs
NAME                            DESIRED   CURRENT   READY   AGE
kubernetes-bootcamp-fb5c67579   1         1         1       28m
```

如果要调整副本集数量，使用 `kubectl scale` 命令：

```
$ kubectl scale deployments/kubernetes-bootcamp --replicas=4
deployment.apps/kubernetes-bootcamp scaled
```

其中，`--replicas=4` 表示将应用程序扩容到 4 个副本：

```
$ kubectl get rs
NAME                            DESIRED   CURRENT   READY   AGE
kubernetes-bootcamp-fb5c67579   4         4         4       30m
```

使用 `kubectl get pods` 可以看到启动了 4 个 Pod，每个 Pod 都分配了一个独立的 IP：

```
$ kubectl get pods -o wide
NAME                                  READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
kubernetes-bootcamp-fb5c67579-cgwjm   1/1     Running   0          65s   172.18.0.7   minikube   <none>           <none>
kubernetes-bootcamp-fb5c67579-d7l4n   1/1     Running   0          65s   172.18.0.9   minikube   <none>           <none>
kubernetes-bootcamp-fb5c67579-mpn68   1/1     Running   0          30m   172.18.0.2   minikube   <none>           <none>
kubernetes-bootcamp-fb5c67579-tk2lm   1/1     Running   0          65s   172.18.0.8   minikube   <none>           <none>
```

执行 `kubectl describe deployments` 可以看到副本集调整的事件：

```
$ kubectl describe deployments/kubernetes-bootcamp
Name:                   kubernetes-bootcamp
Namespace:              default
CreationTimestamp:      Sun, 19 Jun 2022 03:16:25 +0000
Labels:                 app=kubernetes-bootcamp
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=kubernetes-bootcamp
Replicas:               4 desired | 4 updated | 4 total | 4 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=kubernetes-bootcamp
  Containers:
   kubernetes-bootcamp:
    Image:        gcr.io/google-samples/kubernetes-bootcamp:v1
    Port:         8080/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
OldReplicaSets:  <none>
NewReplicaSet:   kubernetes-bootcamp-fb5c67579 (4/4 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  32m    deployment-controller  Scaled up replica set kubernetes-bootcamp-fb5c67579 to 1
  Normal  ScalingReplicaSet  2m38s  deployment-controller  Scaled up replica set kubernetes-bootcamp-fb5c67579 to 4
```

执行 `kubectl describe services` 可以看到 `Endpoints` 变成了多个：

```
$ kubectl describe services/kubernetes-bootcamp
Name:                     kubernetes-bootcamp
Namespace:                default
Labels:                   app=kubernetes-bootcamp
Annotations:              <none>
Selector:                 app=kubernetes-bootcamp
Type:                     NodePort
IP Families:              <none>
IP:                       10.96.61.243
IPs:                      10.96.61.243
Port:                     <unset>  8080/TCP
TargetPort:               8080/TCP
NodePort:                 <unset>  31955/TCP
Endpoints:                172.18.0.2:8080,172.18.0.7:8080,172.18.0.8:8080 + 1 more...
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

Service 会对请求自动进行负载均衡，我们发送多次请求，可以看到请求会落到不同的 Pod 上：

```
$ curl $(minikube ip):31955
Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-fb5c67579-d7l4n | v=1

$ curl $(minikube ip):31955
Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-fb5c67579-mpn68 | v=1

$ curl $(minikube ip):31955
Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-fb5c67579-cgwjm | v=1

$ curl $(minikube ip):31955
Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-fb5c67579-tk2lm | v=1
```

我们再次执行 `kubectl scale`，将副本数改成 2：

```
$ kubectl scale deployments/kubernetes-bootcamp --replicas=2
deployment.apps/kubernetes-bootcamp scaled
```

查看 Deployment 列表显示当前的副本集个数：

```
$ kubectl get deployments
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
kubernetes-bootcamp   2/2     2            2           45m
```

再次查看 Pod 列表，可以发现有两个 Pod 被停止（Terminating）了：

```
$ kubectl get pods -o wide
NAME                                  READY   STATUS        RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
kubernetes-bootcamp-fb5c67579-cgwjm   1/1     Terminating   0          15m   172.18.0.7   minikube   <none>           <none>
kubernetes-bootcamp-fb5c67579-d7l4n   1/1     Running       0          15m   172.18.0.9   minikube   <none>           <none>
kubernetes-bootcamp-fb5c67579-mpn68   1/1     Running       0          45m   172.18.0.2   minikube   <none>           <none>
kubernetes-bootcamp-fb5c67579-tk2lm   1/1     Terminating   0          15m   172.18.0.8   minikube   <none>           <none>
```

## 执行滚动更新

当我们的应用程序运行多个实例时，我们就可以对我们的应用进行零停机的滚动更新（*Rolling Update*），而且所有的更新都是经过版本控制的，任何 Deployment 更新都可以恢复到以前的（稳定）版本。

下面使用 `kubectl set image` 命令执行滚动更新，将应用版本升级到 v2：

```
$ kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2
deployment.apps/kubernetes-bootcamp image updated
```

等待应用更新完毕后，再次访问我们的应用，成功升级到 v2：

```
$ curl $(minikube ip):31955
Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-7d44784b7c-4ntgh | v=2
```

也可以使用 `kubectl rollout status` 查看更新是否成功：

```
$ kubectl rollout status deployments/kubernetes-bootcamp
deployment "kubernetes-bootcamp" successfully rolled out
```

如果我们更新的时候出错了，比如更新到一个不存在的镜像：

```
$ kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=gcr.io/google-samples/kubernetes-bootcamp:v10
deployment.apps/kubernetes-bootcamp image updated
```

可以发现 Kubernetes 并不会直接将四个 Pod 一股脑都升级到错误的镜像，而是先停止一个 Pod，等待这个 Pod 更新成功，再更新下一个，保证应用服务一直是可访问的（也就是零停机）。

执行 `kubectl get deployments` 可以看到当前有 3 个可用的应用实例，有 2 个正在更新：

```
$ kubectl get deployments
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
kubernetes-bootcamp   3/4     2            3           13m
```

使用 `kubectl get pods` 可以看到有 2 个 Pod 一直处于 `ImagePullBackOff` 状态（因为这个镜像不存在）：

```
$ kubectl get pods
NAME                                   READY   STATUS             RESTARTS   AGE
kubernetes-bootcamp-59b7598c77-8nfsh   0/1     ImagePullBackOff   0          2m35s
kubernetes-bootcamp-59b7598c77-rcdfq   0/1     ImagePullBackOff   0          2m35s
kubernetes-bootcamp-7d44784b7c-9vwn2   1/1     Running            0          13m
kubernetes-bootcamp-7d44784b7c-qcgnn   1/1     Running            0          13m
kubernetes-bootcamp-7d44784b7c-vfn79   1/1     Running            0          13m
```

下面是 `kubectl rollout status` 命令的输出：

```
$ kubectl rollout status deployments/kubernetes-bootcampWaiting for deployment "kubernetes-bootcamp" rollout to finish: 2 out of 4 new replicas have been updated...
```

这时可以使用 `kubectl rollout undo` 执行回滚操作，应用程序将会全部恢复到之前的 v2 版本：

```
$ kubectl rollout undo deployments/kubernetes-bootcamp
deployment.apps/kubernetes-bootcamp rolled back

$ kubectl rollout status deployments/kubernetes-bootcamp
deployment "kubernetes-bootcamp" successfully rolled out
```

## 参考

1. [学习 Kubernetes 基础知识](https://kubernetes.io/zh-cn/docs/tutorials/kubernetes-basics/)
1. [Kubernetes 术语表](https://kubernetes.io/docs/reference/glossary/)
1. [Play with Kubernetes](https://labs.play-with-k8s.com/)
1. [Kubernetes 指南](https://kubernetes.feisky.xyz/concepts/architecture)

## 更多

### 了解 Kubernetes 基本概念

#### Cluster

Cluster 是计算、存储和网络资源的集合，Kubernete 利用这些资源运行各种基于容器的应用。

#### Master

Master 的主要职责是调度，决定将应用放在哪个 Node 上运行。

#### Node

Node 的主要职责是运行容器应用，同时监控并汇报容器状态。

#### Pod

Kubernetes 以 Pod 作为最小工作单元进行调度和管理，每个 Pod 包含一个或多个容器，Pod 中的容器会作为一个整体被调度到一个 Node 上运行。

Pod 中的所有容器使用同一个网络，即相同的 IP 地址和 Port 空间，它们可以直接使用 localhost 通信。这些容器之间也共享存储，当 Kubernetes 挂载 Volumne 到 Pod，本质上是将 Volumne 挂载到 Pod 里的每个容器。

#### Controller

Kubernetes 通常不会直接创建 Pod，而是通过 Controller 来管理 Pod 的。为满足不同的业务场景，Kubernete 提供了多种 Controller：

1. Deployment - 通过 ReplicaSet 实现 Pod 的多副本管理，还提供版本升级和回滚等功能
2. ReplicaSet - 实现 Pod 的多副本管理
3. DaemonSet - 每个 Node 最多只运行一个 Pod 副本
4. StatefulSet - 保证 Pod 的每个副本在整个生命周期中名称不变
5. Job - 运行一次性的任务，运行结束后自动删除

#### Service

Deployment 可以部署多个副本，每个 Pod 都有自己的 IP，但是我们不能通过 Pod 的 IP 直接来访问，因为 Pod 很可能会被频繁地销毁和重启，它们的 IP 会发生变化。

于是引入了 Service 的概念，Service 提供了访问一组特定 Pod 的方式，它有自己的 IP 和端口，并为 Pod 提供负载均衡。

#### Namespace

Namespace 一般用于多租户隔离，它将一个物理的 Cluster 划分成多个虚拟 Cluster，不同 Namespace 里的资源是完全隔离的。Kubernetes 默认创建了两个 Namespace：

```
$ kubectl get namespace
NAME                   STATUS   AGE
default                Active   28s
kube-system            Active   29s
```

创建资源时如果不指定 Namespace，默认会放在 `default` 中，Kubernetes 自己创建的系统资源放在 `kube-system` 中。

### Kubernetes 架构

Kubernetes 主要由以下几个核心组件组成：
* etcd 保存了整个集群的状态；
* kube-apiserver 提供了资源操作的唯一入口，并提供认证、授权、访问控制、API 注册和发现等机制；
* kube-controller-manager 负责维护集群的状态，比如故障检测、自动扩展、滚动更新等；
* kube-scheduler 负责资源的调度，按照预定的调度策略将 Pod 调度到相应的机器上；
* kubelet 负责维持容器的生命周期，同时也负责 Volume（CVI）和网络（CNI）的管理；
* Container runtime 负责镜像管理以及 Pod 和容器的真正运行（CRI）；
* kube-proxy 负责为 Service 提供 cluster 内部的服务发现和负载均衡；

![](./images/components.png)

### Kubernetes 其他教程

https://kubernetes.io/docs/tutorials/

### Kubernetes 任务

https://kubernetes.io/docs/tasks/

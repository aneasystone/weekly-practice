# 在 Kubernetes 环境中开发 Spring Boot 项目

这篇教程介绍了如何在 Kubernetes 环境下部署 Spring Boot 应用，严格来说这并不是一篇关于 Spring Boot 的教程，而是一篇关于 Kubernetes 的简单入门。

## 准备 Kubernetes 环境

在开始教程之前，需要先确保你已经安装有 Kubernetes 环境了，可以参考 [week010-install-kubernetes](../../../../week010-install-kubernetes/README.md) 来安装 Kubernetes。

使用 `kubectl cluster-info` 查看集群信息：

```
> kubectl cluster-info
Kubernetes control plane is running at https://kubernetes.docker.internal:6443
CoreDNS is running at https://kubernetes.docker.internal:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

使用 `kubectl get all` 查看当前集群中所有的资源：

```
> kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   53d
```

## 准备 Spring Boot 应用

我们直接使用在 [week011-spring-boot-on-docker](../../../../week011-spring-boot-on-docker/README.md) 中创建的 Spring Boot 应用，在那一篇教程中，我们还使用 Jib 插件将应用构建成 Docker 镜像 `aneasystone/myapp`，并推送到了 DockerHub 公共仓库。

使用 `docker` 运行应用：

```
> docker run --rm -p 8080:8080 aneasystone/myapp
```

## 将应用部署到 Kubernetes

Kubernetes 使用一个 YAML 文件来部署应用，可以使用 kubectl 来创建这个 YAML 文件：

```
> kubectl create deployment myapp --image=aneasystone/myapp --dry-run=client -o=yaml > deployment.yaml
> echo --- >> .\deployment.yaml
> kubectl create service clusterip myapp --tcp=8080:8080 --dry-run=client -o=yaml >> .\deployment.yaml
```

上面的 `kubectl create deployment` 和 `kubectl create service` 两个命令本来是用于创建 `Deployment` 和 `Service` 的，但是在这里使用了 `--dry-run=client` 参数只预览执行结果而不真实执行，并通过 `-o=yaml` 参数将执行结果保存成 YAML 格式的文件。生成的 `deployment.yaml` 文件内容如下：

```
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: myapp
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: myapp
    spec:
      containers:
      - image: aneasystone/myapp
        name: myapp
        resources: {}
status: {}
---
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: null
  labels:
    app: myapp
  name: myapp
spec:
  ports:
  - name: 8080-8080
    port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    app: myapp
  type: ClusterIP
status:
  loadBalancer: {}
```

可以根据需要对文件进行修改，比如将副本数修改为 2，或限制内存占用等，然后再使用 `kubectl apply` 执行部署：

```
> kubectl apply -f deployment.yaml
deployment.apps/myapp created
service/myapp created
```

执行后稍等片刻，使用 `kubectl get all` 查看应用的执行情况：

```
> kubectl get all
NAME                         READY   STATUS    RESTARTS   AGE
pod/myapp-5457bd6566-9hkvw   1/1     Running   0          38s

NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP    53d
service/myapp        ClusterIP   10.106.78.189   <none>        8080/TCP   39s

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/myapp   1/1     1            1           39s

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/myapp-5457bd6566   1         1         1       39s
```

可以看到我们创建了 `Deployment`、`ReplicaSet`、`Pod` 和 `Service` 这些资源。

由于 Service 类型是 `ClusterIP`，因此暴露的端口 8080 只能在集群内部访问，可以使用 `kubectl port-forward` 将端口代理出来：

```
> kubectl port-forward service/myapp 8080:8080

Forwarding from 127.0.0.1:8080 -> 8080
Forwarding from [::1]:8080 -> 8080
```

这样就可以从集群外面访问应用了：

```
$ curl http://localhost:8080
Hello Docker World
```

## 使用 NodePort

在上面创建 `Service` 的时候，也可以使用 `NodePort` 类型：

```
> kubectl create service nodeport myapp --tcp=8080:8080 --dry-run=client -o=yaml >> .\deployment2.yaml
```

运行之后可以看到 Service 的端口是 `8080:32016/TCP`：

```
> kubectl get all
NAME                         READY   STATUS    RESTARTS   AGE
pod/myapp-5457bd6566-82w6b   1/1     Running   0          65s

NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP          53d
service/myapp        NodePort    10.109.254.94   <none>        8080:32016/TCP   65s

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/myapp   1/1     1            1           65s

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/myapp-5457bd6566   1         1         1       65s
```

此时可以直接从集群外面通过 `32016` 端口访问应用：

```
$ curl http://localhost:32016
Hello Docker World
```

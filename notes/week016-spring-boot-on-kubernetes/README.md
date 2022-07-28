# WEEK016 - 在 Kubernetes 环境中开发 Spring Boot 项目

在前面的教程中，我们学习了很多 Spring Boot 与 Docker 或 Kubernetes 的知识。比如在 [spring-boot-docker](../week009-spring-guides/guides/gs/spring-boot-docker/README.md) 中介绍了如何编写 Dockerfile 文件，以及如何构建一个 Docker 镜像来运行 Spring Boot 应用；在 [week011-spring-boot-on-docker](../week011-spring-boot-on-docker/README.md) 中更加深入的学习了构建镜像的知识以及如何优化我们的 Spring Boot 镜像；然后在 [spring-boot-kubernetes](../week009-spring-guides/guides/gs/spring-boot-kubernetes/README.md) 这篇教程中介绍了如何在 Kubernetes 环境下部署 Spring Boot 应用，不过教程的内容浅尝辄止，只能算作 Kubernetes 的简单入门。

在这篇教程中，我们将继续学习 Kubernetes 的知识，以及在 Kubernetes 环境下部署 Spring Boot 应用的最佳实践。

## 准备应用

通过 [start.spring.io](https://start.spring.io/) 生成项目代码，依赖选择 webflux 和 actuator。代码生成后，直接使用 Spring Boot Maven Plugin 构建镜像：

```
$ ./mvnw spring-boot:build-image -Dspring-boot.build-image.imageName=aneasystone/spring-boot-k8s
```

然后使用 `docker run` 运行：

```
$ docker run --name spring-boot-k8s -p 8080:8080 -t aneasystone/spring-boot-k8s
```

通过 `/actuator/health` 端点检查程序是否启动成功：

```
$ curl http://localhost:8080/actuator/health
{"status":"UP"}
```

## 将应用部署到 Kubernetes

在部署之前，需要首先确保两件事情：

1. 安装 Kubernetes CLI（`kubectl`）
2. 安装 Kubernetes 集群

可以参考 [week010-install-kubernetes](../week010-install-kubernetes/README.md) 和 [week013-playing-with-kubernetes](../week013-playing-with-kubernetes/README.md) 安装 Kubernetes，并使用下面的命令检查环境是否已准备好：

```
$ kubectl cluster-info
```

一切准备就绪之后，我们创建一个 k8s 目录，并在该目录下创建两个 YAML 文件，一个 `deployment.yaml` 文件：

```
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: spring-boot-k8s
  name: spring-boot-k8s
spec:
  replicas: 1
  selector:
    matchLabels:
      app: spring-boot-k8s
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: spring-boot-k8s
    spec:
      containers:
      - image: aneasystone/spring-boot-k8s:snapshot
        name: spring-boot-k8s
        resources: {}
status: {}
```

一个 `service.yaml` 文件：

```
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: null
  labels:
    app: spring-boot-k8s
  name: spring-boot-k8s
spec:
  ports:
  - name: 80-8080
    port: 80
    protocol: TCP
    targetPort: 8080
  selector:
    app: spring-boot-k8s
  type: ClusterIP
status:
  loadBalancer: {}
```

这两个文件也可以通过下面的 `kubectl` 命令生成：

```
$ kubectl create deployment spring-boot-k8s --image aneasystone/spring-boot-k8s:snapshot -o yaml --dry-run=client > k8s/deployment.yaml
$ kubectl create service clusterip spring-boot-k8s --tcp 80:8080 -o yaml --dry-run=client > k8s/service.yaml
```

这里有一点要注意的是，Kubernetes 默认情况下对于 tag 为 latest 的镜像拉取策略（Pull policy）是 `Always`，为了不让 Kubernetes 拉取镜像（因为这个镜像不在外部的镜像仓库里），而是直接使用本地的镜像，我们需要将镜像 tag 修改掉，这里修改为 snapshot，对于非 latest 的镜像，Kubernetes 的拉取策略是 `IfNotPresent`。

```
$ docker tag aneasystone/spring-boot-k8s aneasystone/spring-boot-k8s:snapshot
```

然后使用 `kubectl apply` 将镜像部署到 Kubernetes 集群：

```
$ kubectl apply -f ./k8s
```

稍等片刻，使用 `kubectl get all` 检查应用在集群中的运行情况：

```
$ kubectl get all
NAME                                  READY   STATUS    RESTARTS   AGE
pod/spring-boot-k8s-f45df6cc6-hh679   1/1     Running   0          20s

NAME                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/kubernetes        ClusterIP   10.96.0.1       <none>        443/TCP   72d
service/spring-boot-k8s   ClusterIP   10.111.105.66   <none>        80/TCP    20s

NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/spring-boot-k8s   1/1     1            1           20s

NAME                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/spring-boot-k8s-f45df6cc6   1         1         1       20s
```

此时我们还不能访问我们的服务，这是因为服务的端口只暴露在集群内部，可以通过 `kubectl port-forward` 将集群内部的某个端口代理出来：

```
$ kubectl port-forward svc/spring-boot-k8s 9090:80
```

然后使用 `/actuator/health` 端点检查服务的健康状态：

```
$ curl -s http://localhost:9090/actuator/health
{"status":"UP","groups":["liveness","readiness"]}
```

## 最佳实践

## 使用 `ConfigMaps` 配置

## 服务发现和负载均衡

## 参考

* [【Topical Guides】Spring on Kubernetes](https://spring.io/guides/topicals/spring-on-kubernetes/)

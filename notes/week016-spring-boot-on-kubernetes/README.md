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

为了让我们的应用能更好地在 Kubernetes 环境下运行，推荐以下几点最佳实践：

1. [添加 readiness 和 liveness 探针](https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-features.html#production-ready-kubernetes-probes)
2. [等待容器生命周期结束](https://docs.spring.io/spring-boot/docs/current/reference/html/deployment.html#deployment.cloud.kubernetes.container-lifecycle)
3. [开启优雅退出](https://docs.spring.io/spring-boot/docs/current/reference/html/web.html#web.graceful-shutdown)

我们在 `deployment.yaml` 文件中找到容器相关的配置，并添加 `livenessProbe`、`readinessProbe` 和 `lifecycle`：

```
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
lifecycle:
  preStop:
    exec:
      command: ["sh", "-c", "sleep 10"]
```

Kubernetes 提供了一种名为探针（`Probe`）的机制用于对 Pod 中的容器状况进行检查，探针由 Kubelet 执行，对容器定期检测，用于确定容器是否存活或者是否可以提供服务。探针根据作用可分为两类：

* 存活探针（`livenessProbe`）

该探针用于确定容器是否为正常运行状态，如果探测结果为 Failure，Kubelet 会杀掉对应的容器，并且根据其重启策略（`Restart Policy`）来决定是否重启；如果没有配置，默认为 Success。

* 就绪探针（`readinessProbe`）

该探针用于确定容器是否可提供服务，如果探测结果为 Failure，控制器 `Endpoints Controller` 会将对应的 Pod IP 从所有匹配上的 Service 的 Endpoint 列表中移除；如果没有配置，默认为 Success。

探针的实现一般有三种方式：

* `exec`

在容器里执行一个命令，如果命令退出时返回 0，则认为检测成功，否则认为失败。比如下面的例子：

```
livenessProbe:
  exec:
    command:
    - cat
    - /tmp/healthy
```

* `tcpSocket`

针对 `容器IP:端口` 的组合进行 TCP 连接检查，如果对应端口处于开放状态，则认为检测成功，否则认为失败。

* `httpGet`

针对 `容器IP:端口:API路径` 的组合进行 HTTP GET 请求，如果 HTTP 响应的状态码在 200~400 之间，则认为检测成功，否则认为失败。比如这里我们就是通过 `/actuator/health/liveness` 和 `/actuator/health/readiness` 端点来检测的。

> 这两个端点默认只在 Kubernetes 环境下才开启。Spring Boot 会自动检测应用程序是否运行在 Kubernetes 环境中（通过环境变量 `*_SERVICE_HOST` 和 `*_SERVICE_PORT` 来判断），你也可以通过配置 `management.endpoint.health.probes.enabled` 手动开启。

另外，Kubernetes 在运行容器的生命周期中提供了钩子（`Container Lifecycle Hooks`），可以在执行相应的生命周期钩子时运行在处理程序中实现的代码。这样的钩子有两个：

* `PostStart`

在创建容器后立即执行，但是无法保证挂钩将在容器 ENTRYPOINT 之前执行。没有参数传递给处理程序。由于无法保证和容器内其它进程启动的顺序相关联，所以不是应用程序进行启动前配置的最佳解决方案。

* `PreStop`

在销毁容器之前即执行，它是阻塞的，所以它必须在删除容器的调用之前完成。没有参数传递给处理程序。很适合作为应用程序优雅退出的机制的，可以定义一系列的行为来释放容器占有的资源、进行通知和告警来实现优雅退出。在这里我们就是通过 `PreStop` 钩子，在容器退出前执行命令 `sleep 10` 等待 10 秒，确保所有的请求都已处理结束。

至此，我们已经实现了最佳实践的第一点和第二点，关于第三点，我们需要通过配置开启服务的优雅退出：

```
server.shutdown=graceful
```

在 Kubernetes 环境中，我们常常使用 `ConfigMap` 来保存配置。

## 使用 `ConfigMap` 配置

创建一个配置文件 `application.properties`，内容如下：

```
server.shutdown=graceful
management.endpoints.web.exposure.include=*
```

其中，`management.endpoints.web.exposure.include=*` 的作用是开启 Actuator 的所有端点，这是为了方便我们检查配置是否生效。然后使用命令 `kubectl create configmap` 创建 `ConfigMap`：

```
$ kubectl create configmap spring-boot-k8s --from-file=./k8s/application.properties
```

使用 `kubectl get configmap` 检查是否创建成功：

```
$ kubectl get configmap spring-boot-k8s -o yaml
apiVersion: v1
data:
  application.properties: "server.shutdown=graceful\r\nmanagement.endpoints.web.exposure.include=*\r\n"
kind: ConfigMap
metadata:
  creationTimestamp: "2022-07-29T23:30:30Z"
  name: spring-boot-k8s
  namespace: default
  resourceVersion: "1712129"
  uid: 6ca3e9c8-bb53-482d-a650-b710f2ed9bcf
```

接下来我们就可以将这个 `ConfigMap` 作为卷挂载到容器中，首先在 `spec` 中定义一个卷：

```
spec:
  volumes:
    - name: config-volume
      configMap:
        name: spring-boot-k8s
```

然后将其挂载到容器中：

```
spec:
  containers:
    - image: aneasystone/spring-boot-k8s:snapshot
      name: spring-boot-k8s
      resources: {}
      volumeMounts:
        - name: config-volume
          mountPath: /workspace/config
```

使用下面的命令使配置生效：

```
$ kubectl apply -f ./k8s
```

等待应用程序就绪之后，再使用 `kubectl port-forward` 开启代理：

```
$ kubectl port-forward svc/spring-boot-k8s 9090:80
```

访问 `http://localhost:9090/actuator/env` 可以看到配置已经生效：

```
{
    "name": "Config resource 'class path resource [config/application.properties]' via location 'optional:classpath:/config/'",
    "properties": {
        "server.shutdown": {
            "value": "graceful",
            "origin": "class path resource [config/application.properties] - 1:17"
        },
        "management.endpoints.web.exposure.include": {
            "value": "*",
            "origin": "class path resource [config/application.properties] - 2:43"
        }
    }
}
```

## 服务发现和负载均衡

这一节我们将使用 [Kustomize](https://kustomize.io/) 来部署一个示例应用 [ryanjbaxter/k8s-spring-workshop](https://github.com/ryanjbaxter/k8s-spring-workshop)。Kustomize 是一款用于 Kubernetes 原生的配置管理的工具，它以无模板的方式来定制应用的配置，直接使用了 Kubernetes 的原生概念，而不需要额外的 DSL 语法，允许用户以一个应用描述文件为基础（Base YAML），然后通过 Overlay 的方式生成最终部署应用所需的描述文件。

一般情况下，应用都会有多套部署环境：开发环境、测试环境、生产环境。多套环境则意味着多套 Kubernetes 应用资源 YAML，而这么多套 YAML 之间只存在一些微小的差异，比如镜像不同、标签不同、副本数不同、数据源配置不同等等。传统的维护方法通常是把一个环境下的 YAML 拷贝出来然后对差异的地方进行修改，这不仅麻烦，而且可能会因为人为疏忽导致配置错误，另外，多套类似的配置也不便于后续的维护和管理。

Kustomize 通过 Base + Overlay 的方式来解决这个问题，在 Base 中定义基础配置，然后通过 Overlay 对 Base 中的配置进行新增或修改。下面是一个简单的例子：

```
demo
├── base
│   ├── deployment.yaml
│   ├── kustomization.yaml
│   └── service.yaml
└── overlays
    └── production
        ├── ingress.yaml
        └── kustomization.yaml
```

在开发或测试环境我们使用 Base 中的 deployment 和 service 部署应用即可，但是在生产环境还要再部署一个 ingress，那么就可以通过 Overlay 补充一个配置文件进来即可。

又或者在生产环境中我们希望将应用的副本数改为 2，这时就可以通过 Patch 的方式修改 Base 里的配置文件。在我们这个示例程序中，就是使用这种方式来部署应用的：

```
kustomize
├── base
│   ├── deployment.yaml
│   ├── kustomization.yaml
│   └── service.yaml
└── multi-replica
    ├── kustomization.yaml
    └── replicas.yaml
```

其中 `multi-replica/kustomization.yaml` 文件的内容如下：

```
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ./../base
patchesStrategicMerge:
  - replicas.yaml
```

可以看到，这个资源的类型为 `Kustomization`。我们通过 `resources` 指定 Base 配置的位置，并通过 `patchesStrategicMerge` 指定使用 `replicas.yaml` 来修改配置。在 `replicas.yaml` 文件中，我们只需要配上要修改的值即可，不用再编写完整的配置文件了：

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: k8s-workshop-name-service
spec:
  replicas: 2
```

有了 Kustomization 配置文件之后，就可以使用 `kustomize build` 生成完整的 Kubernetes 配置，生成的配置可以直接通过 `kubectl apply` 来部署：

```
$ kustomize build "github.com/ryanjbaxter/k8s-spring-workshop/name-service/kustomize/multi-replica/" | kubectl apply -f -
```

从 1.14 版本开始，kubectl 也开始支持使用 kustomization 文件来管理 Kubernetes 对象。 可以通过 `kubectl apply -k` 直接部署：

```
$ kubectl apply -k "github.com/ryanjbaxter/k8s-spring-workshop/name-service/kustomize/multi-replica/"
```

部署完成后，通过 `kubectl get pods` 应该能看到两个 `k8s-workshop-name-service` Pod：

```
$ kubectl get pods --selector app=k8s-workshop-name-service
NAME                                         READY   STATUS    RESTARTS   AGE
k8s-workshop-name-service-85fb6bcd85-ddtnd   1/1     Running   0          6m20s
k8s-workshop-name-service-85fb6bcd85-k492l   1/1     Running   0          6m20s
```

使用 `kubectl port-forward` 将集群内 Service 端口代理到主机的 9090 端口：

```
$ kubectl port-forward svc/k8s-workshop-name-service 9090:80
```

使用 `curl` 确认接口是否能成功响应：

```
$ curl -i http://localhost:9090/; echo
HTTP/1.1 200
k8s-host: k8s-workshop-name-service-85fb6bcd85-ddtnd
Content-Type: text/plain;charset=UTF-8
Content-Length: 5
Date: Sun, 31 Jul 2022 04:24:54 GMT

Ringo
```

注意请求头部的 `k8s-host`，它表示该请求是由哪个 Pod 处理的，我们多请求几次发现，每次返回的都是同一个 Pod，这是因为 `kubectl port-forward` 命令只代理了一个 Pod。

在 Kubernetes 中部署应用时，Kubernetes 会自动根据服务名生成 DNS 记录，所以我们可以直接使用服务名来请求接口，而不用关心每个服务所在 Pod 的真实 IP 地址，此外 Kubernetes 也会使用负载均衡策略将请求路由到不同的 Pod 上。

我们修改 `DemoApplication.java`，新增一个接口，通过 `WebClient` 调用 `k8s-workshop-name-service` 接口：

```
	@GetMapping
	public Mono<String> index() {
		return webClient.get().uri("http://k8s-workshop-name-service")
				.retrieve()
				.toEntity(String.class)
				.map(entity -> {
					String host = entity.getHeaders().get("k8s-host").get(0);
					return "Hello " + entity.getBody() + " from " + host;
				});
	}
```

代码修改完成后，我们重新构建镜像并修改镜像标签：

```
$ ./mvnw spring-boot:build-image -Dspring-boot.build-image.imageName=aneasystone/spring-boot-k8s
$ docker tag aneasystone/spring-boot-k8s:latest aneasystone/spring-boot-k8s:snapshot
```

然后怎么将新构建的镜像重新部署到 Kubernetes 呢？最简单的一种做法是将之前的 Pod 删除：

```
$ kubectl delete pod --selector app=spring-boot-k8s   
pod "spring-boot-k8s-655565dd6-6cblq" deleted
```

这样 Kubernetes 又会自动创建一个新 Pod，使用的自然就是新的镜像了。继续使用 `kubectl port-forward` 代理端口：

```
$ kubectl port-forward svc/spring-boot-k8s 9090:80
```

然后使用下面的 watch 命令每隔 1 秒发一次请求，观察 Pod 是否会变：

```
$ watch -n 1 curl http://localhost:9090
```

可以发现 Pod 并不是每次请求都会变，而是要等很长时间才能观察到变化。（*这可能和 Kubernetes 的负载均衡机制有关？*）如果想要立即观察到变化，可以使用 `kubectl delete pod` 删除该 Pod，请求会立即切到另一个 Pod 上：

```
$ kubectl delete pod k8s-workshop-name-service-56b986b664-wjcr9
```

## 参考

* [【Topical Guides】Spring on Kubernetes](https://spring.io/guides/topicals/spring-on-kubernetes/)
* [kustomize 最简实践](https://zhuanlan.zhihu.com/p/92153378)
* [使用 Kustomize 对 Kubernetes 对象进行声明式管理](https://kubernetes.io/zh-cn/docs/tasks/manage-kubernetes-objects/kustomization/)

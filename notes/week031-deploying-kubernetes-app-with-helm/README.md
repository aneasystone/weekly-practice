# WEEK031 - 使用 Helm 部署 Kubernetes 应用

在 [week013-playing-with-kubernetes](../week013-playing-with-kubernetes/README.md) 中我们学习了如何通过 `Deployment` 部署一个简单的应用服务并通过 `Service` 来暴露它，在真实的场景中，一套完整的应用服务可能还会包含很多其他的 Kubernetes 资源，比如 `DaemonSet`、`Ingress`、`ConfigMap`、`Secret` 等，当用户部署这样一套完整的服务时，他就不得不关注这些底层的 Kubernetes 概念，这对用户非常不友好。

我们知道，几乎每个操作系统都内置了一套软件包管理器，用来方便用户安装、配置、卸载或升级各种系统软件和应用软件，比如 Debian 和 Ubuntu 使用的是 DEB 包管理器 `dpkg` 和 `apt`，CentOS 使用的是 RPM 包管理器 `yum`，Mac OS 有 `Homebrew`，Windows 有 `WinGet` 和 `Chocolatey` 等，另外很多系统还内置了图形界面的应用市场方便用户安装应用，比如 Windows 应用商店、Apple Store、安卓应用市场等，这些都可以算作是包管理器。

使用包管理器安装应用大大降低了用户的使用门槛，他只需要执行一句命令或点击一个安装按钮即可，而不用去关心这个应用需要哪些依赖和哪些配置。那么在 Kubernetes 下能不能也通过这种方式来部署应用服务呢？[Helm](https://helm.sh/zh/) 作为 Kubernetes 的包管理器，解决了这个问题。

## Helm 简介

Helm 是 [Deis 团队](https://deislabs.io/) 于 2015 年发布的一个 Kubernetes 包管理工具，当时 Deis 团队还没有被微软收购，他们在一家名为 Engine Yard 的公司里从事 PaaS 产品 Deis Workflow 的开发，在开发过程中，他们需要将众多的微服务部署到 Kubernetes 集群中，由于在 Kubernetes 里部署服务需要开发者手动编写和维护数量繁多的 Yaml 文件，并且服务的分发和安装也比较繁琐，Matt Butcher 和另外几个同事于是在一次 Hackthon 团建中发起了 Helm 项目。

> Helm 的取名非常有意思，Kubernetes 是希腊语 “舵手” 的意思，而 Helm 是舵手操作的 “船舵”，用来控制船的航行方向。

Helm 引入了 [Chart](https://helm.sh/zh/docs/topics/charts/) 的概念，它也是 Helm 所使用的包格式，可以把它理解成一个描述 Kubernetes 相关资源的文件集合。开发者将自己的应用配置文件打包成 Helm chart 格式，然后发布到 [ArtifactHub](https://artifacthub.io/)，这和你使用 `docker push` 将镜像推送到 DockerHub 镜像仓库一样，之后用户安装你的 Kubernetes 应用只需要一条简单的 Helm 命令就能搞定，极大程度上解决了 Kubernetes 应用维护、分发、安装等问题。

Helm 在 2018 年 6 月加入 CNCF，并在 2020 年 4 月正式毕业，目前已经是 Kubernetes 生态里面不可或缺的明星级项目。

## 快速开始

这一节我们将通过官方的入门示例快速掌握 Helm 的基本用法。

### 安装 Helm

我们首先从 Helm 的 [Github Release](https://github.com/helm/helm/releases) 页面找到最新版本，然后通过 `curl` 将安装包下载下来：

```
$ curl -LO https://get.helm.sh/helm-v3.11.1-linux-amd64.tar.gz
```

然后解压安装包，并将 `helm` 安装到 `/usr/local/bin` 目录：

```
$ tar -zxvf helm-v3.11.1-linux-amd64.tar.gz
$ sudo mv linux-amd64/helm /usr/local/bin/helm
```

这样 Helm 就安装好了，通过 `helm version` 检查是否安装成功：

```
$ helm version
version.BuildInfo{Version:"v3.11.1", GitCommit:"293b50c65d4d56187cd4e2f390f0ada46b4c4737", GitTreeState:"clean", GoVersion:"go1.18.10"}
```

使用 `helm help` 查看 Helm 支持的其他命令和参数。

> 一般来说，直接下载 Helm 二进制文件就可以完成安装，不过官方也提供了一些其他方法来安装 Helm，比如通过 [get_helm.sh](https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3) 脚本来自动安装，或者通过 `yum` 或 `apt` 这些操作系统的包管理器来安装，具体内容可参考官方的 [安装文档](https://helm.sh/zh/docs/intro/install/)。

### 使用 Helm

Helm 安装完成之后，我们就可以使用 Helm 在 Kubernetes 中安装应用了。对于新手来说，最简单的方法是在 [ArtifactHub](https://artifacthub.io/) 上搜索要安装的应用，然后按照文档中的安装步骤来操作即可。比如我们想要部署 Nginx，首先在 ArtifactHub 上进行搜索：

![](./images/search-nginx.png)

注意左侧的 KIND 勾选上 `Helm charts`，搜索出来的结果会有很多条，这些都是由不同的组织或个人发布的，可以在列表中看出发布的组织或个人名称，以及该 Charts 所在的仓库。[Bitnami](https://bitnami.com/) 是 Helm 中最常用的仓库之一，它内置了很多常用的 Kubernetes 应用，于是我们选择进入 [第一条搜索结果](https://artifacthub.io/packages/helm/bitnami/nginx)：

![](./images/bitnami-nginx.png)

这里可以查看关于 Nginx 应用的安装步骤、使用说明、以及支持的配置参数等信息，我们可以点击 `INSTALL` 按钮，会弹出一个对话框，并显示该应用的安装步骤：

![](./images/nginx-install.png)

我们按照它的提示，首先使用 `helm repo add` 将 Bitnami 仓库添加到我们的电脑：

```
$ helm repo add bitnami https://charts.bitnami.com/bitnami
"bitnami" has been added to your repositories
```

然后使用 `helm install` 安装 Nginx 应用：

```
$ helm install my-nginx bitnami/nginx --version 13.2.23
NAME: my-nginx
LAST DEPLOYED: Sat Feb 11 08:58:10 2023
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: nginx
CHART VERSION: 13.2.23
APP VERSION: 1.23.3

** Please be patient while the chart is being deployed **
NGINX can be accessed through the following DNS name from within your cluster:

    my-nginx.default.svc.cluster.local (port 80)

To access NGINX from outside the cluster, follow the steps below:

1. Get the NGINX URL by running these commands:

  NOTE: It may take a few minutes for the LoadBalancer IP to be available.
        Watch the status with: 'kubectl get svc --namespace default -w my-nginx'

    export SERVICE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].port}" services my-nginx)
    export SERVICE_IP=$(kubectl get svc --namespace default my-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    echo "http://${SERVICE_IP}:${SERVICE_PORT}"
```

稍等片刻，Nginx 就安装好了，我们可以使用 `kubectl` 来验证：

```
$ kubectl get deployments
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
my-nginx   1/1     1            1           12m
$ kubectl get svc
NAME             TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
kubernetes       ClusterIP      10.96.0.1        <none>        443/TCP          75d
my-nginx         LoadBalancer   10.111.151.137   localhost     80:31705/TCP     12m
```

访问 `localhost:80` 可以看到 Nginx 已成功启动：

![](./images/nginx.png)

卸载和安装一样也很简单，使用 `helm delete` 命令即可：

```
$ helm delete my-nginx
release "my-nginx" uninstalled
```

我们还可以通过 `--set` 选项来改写 Nginx 的一些参数，比如默认情况下创建的 Service 端口是 80，使用下面的命令将端口改为 8080：

```
$ helm install my-nginx bitnami/nginx --version 13.2.23 \
	--set service.ports.http=8080
```

更多的参数列表可以参考安装文档中的 [`Parameters`](https://artifacthub.io/packages/helm/bitnami/nginx#parameters) 部分。

另外，[`helm`](https://helm.sh/zh/docs/helm/helm/) 命令和它的子命令还支持一些其他选项，比如上面的 `--version` 和 `--set` 都是 [`helm install`](https://helm.sh/zh/docs/helm/helm_install/) 子命令的选项，我们可以使用 `helm` 命令的 `--namespace` 选项将应用部署到指定的命名空间中：

```
$ helm install my-nginx bitnami/nginx --version 13.2.23 \
	--set service.ports.http=8080 \
	--namespace nginx --create-namespace
```

## 常用的 Helm 命令

通过上一节的学习，我们大致了解了 Helm 中三个非常重要的概念：

* `Repository`
* `Chart`
* `Release`

`Repository` 比较好理解，就是存放安装包的仓库，可以使用 `helm env` 查看 `HELM_REPOSITORY_CACHE` 环境变量的值，这就是仓库的本地地址，用于缓存仓库信息以及已下载的安装包：

```
$ helm env | grep HELM_REPOSITORY_CACHE
HELM_REPOSITORY_CACHE="/home/aneasystone/.cache/helm/repository"
```

当我们执行 `helm repo add` 命令时，会将仓库信息缓存到该目录；当我们执行 `helm install` 命令时，也会将安装包下载并缓存到该目录。查看该目录，可以看到我们已经添加的 `bitnami` 仓库信息，还有已下载的 `nginx` 安装包：

```
$ ls /home/aneasystone/.cache/helm/repository
bitnami-charts.txt  bitnami-index.yaml  nginx-13.2.23.tgz
```

这个安装包就被称为 `Chart`，是 Helm 特有的安装包格式，这个安装包中包含了一个 Kubernetes 应用的所有资源文件。而 `Release` 就是安装到 Kubernetes 中的 Chart 实例，每个 Chart 可以在集群中安装多次，每安装一次，就会产生一个 Release。

明白了这三个基本概念，我们就可以这样理解 Helm 的用途：**它先从 `Repository` 中下载 `Chart`，然后将 `Chart` 实例化后以 `Release` 的形式部署到 Kubernetes 集群中**，如下图所示（[图片来源](https://docs.couchbase.com/cloud-native-database/helm-overview.html)）：

![](./images/helm-overview.png)

而绝大多数的 Helm 命令，都是围绕着这三大概念进行的。

https://stackoverflow.com/questions/62371422/how-to-list-full-url-about-helm-search-url-in-v3-2-1

## 制作自己的 Helm Chart

如前所述，Helm 的安装包被称为 `Chart`，这个安装包中包含了一个 Kubernetes 应用的所有资源文件。我们不妨将本地仓库中的 Nginx 安装包解压开来，看看里面都有些什么：

```
$ tar zxvf nginx-13.2.23.tgz
$ tree nginx
nginx
├── Chart.lock
├── Chart.yaml
├── README.md
├── charts
│   └── common
│       ├── Chart.yaml
│       ├── README.md
│       ├── templates
│       │   ├── _affinities.tpl
│       │   ├── _capabilities.tpl
│       │   ├── _errors.tpl
│       │   ├── _images.tpl
│       │   ├── _ingress.tpl
│       │   ├── _labels.tpl
│       │   ├── _names.tpl
│       │   ├── _secrets.tpl
│       │   ├── _storage.tpl
│       │   ├── _tplvalues.tpl
│       │   ├── _utils.tpl
│       │   ├── _warnings.tpl
│       │   └── validations
│       │       ├── _cassandra.tpl
│       │       ├── _mariadb.tpl
│       │       ├── _mongodb.tpl
│       │       ├── _mysql.tpl
│       │       ├── _postgresql.tpl
│       │       ├── _redis.tpl
│       │       └── _validations.tpl
│       └── values.yaml
├── templates
│   ├── NOTES.txt
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── extra-list.yaml
│   ├── health-ingress.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── pdb.yaml
│   ├── prometheusrules.yaml
│   ├── server-block-configmap.yaml
│   ├── serviceaccount.yaml
│   ├── servicemonitor.yaml
│   ├── svc.yaml
│   └── tls-secrets.yaml
├── values.schema.json
└── values.yaml

5 directories, 41 files
```

## 参考

1. [Helm | 快速入门指南](https://helm.sh/zh/docs/intro/quickstart/)
1. [Helm | 使用Helm](https://helm.sh/zh/docs/intro/using_helm/)
1. [Helm | 项目历史](https://helm.sh/zh/docs/community/history/)
1. [微软 Deis Labs 的传奇故事](https://zhuanlan.zhihu.com/p/496603933)
1. [Helm Dashboard](https://github.com/komodorio/helm-dashboard)
1. [Kubernetes Tutorials ｜ k8s 教程](https://github.com/guangzhengli/k8s-tutorials#helm)
1. [使用Helm管理kubernetes应用](https://jimmysong.io/kubernetes-handbook/practice/helm.html)

# WEEK023 - 搭建自己的镜像仓库

镜像仓库（Docker Registry）是用于存储和管理镜像的地方，方便将镜像分发到世界各地，镜像仓库一般分为公共仓库和私有仓库两种形式。

Docker 官方的 [Docker Hub](https://hub.docker.com/) 是最常用的公共仓库之一，包含很多高质量的官方镜像，这也是 Docker 默认使用的仓库，除此之外，还有 Red Hat 的 [Quay.io](https://quay.io/repository/)，Google 的 [Google Container Registry](https://cloud.google.com/container-registry/)（Kubernetes 就是使用 GCR 作为默认的镜像仓库），以及 GitHub 的 [ghcr.io](https://docs.github.com/cn/packages/working-with-a-github-packages-registry/working-with-the-container-registry) 等。国内一些云服务商也提供类似的服务，比如 [网易云镜像服务](https://c.163.com/hub#/m/library/)、[DaoCloud 镜像市场](https://hub.daocloud.io/)、[阿里云容器镜像服务（ACR）](https://www.aliyun.com/product/acr?source=5176.11533457) 等。另外还有些服务商提供了针对 Docker Hub 的镜像服务（Registry Mirror），这些镜像服务被称为 **加速器**，比如 [DaoCloud 加速器](https://www.daocloud.io/mirror)，使用加速器会直接从国内的地址下载 Docker Hub 的镜像，比直接从 Docker Hub 下载快得多。

除公开仓库外，用户也可以在本地搭建私有镜像仓库。通过官方提供的 [Docker Registry](https://hub.docker.com/_/registry/) 镜像，可以很容易搭建一个自己的镜像仓库服务，这个仓库服务提供了 [Docker Registry API](https://docs.docker.com/registry/spec/api/) 相关的接口，并没有图形界面，不过对 Docker 命令来说已经足够了。如果还需要一些高级特性，可以尝试 [Harbor](https://github.com/goharbor/harbor) 或 [Sonatype Nexus](https://www.sonatype.com/products/nexus-repository)，他们不仅提供了图形界面，还具有镜像维护、用户管理、访问控制等高级功能。

## 使用 Docker Registry 搭建私有镜像仓库

首先下载 [Docker Registry](https://hub.docker.com/_/registry/) 镜像：

```
$ docker pull registry:latest
```

目前最新的 registry 版本是 2.8，它是基于 [Distribution](https://github.com/distribution/distribution) 实现的，老版本的 registry 是基于 [docker-registry](https://github.com/docker-archive/docker-registry) 实现的，现在已经几乎不用了。*Distribution* 是 [OCI Distribution Specification](https://github.com/opencontainers/distribution-spec) 的开源实现，很多其他的镜像仓库项目如 Docker Hub、GitHub Container Registry、GitLab Container Registry、DigitalOcean Container Registry、Harbor Project、VMware Harbor Registry 都是以 *Distribution* 为基础开发的。

使用 docker 命令启动镜像仓库：

```
$ docker run -d -p 5000:5000 --name registry registry:latest
```

这样我们的私有镜像仓库就搭建好了。为了验证这个镜像仓库是否可用，我们可以从官方随便下载一个镜像（这里我使用的是 `hello-world` 镜像），然后通过 `docker tag` 在镜像名前面加上私有仓库的地址 `localhost:5000/`，再通过 `docker push` 就可以将这个镜像推送到我们的私有仓库里了：

```
$ docker pull hello-world
$ docker tag hello-world localhost:5000/hello-world
$ docker push localhost:5000/hello-world
```

### 使用 Docker Registry API 访问仓库

我们可以通过 [Docker Registry API](https://docs.docker.com/registry/spec/api/) 暴露的一些接口来访问仓库，比如使用 `/v2/_catalog` 接口查询仓库中有哪些镜像：

```
$ curl -s http://localhost:5000/v2/_catalog | jq
{
  "repositories": [
    "hello-world"
  ]
}
```

使用 `/v2/<name>/tags/list` 接口查询某个镜像的标签：

```
$ curl -s http://localhost:5000/v2/hello-world/tags/list | jq
{
  "name": "hello-world",
  "tags": [
    "latest"
  ]
}
```

使用 `/v2/<name>/manifests/<reference>` 接口查询某个镜像版本的详细信息：

```
$ curl -s http://localhost:5000/v2/hello-world/manifests/latest | jq
{
  "schemaVersion": 1,
  "name": "hello-world",
  "tag": "latest",
  "architecture": "amd64",
  "fsLayers": [
    {
      "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
    },
    {
      "blobSum": "sha256:2db29710123e3e53a794f2694094b9b4338aa9ee5c40b930cb8063a1be392c54"
    }
  ],
  "history": [
    {
      "v1Compatibility": "{\"architecture\":\"amd64\",\"config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/hello\"],\"Image\":\"sha256:b9935d4e8431fb1a7f0989304ec86b3329a99a25f5efdc7f09f3f8c41434ca6d\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"container\":\"8746661ca3c2f215da94e6d3f7dfdcafaff5ec0b21c9aff6af3dc379a82fbc72\",\"container_config\":{\"Hostname\":\"8746661ca3c2\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\",\"-c\",\"#(nop) \",\"CMD [\\\"/hello\\\"]\"],\"Image\":\"sha256:b9935d4e8431fb1a7f0989304ec86b3329a99a25f5efdc7f09f3f8c41434ca6d\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":{}},\"created\":\"2021-09-23T23:47:57.442225064Z\",\"docker_version\":\"20.10.7\",\"id\":\"a1f125167a7f2cffa48b7851ff3f75e983824c16e8da61f20765eb55f7b3a594\",\"os\":\"linux\",\"parent\":\"cd13bf215b21e9bc78460fa5070860a498671e2ac282d86d15042cf0c26e6e8b\",\"throwaway\":true}"
    },
    {
      "v1Compatibility": "{\"id\":\"cd13bf215b21e9bc78460fa5070860a498671e2ac282d86d15042cf0c26e6e8b\",\"created\":\"2021-09-23T23:47:57.098990892Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop) COPY file:50563a97010fd7ce1ceebd1fa4f4891ac3decdf428333fb2683696f4358af6c2 in / \"]}}"
    }
  ],
  "signatures": [
    {
      "header": {
        "jwk": {
          "crv": "P-256",
          "kid": "6GC6:JFLS:HP3P:WWBW:V4RI:BJKW:64GB:NSAO:Y4U6:UT6M:MSLJ:QG6K",
          "kty": "EC",
          "x": "Q1gHvt0A-Q-Pu8hfm2o-hLST0b-XZlEQcn9kYHZzAi0",
          "y": "oNddnJzLNOMcRcEebuEqZiapZHHmQSZHnnnaSkvYUaE"
        },
        "alg": "ES256"
      },
      "signature": "NthpjcYe39XSmnKRz9dlSWZBcpIgqIXuFGhQ4bxALK97NsWAZPE6CSiLwEn3ECjm1ovKzjJthOAuK_CW92ju-Q",
      "protected": "eyJmb3JtYXRMZW5ndGgiOjIwOTIsImZvcm1hdFRhaWwiOiJDbjAiLCJ0aW1lIjoiMjAyMi0wOS0xNFQyMzo1ODozM1oifQ"
    }
  ]
}
```

除了这三个比较常用的查询类接口，Docker Registry API 还有一些用于上传和下载的接口，具体的内容可以查看这里的 [接口列表](https://docs.docker.com/registry/spec/api/#detail)。

## 使用 `crane` 工具操作仓库

## 使用 Docker Registry UI 图形界面

## 使用 Harbar 搭建私有镜像仓库

## 参考

1. [仓库 - Docker — 从入门到实践](https://yeasy.gitbook.io/docker_practice/basic_concept/repository)
1. [私有仓库 - Docker — 从入门到实践](https://yeasy.gitbook.io/docker_practice/repository/registry)
1. [Docker Registry](https://docs.docker.com/registry/)
1. [Docker Registry UI](https://github.com/Joxit/docker-registry-ui)
1. [How to delete images from a private docker registry?](https://stackoverflow.com/questions/25436742/how-to-delete-images-from-a-private-docker-registry)
1. [你必须知道的Docker镜像仓库的搭建](https://www.cnblogs.com/edisonchou/p/docker_registry_repository_setup_introduction.html)
1. [distribution/distribution](https://github.com/distribution/distribution) - The toolkit to pack, ship, store, and deliver container content
1. [SUSE/Portus](https://github.com/SUSE/Portus) - Authorization service and frontend for Docker registry (v2)
1. [google/go-containerregistry](https://github.com/google/go-containerregistry) - Go library and CLIs for working with container registries

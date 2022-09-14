# WEEK023 - 搭建自己的镜像仓库

镜像仓库（Docker Registry）是用于存储和管理镜像的地方，方便将镜像分发到世界各地，镜像仓库一般分为公共仓库和私有仓库两种形式。

Docker 官方的 [Docker Hub](https://hub.docker.com/) 是最常用的公共仓库，包含很多高质量的官方镜像，这也是 Docker 默认使用的仓库，除此之外，还有 Red Hat 的 [Quay.io](https://quay.io/repository/)，Google 的 [Google Container Registry](https://cloud.google.com/container-registry/)（Kubernetes 就是使用 GCR 作为默认的镜像仓库），以及 GitHub 的 [ghcr.io](https://docs.github.com/cn/packages/working-with-a-github-packages-registry/working-with-the-container-registry) 等。国内一些云服务商也提供类似的服务，比如 [网易云镜像服务](https://c.163.com/hub#/m/library/)、[DaoCloud 镜像市场](https://hub.daocloud.io/)、[阿里云容器镜像服务（ACR）](https://www.aliyun.com/product/acr?source=5176.11533457) 等。另外还有些服务商提供了针对 Docker Hub 的镜像服务（Registry Mirror），这些镜像服务被称为 **加速器**，比如 [DaoCloud 加速器](https://www.daocloud.io/mirror)，使用加速器会直接从国内的地址下载 Docker Hub 的镜像，比直接从 Docker Hub 下载快得多。

除公开仓库外，用户也可以在本地搭建私有镜像仓库。通过官方提供的 [Docker Registry](https://hub.docker.com/_/registry/) 镜像，可以很容易搭建一个自己的镜像仓库服务，这个仓库服务提供了 [Docker Registry API](https://docs.docker.com/registry/spec/api/) 相关的接口，并没有图形界面，不过对 Docker 命令来说已经足够了。如果还需要一些高级特性，可以尝试 [Harbor](https://github.com/goharbor/harbor) 或 [Sonatype Nexus](https://www.sonatype.com/products/nexus-repository)，他们不仅提供了图形界面，还具有镜像维护、用户管理、访问控制等高级功能。

## 使用 Docker Registry 搭建私有镜像仓库

## 使用 Docker Registry API 访问仓库

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
1. [docker-archive/docker-registry](https://github.com/docker-archive/docker-registry)
1. [distribution/distribution](https://github.com/distribution/distribution) - The toolkit to pack, ship, store, and deliver container content
1. [SUSE/Portus](https://github.com/SUSE/Portus) - Authorization service and frontend for Docker registry (v2)
1. [google/go-containerregistry](https://github.com/google/go-containerregistry) - Go library and CLIs for working with container registries

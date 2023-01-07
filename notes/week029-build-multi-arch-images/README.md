# WEEK029 - 构建多架构容器镜像实战

最近在一个国产化项目中遇到了这样一个场景，在同一个 Kubernetes 集群中的节点是混合架构的，也就是说，其中某些节点的 CPU 架构是 x86 的，而另一些节点是 ARM 的。为了让我们的镜像在这样的环境下运行，一种最简单的做法是根据节点类型为其打上相应的标签，然后针对不同的架构构建不同的镜像，比如 `demo:v1-amd64` 和 `demo:v1-arm64`，然后还需要写两套 YAML：一套使用 `demo:v1-amd64` 镜像，并通过 `nodeSelector` 选择 x86 的节点，另一套使用 `demo:v1-arm64` 镜像，并通过 `nodeSelector` 选择 ARM 的节点。很显然，这种做法不仅非常繁琐，而且管理起来也相当麻烦，如果集群中还有其他架构的节点，那么维护成本将成倍增加。

解决这个问题更好的方法是使用 **多架构镜像（ multi-arch images ）**。

### docker manifest

https://docs.docker.com/engine/reference/commandline/manifest/

https://github.com/estesp/manifest-tool

### docker buildx

https://github.com/docker/buildx

https://github.com/docker/buildx#building-multi-platform-images

https://github.com/moby/buildkit/blob/master/docs/multi-platform.md

## 参考

1. [Faster Multi-platform builds: Dockerfile cross-compilation guide (Part 1)](https://medium.com/@tonistiigi/faster-multi-platform-builds-dockerfile-cross-compilation-guide-part-1-ec087c719eaf)
1. [Multi-arch build and images, the simple way](https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/)
1. [Docker: Exporting Image for Multiple Architectures](https://stackoverflow.com/questions/73515781/docker-exporting-image-for-multiple-architectures)
1. [如何使用 docker buildx 构建跨平台 Go 镜像](https://waynerv.com/posts/building-multi-architecture-images-with-docker-buildx/)
1. [构建多种系统架构支持的 Docker 镜像](https://yeasy.gitbook.io/docker_practice/image/manifest)
1. [使用buildx来构建支持多平台的Docker镜像(Mac系统)](https://blog.cnscud.com/docker/2021/11/17/docker-buildx.html)
1. [使用 Docker Buildx 构建多种系统架构镜像](https://www.51cto.com/article/678858.html)
1. [使用 buildx 构建多平台 Docker 镜像](https://icloudnative.io/posts/multiarch-docker-with-buildx/)
1. [基于QEMU和binfmt-misc透明运行不同架构程序](https://blog.lyle.ac.cn/2020/04/14/transparently-running-binaries-from-any-architecture-in-linux-with-qemu-and-binfmt-misc/)
1. [多架构镜像三部曲（一）组合](https://blog.csdn.net/mycosmos/article/details/123587243)
1. [多架构镜像三部曲（二）构建](https://blog.csdn.net/mycosmos/article/details/125020271)

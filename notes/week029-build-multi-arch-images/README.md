# WEEK029 - 构建多架构容器镜像实战

最近在一个国产化项目中遇到了这样一个场景，在同一个 Kubernetes 集群中的节点是混合架构的，也就是说，其中某些节点的 CPU 架构是 x86 的，而另一些节点是 ARM 的。为了让我们的镜像在这样的环境下运行，一种最简单的做法是根据节点类型为其打上相应的标签，然后针对不同的架构构建不同的镜像，比如 `demo:v1-amd64` 和 `demo:v1-arm64`，然后还需要写两套 YAML：一套使用 `demo:v1-amd64` 镜像，并通过 `nodeSelector` 选择 x86 的节点，另一套使用 `demo:v1-arm64` 镜像，并通过 `nodeSelector` 选择 ARM 的节点。很显然，这种做法不仅非常繁琐，而且管理起来也相当麻烦，如果集群中还有其他架构的节点，那么维护成本将成倍增加。

你可能知道，每个 Docker 镜像都是通过一个 manifest 来描述的，manifest 中包含了这个镜像的基本信息，包括它的 mediaType、大小、摘要以及每一层的分层信息等。可以使用 `docker manifest inspect` 查看某个镜像的 manifest 信息：

```
$ docker manifest inspect aneasystone/hello-actuator:v1
{
        "schemaVersion": 2,
        "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
        "config": {
                "mediaType": "application/vnd.docker.container.image.v1+json",
                "size": 3061,
                "digest": "sha256:d6d5f18d524ce43346098c5d5775de4572773146ce9c0c65485d60b8755c0014"
        },
        "layers": [
                {
                        "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
                        "size": 2811478,
                        "digest": "sha256:5843afab387455b37944e709ee8c78d7520df80f8d01cf7f861aae63beeddb6b"
                },
                {
                        "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
                        "size": 928436,
                        "digest": "sha256:53c9466125e464fed5626bde7b7a0f91aab09905f0a07e9ad4e930ae72e0fc63"
                },
                {
                        "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
                        "size": 186798299,
                        "digest": "sha256:d8d715783b80cab158f5bf9726bcada5265c1624b64ca2bb46f42f94998d4662"
                },
                {
                        "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
                        "size": 19609795,
                        "digest": "sha256:112ce4ba7a4e8c2b5bcf3f898ae40a61b416101eba468397bb426186ee435281"
                }
        ]
}
```

> 可以加上 `--verbose` 查看更详细的信息，包括该 manifest 引用的镜像标签和架构信息：
> 
> ```
> $ docker manifest inspect --verbose aneasystone/hello-actuator:v1
> {
>         "Ref": "docker.io/aneasystone/hello-actuator:v1",
>         "Descriptor": {
>                 "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
>                 "digest": "sha256:f16a1fcd331a6d196574a0c0721688360bf53906ce0569bda529ba09335316a2",
>                 "size": 1163,
>                 "platform": {
>                         "architecture": "amd64",
>                         "os": "linux"
>                 }
>         },
>         "SchemaV2Manifest": {
>                 ...
>         }
> }
> ```

我们一般不会直接使用 manifest，而是通过标签来关联它，方便人们使用。从上面的输出结果可以看出，该 manifest 通过 `docker.io/aneasystone/hello-actuator:v1` 这个镜像标签来关联，支持的平台是 `linux/amd64`，该镜像有四个分层，另外注意这里的 `mediaType` 字段，它的值是 `application/vnd.docker.distribution.manifest.v2+json`，表示这是 Docker 镜像格式（如果是 `application/vnd.oci.image.manifest.v1+json` 表示 OCI 镜像）。

可以看出这个镜像标签只关联了一个 manifest ，而一个 manifest 只对应一种架构；如果同一个镜像标签能关联多个 manifest ，不同的 manifest 对应不同的架构，那么当我们通过这个镜像标签启动容器时，容器引擎就可以自动根据当前系统的架构找到对应的 manifest 并下载对应的镜像。实际上这就是 **多架构镜像（ multi-arch images ）** 的基本原理，我们把这里的多个 manifest 合称为 [manifest list](https://docs.docker.com/registry/spec/manifest-v2-2/#manifest-list)（ 在 OCI 规范中被称为 [image index](https://github.com/opencontainers/image-spec/blob/v1.0.0/image-index.md) ），镜像标签不仅可以关联 manifest，也可以关联 manifest list。

可以使用 `docker manifest inspect` 查看某个多架构镜像的 manifest list 信息：

```
$ docker manifest inspect alpine:3.17
{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.list.v2+json",
   "manifests": [
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 528,
         "digest": "sha256:c0d488a800e4127c334ad20d61d7bc21b4097540327217dfab52262adc02380c",
         "platform": {
            "architecture": "amd64",
            "os": "linux"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 528,
         "digest": "sha256:ecc4c9eff5b0c4de6be6b4b90b5ab2c2c1558374852c2f5854d66f76514231bf",
         "platform": {
            "architecture": "arm",
            "os": "linux",
            "variant": "v6"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 528,
         "digest": "sha256:4c679bd1e6b6516faf8466986fc2a9f52496e61cada7c29ec746621a954a80ac",
         "platform": {
            "architecture": "arm",
            "os": "linux",
            "variant": "v7"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 528,
         "digest": "sha256:af06af3514c44a964d3b905b498cf6493db8f1cde7c10e078213a89c87308ba0",
         "platform": {
            "architecture": "arm64", 
            "os": "linux",
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 528,
         "digest": "sha256:af6a986619d570c975f9a85b463f4aa866da44c70427e1ead1fd1efdf6150d38",
         "platform": {
            "architecture": "386", 
            "os": "linux"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 528,
         "digest": "sha256:a7a53c2331d0c5fedeaaba8d716eb2b06f7a9c8d780407d487fd0fbc1244f7e6",
         "platform": {
            "architecture": "ppc64le",
            "os": "linux"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 528,
         "digest": "sha256:07afab708df2326e8503aff2f860584f2bfe7a95aee839c8806897e808508e12",
         "platform": {
            "architecture": "s390x",
            "os": "linux"
         }
      }
   ]
}
```

这里的 `alpine:3.17` 就是一个多架构镜像，从输出结果可以看到 `mediaType` 是 `application/vnd.docker.distribution.manifest.list.v2+json`，说明这个镜像标签关联的是一个 manifest list，它包含了多个 manifest，支持 amd64、arm/v6、arm/v7、arm64、i386、ppc64le、s390x 多个架构。我们也可以直接在 [Docker Hub](https://hub.docker.com/_/alpine/tags) 上看到这些信息：

![](./images/alpine-image.png)

很显然，在我们这个混合架构的 Kubernetes 集群中，这个镜像是可以直接运行的。我们也可以将我们的应用构建成这样的多架构镜像，那么在这个 Kubernetes 集群中就可以自由地运行我们自己的应用了，这种方法比上面那种为每个架构构建一个镜像的方法要优雅得多。

那么，我们要如何构建这样的多架构镜像呢？一般来说，如果你使用 Docker 作为你的构建工具，通常有两种方法：`docker manifest` 和 `docker buildx`。

### 使用 `docker manifest` 创建多架构镜像

`docker build` 是最常用的镜像构建命令，首先，我们创建一个 `Dockerfile` 文件，内容如下：

```
FROM alpine:3.17
CMD ["echo", "Hello"]
```

然后使用 `docker build` 构建镜像：

```
$ docker build -f Dockerfile -t aneasystone/demo:v1 .
```

这样一个简单的镜像就构建好了，使用 `docker run` 对其进行测试：

```
$ docker run --rm -it aneasystone/demo:v1
Hello
```

非常顺利，镜像能正常运行。不过这样构建的镜像有一个问题，Docker Engine 是根据当前我们的系统自动拉取基础镜像的，我的系统是 x86 的，所以拉取的 alpine:3.17 镜像架构是 `linux/amd64` 的：

```
$ docker image inspect alpine:3.17 | grep Architecture

        "Architecture": "amd64",
```

如果要构建其他架构的镜像，可以有三种办法。第一种是最原始的方法，Docker 官方为每种 [不同的架构创建了不同的独立账号](https://github.com/docker-library/official-images#architectures-other-than-amd64)，比如下面是一些常用的账号：

* ARMv6 32-bit (arm32v6): https://hub.docker.com/u/arm32v6/
* ARMv7 32-bit (arm32v7): https://hub.docker.com/u/arm32v7/
* ARMv8 64-bit (arm64v8): https://hub.docker.com/u/arm64v8/
* Linux x86-64 (amd64): https://hub.docker.com/u/amd64/
* Windows x86-64 (windows-amd64): https://hub.docker.com/u/winamd64/

所以我们就可以通过 `amd64/alpine` 和 `arm64v8/alpine` 来拉取相应架构的镜像，我们对 `Dockerfile` 文件稍微修改一下：

```
ARG ARCH=amd64
FROM ${ARCH}/alpine:3.17
CMD ["echo", "Hello"]
```

然后使用 `--build-arg` 参数来构建不同架构的镜像：

```
$ docker build --build-arg ARCH=amd64 -f Dockerfile-arg -t aneasystone/demo:v1-amd64 .
$ docker build --build-arg ARCH=arm64v8 -f Dockerfile-arg -t aneasystone/demo:v1-arm64 .
```

不过从 2017 年 9 月开始，一个镜像可以支持多个架构了，这种方法就渐渐不用了。第二种办法就是直接使用 `alpine:3.17` 这个基础镜像，通过 `FROM` 指令的 `--platform` 参数，让 Docker Engine 自动拉取特定架构的镜像。我们新建两个文件 `Dockerfile-amd64` 和 `Dockerfile-arm64`，`Dockerfile-amd64` 文件内容如下：

```
FROM --platform=linux/amd64 alpine:3.17
CMD ["echo", "Hello"]
```

`Dockerfile-arm64` 文件内容如下：

```
FROM --platform=linux/arm64 alpine:3.17
CMD ["echo", "Hello"]
```

然后使用 `docker build` 再次构建镜像即可：

```
$ docker build --pull -f Dockerfile-amd64 -t aneasystone/demo:v1-amd64 .
$ docker build --pull -f Dockerfile-arm64 -t aneasystone/demo:v1-arm64 .
```

> 注意这里的 `--pull` 参数，强制要求 Docker Engine 拉取基础镜像，要不然第二次构建时会使用第一次的缓存，这样基础镜像就不对了。

第三种方法不用修改 `Dockerfile` 文件，因为 `docker build` 也支持 `--platform` 参数，我们只需要像下面这样构建镜像即可：

```
$ docker build --pull --platform=linux/amd64 -f Dockerfile -t aneasystone/demo:v1-amd64 .
$ docker build --pull --platform=linux/arm64 -f Dockerfile -t aneasystone/demo:v1-arm64 .
```

> 在执行 `docker build` 命令时，可能会遇到下面这样的报错信息：
> 
> ```
> $ docker build -f Dockerfile-arm64 -t aneasystone/demo:v1-arm64 .
> [+] Building 1.2s (3/3) FINISHED
>  => [internal] load build definition from > Dockerfile-arm64                   0.0s
>  => => transferring dockerfile: > 37B                                          0.0s
>  => [internal] load .> dockerignore                                            0.0s
>  => => transferring context: > 2B                                              0.0s
>  => ERROR [internal] load metadata for docker.io/library/alpine:3.> 17         1.1s
> ------
>  > [internal] load metadata for docker.io/library/alpine:3.17:
> ------
> failed to solve with frontend dockerfile.v0: failed to create LLB > definition: unexpected status code [manifests 3.17]: 403 Forbidden
> ```
>
> 根据 [这里](https://github.com/docker/buildx/issues/680) 的信息，修改 Docker Daemon 的配置文件，将 `buildkit` 设置为 false 即可：
>
> ```
>   "features": {
>     "buildkit": false
>   },
> ```

构建完不同架构的镜像后，我们就可以使用 [docker manifest](https://docs.docker.com/engine/reference/commandline/manifest/) 命令创建 manifest list，生成自己的多架构镜像了。由于目前创建 manifest list 必须引用远程仓库中的镜像，所以在这之前，我们需要先将刚刚生成的两个镜像推送到镜像仓库中：

```
$ docker push aneasystone/demo:v1-amd64
$ docker push aneasystone/demo:v1-arm64
```

然后使用 `docker manifest create` 创建一个 manifest list，包含我们的两个镜像：

```
$ docker manifest create aneasystone/demo:v1 \
    --amend aneasystone/demo:v1-amd64 \
    --amend aneasystone/demo:v1-arm64
```

最后将该 manifest list 也推送到镜像仓库中就大功告成了：

```
$ docker manifest push aneasystone/demo:v1
```

可以使用 `docker manifest inspect` 查看这个镜像的 manifest list 信息：

```
$ docker manifest inspect aneasystone/demo:v1
{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.list.v2+json",
   "manifests": [
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 528,
         "digest": "sha256:170c4a5295f928a248dc58ce500fdb5a51e46f17866369fdcf4cbab9f7e4a1ab",
         "platform": {
            "architecture": "amd64",
            "os": "linux"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 528,
         "digest": "sha256:3bb9c02263447e63c193c1196d92a25a1a7171fdacf6a29156f01c56989cf88b",
         "platform": {
            "architecture": "arm64",
            "os": "linux",
            "variant": "v8"
         }
      }
   ]
}
```

也可以在 [Docker Hub](https://hub.docker.com/repository/docker/aneasystone/demo/tags) 上看到这个镜像的架构信息：

![](./images/demo-image.png)

### 使用 `docker buildx` 创建多架构镜像

从上一节可以看出，使用 `docker manifest` 来构建多架构镜像的步骤大致分为以下四步：

1. 使用 `docker build` 依次构建每个架构的镜像；
1. 使用 `docker push` 将镜像推送到镜像仓库；
1. 使用 `docker manifest create` 创建一个 manifest list，包含上面的每个镜像；
1. 使用 `docker manifest push` 将 manifest list 推送到镜像仓库；

每次构建多架构镜像都要经历这么多步骤还是非常麻烦的，这一节将介绍一种更方便的方式，使用 `docker buildx` 来创建多架构镜像。

[buildx](https://github.com/docker/buildx) 是一款 Docker CLI 插件，它对 [Moby BuildKit](https://github.com/moby/buildkit) 的构建功能进行了大量的扩展，同时在使用体验上还保持和 `docker build` 一样，用户可以很快上手。如果你的系统是 Windows 或 MacOS，`buildx` 已经内置在 [Docker Desktop](https://docs.docker.com/desktop/) 里了，无需额外安装；如果你的系统是 Linux，可以使用 DEB 或 RPM 包的形式安装，也可以手工安装，具体安装步骤参考 [官方文档](https://github.com/docker/buildx#installing)。

使用 `docker buildx` 创建多架构镜像只需简单一行命令即可：

```
$ docker buildx build --platform=linux/amd64,linux/arm64 -t aneasystone/demo:v2 .
```

不过第一次执行这行命令时会报下面这样的错：

```
ERROR: multiple platforms feature is currently not supported for docker driver. Please switch to a different driver (eg. "docker buildx create --use")
```

这是因为 `buildx` 默认使用的 **构建器（ builder ）** 驱动是 `docker driver`，它不支持同时构建多个 platform 的镜像，我们可以使用 `docker buildx create` 创建其他驱动的构建器（ 关于 `buildx` 的四种驱动以及它们支持的特性可以 [参考这里](https://docs.docker.com/build/drivers/) ）：

```
$ docker buildx create --use
nice_cartwright
```

这样创建的构建器驱动是 `docker-container driver`，它目前还没有启动：

```
$ docker buildx ls
NAME/NODE          DRIVER/ENDPOINT                STATUS   BUILDKIT PLATFORMS
nice_cartwright *  docker-container
  nice_cartwright0 npipe:////./pipe/docker_engine inactive
default            docker
  default          default                        running  20.10.17 linux/amd64, linux/arm64, ...
```

当执行 `docker buildx build` 时会自动启动构建器：

```
$ docker buildx build --platform=linux/amd64,linux/arm64 -t aneasystone/demo:v2 .
[+] Building 14.1s (7/7) FINISHED
 => [internal] booting buildkit                                                                                                            1.2s 
 => => starting container buildx_buildkit_nice_cartwright0                                                                                 1.2s 
 => [internal] load build definition from Dockerfile                                                                                       0.1s 
 => => transferring dockerfile: 78B                                                                                                        0.0s 
 => [internal] load .dockerignore                                                                                                          0.0s 
 => => transferring context: 2B                                                                                                            0.0s 
 => [linux/amd64 internal] load metadata for docker.io/library/alpine:3.17                                                                12.3s 
 => [linux/arm64 internal] load metadata for docker.io/library/alpine:3.17                                                                12.2s 
 => [linux/arm64 1/1] FROM docker.io/library/alpine:3.17@sha256:f271e74b17ced29b915d351685fd4644785c6d1559dd1f2d4189a5e851ef753a           0.2s 
 => => resolve docker.io/library/alpine:3.17@sha256:f271e74b17ced29b915d351685fd4644785c6d1559dd1f2d4189a5e851ef753a                       0.1s 
 => [linux/amd64 1/1] FROM docker.io/library/alpine:3.17@sha256:f271e74b17ced29b915d351685fd4644785c6d1559dd1f2d4189a5e851ef753a           0.2s 
 => => resolve docker.io/library/alpine:3.17@sha256:f271e74b17ced29b915d351685fd4644785c6d1559dd1f2d4189a5e851ef753a                       0.1s 
WARNING: No output specified with docker-container driver. Build result will only remain in the build cache. To push result image into registry use --push or to load image into docker use --load
```

使用 `docker ps` 可以看到正在运行的构建器，实际上就是 [buildkitd 服务](https://github.com/moby/buildkit#starting-the-buildkitd-daemon)，`docker buildx build` 为我们自动下载了 `moby/buildkit:buildx-stable-1` 镜像并运行：

```
$ docker ps
CONTAINER ID   IMAGE                           COMMAND       CREATED         STATUS         PORTS     NAMES
e776505153c0   moby/buildkit:buildx-stable-1   "buildkitd"   7 minutes ago   Up 7 minutes             buildx_buildkit_nice_cartwright0
```

上面的构建结果中有一行 WARNING 信息，意思是我们没有指定 output 参数，所以构建的结果只存在于构建缓存中，如果要将构建的镜像推送到镜像仓库，可以加上一个 `--push` 参数：

```
$ docker buildx build --push --platform=linux/amd64,linux/arm64 -t aneasystone/demo:v2 .
[+] Building 14.4s (10/10) FINISHED
 => [internal] load build definition from Dockerfile                                                                                       0.1s 
 => => transferring dockerfile: 78B                                                                                                        0.0s 
 => [internal] load .dockerignore                                                                                                          0.0s 
 => => transferring context: 2B                                                                                                            0.0s 
 => [linux/arm64 internal] load metadata for docker.io/library/alpine:3.17                                                                 9.1s 
 => [linux/amd64 internal] load metadata for docker.io/library/alpine:3.17                                                                 9.0s 
 => [auth] library/alpine:pull token for registry-1.docker.io                                                                              0.0s 
 => [linux/arm64 1/1] FROM docker.io/library/alpine:3.17@sha256:f271e74b17ced29b915d351685fd4644785c6d1559dd1f2d4189a5e851ef753a           0.1s 
 => => resolve docker.io/library/alpine:3.17@sha256:f271e74b17ced29b915d351685fd4644785c6d1559dd1f2d4189a5e851ef753a                       0.1s 
 => [linux/amd64 1/1] FROM docker.io/library/alpine:3.17@sha256:f271e74b17ced29b915d351685fd4644785c6d1559dd1f2d4189a5e851ef753a           0.1s 
 => => resolve docker.io/library/alpine:3.17@sha256:f271e74b17ced29b915d351685fd4644785c6d1559dd1f2d4189a5e851ef753a                       0.1s 
 => exporting to image                                                                                                                     5.1s 
 => => exporting layers                                                                                                                    0.0s 
 => => exporting manifest sha256:4463076cf4b016381c6722f6cce481e015487b35318ccc6dc933cf407c212b11                                          0.0s 
 => => exporting config sha256:6057d58c0c6df1fbc55d89e1429ede402558ad4f9a243b06d81e26a40d31eb0d                                            0.0s 
 => => exporting manifest sha256:05276d99512d2cdc401ac388891b0735bee28ff3fc8e08be207a0ef585842cef                                          0.0s 
 => => exporting config sha256:86506d4d3917a7bb85cd3d147e651150b83943ee89199777ba214dd359d30b2e                                            0.0s 
 => => exporting manifest list sha256:a26956bd9bd966b50312b4a7868d8461d596fe9380652272db612faef5ce9798                                     0.0s 
 => => pushing layers                                                                                                                      3.0s 
 => => pushing manifest for docker.io/aneasystone/demo:v2@sha256:a26956bd9bd966b50312b4a7868d8461d596fe9380652272db612faef5ce9798          2.0s 
 => [auth] aneasystone/demo:pull,push token for registry-1.docker.io                                                                       0.0s 
 => [auth] aneasystone/demo:pull,push library/alpine:pull token for registry-1.docker.io   
```

访问 [Docker Hub](https://hub.docker.com/repository/docker/aneasystone/demo/tags)，可以看到我们的镜像已经成功推送到仓库中了：

![](./images/demo-v2-image.png)

## 参考

1. [Faster Multi-platform builds: Dockerfile cross-compilation guide (Part 1)](https://medium.com/@tonistiigi/faster-multi-platform-builds-dockerfile-cross-compilation-guide-part-1-ec087c719eaf)
1. [Multi-arch build and images, the simple way](https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/)
1. [如何使用 docker buildx 构建跨平台 Go 镜像](https://waynerv.com/posts/building-multi-architecture-images-with-docker-buildx/)
1. [构建多种系统架构支持的 Docker 镜像](https://yeasy.gitbook.io/docker_practice/image/manifest)
1. [使用buildx来构建支持多平台的Docker镜像(Mac系统)](https://blog.cnscud.com/docker/2021/11/17/docker-buildx.html)
1. [使用 Docker Buildx 构建多种系统架构镜像](https://www.51cto.com/article/678858.html)
1. [使用 buildx 构建多平台 Docker 镜像](https://icloudnative.io/posts/multiarch-docker-with-buildx/)
1. [基于QEMU和binfmt-misc透明运行不同架构程序](https://blog.lyle.ac.cn/2020/04/14/transparently-running-binaries-from-any-architecture-in-linux-with-qemu-and-binfmt-misc/)
1. [多架构镜像三部曲（一）组合](https://blog.csdn.net/mycosmos/article/details/123587243)
1. [多架构镜像三部曲（二）构建](https://blog.csdn.net/mycosmos/article/details/125020271)

## 更多

### 使用 QEMU 运行不同架构的程序

在构建好多个架构的镜像之后，我们可以使用 `docker run` 测试一下：

```
$ docker run --rm -it aneasystone/demo:v1-amd64
Hello

$ docker run --rm -it aneasystone/demo:v1-arm64
WARNING: The requested image's platform (linux/arm64/v8) does not match the detected host platform (linux/amd64) and no specific platform was requested
Hello
```

这里可以发现一个非常奇怪的现象，我们的系统明明不是 arm64 的，为什么 arm64 的镜像也能正常运行呢？除了一行 WARNING 信息之外，看上去并没有异样，而且我们也可以使用 `sh` 进到容器内部正常操作：

```
> docker run --rm -it aneasystone/demo:v1-arm64 sh
WARNING: The requested image's platform (linux/arm64/v8) does not match the detected host platform (linux/amd64) and no specific platform was requested
/ # ls
bin    dev    etc    home   lib    media  mnt    opt    proc   root   run    sbin   srv    sys    tmp    usr    var
/ #
```

不过当我们执行 `ps` 命令时，发现了一些端倪：

```
/ # ps aux
PID   USER     TIME  COMMAND
    1 root      0:00 {sh} /usr/bin/qemu-aarch64 /bin/sh sh
    8 root      0:00 ps aux
```

可以看出我们所执行的 `sh` 命令实际上被 `/usr/bin/qemu-aarch64` 转换了，而 [QEMU](https://www.qemu.org/) 是一款强大的模拟器，可以在 x86 机器上模拟 arm 的指令。关于 QEMU 执行跨架构程序可以参考 [这篇文章](https://blog.lyle.ac.cn/2020/04/14/transparently-running-binaries-from-any-architecture-in-linux-with-qemu-and-binfmt-misc/)。

### 查看镜像的 manifest 信息

除了 `docker manifest` 命令，还有很多其他方法也可以查看镜像的 manifest 信息，比如：

* [crane manifest](https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_manifest.md)
* [manifest-tool](https://github.com/estesp/manifest-tool)

### `buildx` 支持的几种输出类型

在上文中，我们使用了 `--push` 参数将镜像推送到镜像仓库中：

```
$ docker buildx build --push --platform=linux/amd64,linux/arm64 -t aneasystone/demo:v2 .
```

这个命令实际上等同于：

```
$ docker buildx build --output=type=image,name=aneasystone/demo:v2,push=true --platform=linux/amd64,linux/arm64 .
```

也等同于：

```
$ docker buildx build --output=type=registry,name=aneasystone/demo:v2 --platform=linux/amd64,linux/arm64 .
```

我们通过 `--output` 参数指定镜像的输出类型，这又被称为 [导出器（ exporter ）](https://docs.docker.com/build/exporters/)，`buildx` 支持如下几种不同的导出器：

* `image` - 将构建结果导出到镜像
* `registry` - 将构建结果导出到镜像，并推送到镜像仓库
* `local` - 将构建的文件系统导出成本地目录
* `tar` - 将构建的文件系统打成 tar 包
* `oci` - 构建 [OCI 镜像格式](https://github.com/opencontainers/image-spec/blob/v1.0.1/image-layout.md) 的镜像
* `docker` - 构建 [Docker 镜像格式](https://github.com/docker/docker/blob/v20.10.2/image/spec/v1.2.md) 的镜像
* `cacheonly` - 将构建结果放在构建缓存中

其中 `image` 和 `registry` 这两个导出器上面已经用过，一般用来将镜像推送到远程镜像仓库。如果我们只想构建本地镜像，而不希望将其推送到远程镜像仓库，可以使用 `oci` 或 `docker` 导出器，比如下面的命令使用 `docker` 导出器将构建结果导出成本地镜像：

```
$ docker buildx build --output=type=docker,name=aneasystone/demo:v2-amd64 --platform=linux/amd64 .
```

也可以使用 `docker` 导出器将构建结果导出成 tar 文件：

```
$ docker buildx build --output=type=docker,dest=./demo-v2-docker.tar --platform=linux/amd64 .
```

这个 tar 文件可以通过 `docker load` 加载：

```
$ docker load -i ./demo-v2-docker.tar
```

因为我本地运行的是 Docker 服务，不支持 OCI 镜像格式，所以指定 `type=oci` 时会报错：

```
$ docker buildx build --output=type=oci,name=aneasystone/demo:v2-amd64 --platform=linux/amd64 .
ERROR: output file is required for oci exporter. refusing to write to console
```

不过我们可以将 OCI 镜像导出成 tar 包：

```
$ docker buildx build --output=type=oci,dest=./demo-v2-oci.tar --platform=linux/amd64 .
```

将这个 tar 包解压后，可以看到一个标准的镜像是什么格式：

```
$ mkdir demo-v2-docker && tar -C demo-v2-docker -xf demo-v2-docker.tar
$ tree demo-v2-docker
demo-v2-docker
├── blobs
│   └── sha256
│       ├── 4463076cf4b016381c6722f6cce481e015487b35318ccc6dc933cf407c212b11
│       ├── 6057d58c0c6df1fbc55d89e1429ede402558ad4f9a243b06d81e26a40d31eb0d
│       └── 8921db27df2831fa6eaa85321205a2470c669b855f3ec95d5a3c2b46de0442c9
├── index.json
├── manifest.json
└── oci-layout

2 directories, 6 files
```

> 有一点奇怪的是，OCI 镜像格式的 tar 包和 docker 镜像格式的 tar 包是完全一样的，不知道怎么回事？

如果我们不关心构建结果，而只是想看下构建镜像的文件系统，比如看看它的目录结构是什么样的，或是看看有没有我们需要的文件，可以使用 `local` 或 `tar` 导出器。`local` 导出器将文件系统导到本地的目录：

```
$ docker buildx build --output=type=local,dest=./demo-v2 --platform=linux/amd64 .
```

`tar` 导出器将文件系统导到一个 tar 文件中：

```
$ docker buildx build --output=type=tar,dest=./demo-v2.tar --platform=linux/amd64 .
```

值得注意的是，这个 tar 文件并不是标准的镜像格式，所以我们不能使用 `docker load` 加载，但是我们可以使用 `docker import` 加载，加载的镜像中只有文件系统，在运行这个镜像时，Dockerfile 中的 `CMD` 或 `ENTRYPOINT` 等命令是不会生效的：

```
$ mkdir demo-v2 && tar -C demo-v2 -xf demo-v2.tar
$ ls demo-v2
bin  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

### 不安全的镜像仓库

在上文中，我们使用了两种方法构建了多架构镜像，并将镜像推送到官方的 Docker Hub 仓库，如果需要推送到自己搭建的镜像仓库（ 关于如何搭建自己的镜像仓库，可以参考 [week023-build-your-own-image-registry](../week023-build-your-own-image-registry/README.md) ），由于这个仓库可能是不安全的，可能会遇到一些问题。

第一种方式是直接使用 `docker push` 推送，推送前我们需要修改 Docker 的配置文件 `/etc/docker/daemon.json`，将仓库地址添加到 `insecure-registries` 配置项中：

```
{
  "insecure-registries" : ["192.168.1.39:5000"]
}
```

然后重启 Docker 后即可。

第二种方式是使用 `docker buildx` 的 `image` 或 `registry` 导出器推送，这个推送工作实际上是由 buildkitd 完成的，所以我们需要让 buildkitd 忽略这个不安全的镜像仓库。我们首先创建一个配置文件 `buildkitd.toml`：

```toml
[registry."192.168.1.39:5000"]
  http = true
  insecure = true
```

关于 buildkitd 的详细配置可以 [参考这里](https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md)。然后使用 `docker buildx create` 重新创建一个构建器：

```
$ docker buildx create --config=buildkitd.toml --use
```

这样就可以让 `docker buildx` 将镜像推送到不安全的镜像仓库了。

# WEEK003 Docker 快速入门

在 WEEK002 中，我们通过多种方法在 VirtualBox 上安装了 Docker 服务，这一节我们将根据官网文档，学习 Docker 的一些入门知识。这一节的内容主要包括：

* 构建和运行镜像
* 通过 Docker Hub 分享镜像
* 使用多个容器部署 Docker 应用
* 使用 Docker Compose 运行应用
* 构建镜像的最佳实践，对镜像进行安全扫描

## Part 1: Getting started

我们在命令行上输入如下的命令开始我们的 Docker 之旅：

```
[root@localhost ~]# docker run -d -p 80:80 docker/getting-started
```

其中，`-d` 表示让容器运行在 `detached mode`，也就是后台运行，`-p 80:80` 表示将容器内的 80 端口映射到主机的 80 端口，这样我们就可以通过主机的 80 端口来访问容器里的服务，在浏览器里输入 `http://127.0.0.1:80`，会看到如下页面：

![](./images/getting-started.png)

这样我们就在我们的机器上成功运行了一个简单的容器了。

### 什么是容器？

简单来说，容器就是一个运行在沙箱（`sandboxed`）中的进程，通过 Linux 内核提供的 `namespace` 和 `cgroup` 等特性，它和主机上的其他进程之间是隔离的。它的特点如下：

* 容器是镜像的一个运行实例，你可以通过 Docker API 或 CLI 创建、运行、停止、移动或删除容器
* 容器可以在本地机器、虚拟机或云端运行
* 可移植到任意的操作系统
* 容器之间互相隔离

### 什么是镜像？

当我们运行容器时，它实际上使用了一个独立的文件系统，这个独立的文件系统就是镜像所提供的，并且这个文件系统里包含了容器运行所需要的所有东西，比如：配置，脚本，二进制程序等等，另外，镜像里还包含了一些其他的配置，比如：环境变量，启动后默认执行的命令，和其他元数据。

在 Linux 系统中有一个命令叫 [`chroot`](https://man7.org/linux/man-pages/man1/chroot.1.html)，它可以用来改变程序运行的根目录，系统默认都是以 `/` 作为根目录来运行程序，当使用了 `chroot` 之后，程序的根目录就变成了你指定的位置。你可以把容器简单理解成增强版的 `chroot`，根目录就是镜像所提供的文件系统，不过 `chroot` 只提供了文件系统的隔离，容器在 `chroot` 的基础上还增加了其他的隔离，比如进程隔离，用户隔离，网络隔离，资源限制等。

## Part 2: Sample application

这一部分我们将通过一个简单的待办清单程序来学习如何构建和运行镜像。首先，我们通过 `git clone` 下载程序的源码：

```
[root@localhost ~]# git clone https://github.com/docker/getting-started.git
```

这个代办清单程序的源码位于 `app` 目录下，让我们进去看一看：

```
[root@localhost ~]# cd getting-started/app/
[root@localhost app]# ls
package.json  spec  src  yarn.lock
```

这是一个 Node.js 程序，为了让这个程序能运行起来，我们必须得有 Node.js 的运行环境。

## Part 3: Update the application
## Part 4: Share the application
## Part 5: Persist the DB
## Part 6: Use bind mounts
## Part 7: Multi-container apps
## Part 8: Use Docker Compose
## Part 9: Image-building best practices
## Part 10: What next?

## 参考

1. [Docker 官方文档](https://docs.docker.com/)
1. [How to Get Started with Docker • DockerCon 2020](https://youtu.be/iqqDU2crIEQ)
1. [Containers From Scratch • Liz Rice • GOTO 2018](https://youtu.be/8fi7uSYlOdc)
1. [Demystifying Containers](https://github.com/saschagrunert/demystifying-containers)
1. [linux chroot 命令](https://www.cnblogs.com/sparkdev/p/8556075.html)

## 更多

### 1. 在虚拟机中使用代理

在虚拟机中通过 `git clone` 下载源码时，由于一些客观原因，经常会出现各种网络错误或超时，比如这样：

```
[root@localhost ~]# git clone https://github.com/docker/getting-started.git
正克隆到 'getting-started'...
fatal: unable to access 'https://github.com/docker/getting-started.git/': TCP connection reset by peer
```

又比如这样：

```
[root@localhost ~]# git clone https://github.com/docker/getting-started.git
正克隆到 'getting-started'...
error: RPC failed; result=35, HTTP code = 0
fatal: The remote end hung up unexpectedly
```

这让人无法忍受，这时我们可以通过下面的命令设置 Linux 的代理来解决（当然，前提是你得先准备好梯子）：

```
[root@localhost ~]# export http_proxy=192.168.1.43:10809 https_proxy=192.168.1.43:10809
```

### 2. 体验使用 `chroot` 命令

### 3. 关于 Docker 的更多文档

Docker 官方文档的内容非常丰富，主要分成如下几个部分：

#### 1. Get Started

#### 2. Download and install

Download and install Docker on your machine in a few easy steps.

##### Docker Desktop for Mac
##### Docker Desktop for Windows
##### Docker for Linux

#### 3. Guides

Learn how to set up your Docker environment and start containerizing your applications.

#### 4. Language-specific guides

Learn how to containerize language-specific applications using Docker.

#### 5. Manuals

Browse through the manuals and learn how to use Docker products.

#### 6. Reference

Browse through the CLI and API reference documentation.

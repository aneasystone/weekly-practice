# WEEK003 Docker 快速入门

在 WEEK002 中，我们通过多种方法在 VirtualBox 上安装了 Docker 服务，这一节我们将根据官网文档，学习 Docker 的一些入门知识。这一节的内容主要包括：

* 构建镜像和运行容器
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

* 容器是镜像的一个运行实例，你可以通过 Docker API 或 CLI 创建、运行、停止、移动、删除容器
* 容器可以在本地机器、虚拟机或云端运行
* 可移植到任意的操作系统
* 容器之间互相隔离

### 什么是镜像？

当我们运行容器时，它实际上使用了一个独立的文件系统，这个独立的文件系统就是镜像所提供的。

## Part 2: Sample application
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

## 更多

Docker 官方文档的内容非常丰富，主要分成如下几个部分：

### 1. Get Started

### 2. Download and install

Download and install Docker on your machine in a few easy steps.

#### Docker Desktop for Mac
#### Docker Desktop for Windows
#### Docker for Linux

### 3. Guides

Learn how to set up your Docker environment and start containerizing your applications.

### 4. Language-specific guides

Learn how to containerize language-specific applications using Docker.

### 5. Manuals

Browse through the manuals and learn how to use Docker products.

### 6. Reference

Browse through the CLI and API reference documentation.

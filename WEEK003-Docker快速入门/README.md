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

其中，`-d` 表示让容器运行在 `detached mode`，也就是后台运行，`-p 80:80` 表示将容器内的 80 端口映射到主机的 80 端口，这样我们就可以通过主机的 80 端口来访问容器里的服务，在浏览器里输入 `http://localhost:80`，会看到如下页面：

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

首先，我们在这个目录下新建一个 `Dockerfile` 文件：

```
[root@localhost app]# vi Dockerfile
```

在这个文件中输入如下内容：

```
FROM node:12-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]
EXPOSE 3000
```

`Dockerfile` 是我们构建镜像时所需的指令文件，`FROM node:12-alpine` 表示我们使用 `node:12-alpine` 来作为我们的基础镜像，这是一个内置了 Node.js 运行环境的镜像，`WORKDIR /app` 表示将镜像的 `/app` 目录作为工作目录，这样执行 `COPY . .` 的时候就可以把当前目录下的文件复制到镜像里的 `/app` 目录下了。然后通过 `RUN yarn install --production` 安装程序所需要的一些依赖，这些依赖定义在 `package.json` 文件里。最后的 `CMD ["node", "src/index.js"]` 和 `EXPOSE 3000` 指定了容器运行时的启动命令和容器对外暴露的端口。

写好这个 `Dockerfile` 文件后，就可以通过 `docker build -t todo-list .` 命令来构建镜像：

```
[root@localhost app]# docker build -t todo-list .
Sending build context to Docker daemon  4.641MB
Step 1/6 : FROM node:12-alpine
12-alpine: Pulling from library/node
59bf1c3509f3: Already exists 
8769eb813ad5: Pull complete 
7025e9ac362e: Pull complete 
1efe07d207fa: Pull complete 
Digest: sha256:dfa564312367b1a8fca8db7ae4bae102b28e68b39ebcb7b17022c938f105846b
Status: Downloaded newer image for node:12-alpine
 ---> 1b156b4c3ee8
Step 2/6 : WORKDIR /app
 ---> Running in fbb23d022619
Removing intermediate container fbb23d022619
 ---> a19fa5fc5c18
Step 3/6 : COPY . .
 ---> acdf512be224
Step 4/6 : RUN yarn install --production
 ---> Running in 9af3492b1571
yarn install v1.22.17
[1/4] Resolving packages...
warning Resolution field "ansi-regex@5.0.1" is incompatible with requested version "ansi-regex@^2.0.0"
warning Resolution field "ansi-regex@5.0.1" is incompatible with requested version "ansi-regex@^3.0.0"
warning sqlite3 > node-gyp > request@2.88.2: request has been deprecated, see https://github.com/request/request/issues/3142
warning sqlite3 > node-gyp > tar@2.2.2: This version of tar is no longer supported, and will not receive security updates. Please upgrade asap.
warning sqlite3 > node-gyp > request > har-validator@5.1.5: this library is no longer supported
warning sqlite3 > node-gyp > request > uuid@3.4.0: Please upgrade  to version 7 or higher.  Older versions may use Math.random() in certain circumstances, which is known to be problematic.  See https://v8.dev/blog/math-random for details.
[2/4] Fetching packages...
[3/4] Linking dependencies...
[4/4] Building fresh packages...
success Saved lockfile.
Done in 35.53s.
Removing intermediate container 9af3492b1571
 ---> c50542645f82
Step 5/6 : CMD ["node", "src/index.js"]
 ---> Running in 77212d79a3a7
Removing intermediate container 77212d79a3a7
 ---> 5f5a66a501ae
Step 6/6 : EXPOSE 3000
 ---> Running in c4d8ac990217
Removing intermediate container c4d8ac990217
 ---> eeb273056a6a
Successfully built eeb273056a6a
Successfully tagged todo-list:latest
```

其中 `-t todo-list` 指定了构建后的镜像名称，注意命令最后的 `.` 不能忽略，这表示让 `docker build` 将当前目录作为构建上下文，并从这里寻找 `Dockerfile` 文件。从上面的输出结果可以看出，`docker build` 命令按照 `Dockerfile` 文件中的指令一行一行的执行，最终生成了一个名为 `todo-list:latest` 的镜像。

现在我们构建好了镜像，让我们运行它：

```
[root@localhost app]# docker run -dp 3000:3000 todo-list
```

其中 `-dp` 是 `-d -p` 的缩写，当 `docker` 命令行中的参数是一个字母的时候，就可以通过这种方式缩写，比如 `docker run -i -t` 可以缩写成 `docker run -it`。

我们打开浏览器，访问 `http://localhost:3000`，你就能看到我们的代办清单小程序了：

![](./images/todo-list.png)

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

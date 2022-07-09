# WEEK002 - 在 VirtualBox 上安装 Docker 服务

在 [week001-centos-on-virtualbox](../week001-centos-on-virtualbox/README.md) 中，我们在 VirtualBox 上安装了 CentOS 实验环境，这一节我们会继续在这个环境上安装 Docker 服务。

## 1. 使用 XShell 连接虚拟机

在虚拟机里进行几次操作之后，我们发现，由于这个系统是纯命令行界面，无法使用 VirtualBox 的增强功能，比如共享文件夹、共享剪切板等，每次想从虚拟机中复制一段文本出来都非常麻烦。所以，如果能从虚拟机外面用 XShell 登录进行操作，那就完美了。

我们首先登录虚拟机，查看 IP：

```
[root@localhost ~]# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 08:00:27:c1:96:99 brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.6/24 brd 10.0.2.255 scope global noprefixroute dynamic enp0s3
       valid_lft 453sec preferred_lft 453sec
    inet6 fe80::e0ae:69af:54a5:f8d0/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
```

然后使用 XShell 连接 10.0.2.6 的 22 端口：

![](./images/xshell-docker-1.png)

可是却发现连接不了：

```
Connecting to 10.0.2.6:22...
Could not connect to '10.0.2.6' (port 22): Connection failed.
```

通过复习 [week001-centos-on-virtualbox](../week001-centos-on-virtualbox/README.md) 的内容，我们知道目前我们使用的 VirtualBox 的网络模式是 `NAT 网络`，在这种网络模式下，宿主机是无法直接访问虚拟机的，而要通过 `端口转发（Port Forwarding）`。

我们打开 VirtualBox “管理” -> “全局设定” 菜单，找到 “网络” 选项卡，在这里能看到我们使用的 NAT 网络：

![](./images/virtualbox-network-setting.png)

双击 `NatNetwork` 打开 NAT 网络的配置：

![](./images/virtualbox-network-setting-2.png)

会发现下面有一个 `端口转发` 的按钮，在这里我们可以定义从宿主机到虚拟机的端口映射：

![](./images/virtualbox-nat-port-forwarding.png)

我们新增这样一条规则：

* 协议： TCP
* 主机：192.168.1.43:2222
* 子系统：10.0.2.6:22

这表示 VirtualBox 会监听宿主机 192.168.1.43 的 2222 端口，并将 2222 端口的请求转发到 10.0.2.6 这台虚拟机的 22 端口。

我们使用 XShell 连接 192.168.1.43:2222，这一次成功进入了：

```
Connecting to 192.168.1.43:2222...
Connection established.
To escape to local shell, press 'Ctrl+Alt+]'.

WARNING! The remote SSH server rejected X11 forwarding request.
Last login: Mon Feb 21 06:49:44 2022
[root@localhost ~]#
```

## 2. 通过 yum 安装 Docker

系统默认的仓库里是没有 Docker 服务的：

```
[root@localhost ~]# ls /etc/yum.repos.d/
CentOS-Base.repo  CentOS-Debuginfo.repo  CentOS-Media.repo    CentOS-Vault.repo
CentOS-CR.repo    CentOS-fasttrack.repo  CentOS-Sources.repo  CentOS-x86_64-kernel.repo
```

我们需要先在系统中添加 [Docker 仓库](https://download.docker.com/linux/centos/docker-ce.repo)，可以直接将仓库文件下载下来放到 `/etc/yum.repos.d/` 目录，也可以通过 `yum-config-manager` 命令来添加。

先安装 `yum-utils`：

```
[root@localhost ~]# yum install -y yum-utils
```

再通过 `yum-config-manager` 添加 Docker 仓库：

```
[root@localhost ~]# yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
已加载插件：fastestmirror
adding repo from: https://download.docker.com/linux/centos/docker-ce.repo
grabbing file https://download.docker.com/linux/centos/docker-ce.repo to /etc/yum.repos.d/docker-ce.repo
repo saved to /etc/yum.repos.d/docker-ce.repo
```

接下来我们继续安装 Docker 服务：

```
[root@localhost ~]# yum install docker-ce docker-ce-cli containerd.io
```

安装过程根据提示输入 `y` 确认即可，另外，还会提示你校验 GPG 密钥，正常情况下这个密钥的指纹应该是 `060a 61c5 1b55 8a7f 742b 77aa c52f eb6b 621e 9f35`：

```
从 https://download.docker.com/linux/centos/gpg 检索密钥
导入 GPG key 0x621E9F35:
 用户ID     : "Docker Release (CE rpm) <docker@docker.com>"
 指纹       : 060a 61c5 1b55 8a7f 742b 77aa c52f eb6b 621e 9f35
 来自       : https://download.docker.com/linux/centos/gpg
是否继续？[y/N]：y
```

如果安装顺利，就可以通过 `systemctl start docker` 启动 Docker 服务了，然后运行 `docker run hello-world` 验证 Docker 服务是否正常：

```
[root@localhost ~]# systemctl start docker
[root@localhost ~]# docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
2db29710123e: Pull complete 
Digest: sha256:97a379f4f88575512824f3b352bc03cd75e239179eea0fecc38e597b2209f49a
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

看到这个提示信息，说明 Docker 服务已经在虚拟机中正常运行了。

## 3. 通过 `docker-install` 脚本安装 Docker

官方提供了一个便捷的脚本来一键安装 Docker，可以通过如下命令下载该脚本：

```
[root@localhost ~]# curl -fsSL https://get.docker.com -o get-docker.sh
```

其中，`-f/--fail` 表示连接失败时不显示 HTTP 错误，`-s/--silent` 表示静默模式，不输出任何内容，`-S/--show-error` 表示显示错误，`-L/--location` 表示跟随重定向，`-o/--output` 表示将输出写入到某个文件中。

下载完成后，执行该脚本会自动安装 Docker：

```
[root@localhost ~]# sh ./get-docker.sh
```

如果想知道这个脚本具体做了什么，可以在执行命令之前加上 `DRY_RUN=1` 选项：

```
[root@localhost ~]# DRY_RUN=1 sh ./get-docker.sh
# Executing docker install script, commit: 93d2499759296ac1f9c510605fef85052a2c32be
yum install -y -q yum-utils
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum makecache
yum install -y -q docker-ce
yum install -y -q docker-ce-rootless-extras
```

可以看出和上一节手工安装的步骤基本类似，安装完成后，启动 Docker 服务并运行 `hello-world` 验证：

```
[root@localhost ~]# systemctl start docker
[root@localhost ~]# docker run hello-world
```

## 4. 离线安装 Docker

上面两种安装方式都需要连接外网，当我们的机器位于离线环境时（`air-gapped systems`），我们需要提前将 Docker 的安装包下载准备好。

我们从 https://download.docker.com/linux/ 这里找到对应的 Linux 发行版本和系统架构，比如我这里的系统是 CentOS 7.9，系统架构是 x84_64，所以就进入 `/linux/centos/7/x86_64/stable/Packages/` 这个目录。但是这个目录里有很多的文件，我们该下载哪个文件呢？

为了确定要下载的文件和版本，我们进入刚刚安装的那个虚拟机中，通过 `yum list installed | grep docker` 看看自动安装时都安装了哪些包：

```
[root@localhost ~]# yum list installed | grep docker
containerd.io.x86_64                 1.4.12-3.1.el7                 @docker-ce-stable
docker-ce.x86_64                     3:20.10.12-3.el7               @docker-ce-stable
docker-ce-cli.x86_64                 1:20.10.12-3.el7               @docker-ce-stable
docker-ce-rootless-extras.x86_64     20.10.12-3.el7                 @docker-ce-stable
docker-scan-plugin.x86_64            0.12.0-3.el7                   @docker-ce-stable
```

我们将这些包都下载下来复制到一台新的虚拟机中，将网络服务关闭：

```
[root@localhost ~]# service network stop
```

然后执行 `yum install` 命令安装这些 RPM 包：

```
[root@localhost ~]# yum install *.rpm
```

我们会发现 yum 在安装的时候会自动解析依赖，还是会从外网下载，会出现一堆的报错：

![](./images/rpm-install-docker.png)

我们可以对照着这个列表再去一个个的下载对应的包，全部依赖安装完毕后，再安装 Docker 即可。

当然这样一个个去试并不是什么好方法，我们可以使用 `rpm` 的 `-q` 功能，查询 RPM 包的信息，`-R` 表示查询 RPM 包的依赖：

```
[root@localhost docker]# rpm -q -R -p docker-ce-20.10.12-3.el7.x86_64.rpm 
警告：docker-ce-20.10.12-3.el7.x86_64.rpm: 头V4 RSA/SHA512 Signature, 密钥 ID 621e9f35: NOKEY
/bin/sh
/bin/sh
/bin/sh
/usr/sbin/groupadd
container-selinux >= 2:2.74
containerd.io >= 1.4.1
docker-ce-cli
docker-ce-rootless-extras
iptables
libc.so.6()(64bit)
libc.so.6(GLIBC_2.2.5)(64bit)
libc.so.6(GLIBC_2.3)(64bit)
libcgroup
libdevmapper.so.1.02()(64bit)
libdevmapper.so.1.02(Base)(64bit)
libdevmapper.so.1.02(DM_1_02_97)(64bit)
libdl.so.2()(64bit)
libdl.so.2(GLIBC_2.2.5)(64bit)
libpthread.so.0()(64bit)
libpthread.so.0(GLIBC_2.2.5)(64bit)
libpthread.so.0(GLIBC_2.3.2)(64bit)
libseccomp >= 2.3
libsystemd.so.0()(64bit)
libsystemd.so.0(LIBSYSTEMD_209)(64bit)
rpmlib(CompressedFileNames) <= 3.0.4-1
rpmlib(FileDigests) <= 4.6.0-1
rpmlib(PayloadFilesHavePrefix) <= 4.0-1
rtld(GNU_HASH)
systemd
tar
xz
rpmlib(PayloadIsXz) <= 5.2-1
```

但是这样一个个去下载依赖的包也是很繁琐的，有没有什么办法能将依赖的包一次性都下载下来呢？当然有！还记得上面的 `yum install` 安装命令吧，其实 `yum` 在安装之前，先是做了两件事情，第一步解析包的依赖，然后将所有依赖的包下载下来，最后才是安装。而 `yum --downloadonly` 可以让我们只将依赖包下载下来，默认情况下 `yum` 将依赖的包下载到 `/var/cache/yum/x86_64/[centos/fedora-version]/[repository]/packages` 目录，其中 `[repository]` 表示来源仓库的名称，比如 base、docker-ce-stable、extras 等，不过这样还是不够友好，我们希望下载下来的文件放在一起，这时可以使用 `--downloaddir` 参数来指定下载目录：

```
[root@localhost ~]# yum --downloadonly --downloaddir=. install docker-ce docker-ce-cli containerd.io
已加载插件：fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirrors.bupt.edu.cn
 * extras: mirrors.dgut.edu.cn
 * updates: mirrors.bupt.edu.cn
正在解决依赖关系
--> 正在检查事务
---> 软件包 containerd.io.x86_64.0.1.4.12-3.1.el7 将被 安装
--> 正在处理依赖关系 container-selinux >= 2:2.74，它被软件包 containerd.io-1.4.12-3.1.el7.x86_64 需要
---> 软件包 docker-ce.x86_64.3.20.10.12-3.el7 将被 安装
--> 正在处理依赖关系 docker-ce-rootless-extras，它被软件包 3:docker-ce-20.10.12-3.el7.x86_64 需要
--> 正在处理依赖关系 libcgroup，它被软件包 3:docker-ce-20.10.12-3.el7.x86_64 需要
---> 软件包 docker-ce-cli.x86_64.1.20.10.12-3.el7 将被 安装
--> 正在处理依赖关系 docker-scan-plugin(x86-64)，它被软件包 1:docker-ce-cli-20.10.12-3.el7.x86_64 需要
--> 正在检查事务
---> 软件包 container-selinux.noarch.2.2.119.2-1.911c772.el7_8 将被 安装
--> 正在处理依赖关系 policycoreutils-python，它被软件包 2:container-selinux-2.119.2-1.911c772.el7_8.noarch 需要
---> 软件包 docker-ce-rootless-extras.x86_64.0.20.10.12-3.el7 将被 安装
--> 正在处理依赖关系 fuse-overlayfs >= 0.7，它被软件包 docker-ce-rootless-extras-20.10.12-3.el7.x86_64 需要
--> 正在处理依赖关系 slirp4netns >= 0.4，它被软件包 docker-ce-rootless-extras-20.10.12-3.el7.x86_64 需要
---> 软件包 docker-scan-plugin.x86_64.0.0.12.0-3.el7 将被 安装
---> 软件包 libcgroup.x86_64.0.0.41-21.el7 将被 安装
--> 正在检查事务
---> 软件包 fuse-overlayfs.x86_64.0.0.7.2-6.el7_8 将被 安装
--> 正在处理依赖关系 libfuse3.so.3(FUSE_3.2)(64bit)，它被软件包 fuse-overlayfs-0.7.2-6.el7_8.x86_64 需要
--> 正在处理依赖关系 libfuse3.so.3(FUSE_3.0)(64bit)，它被软件包 fuse-overlayfs-0.7.2-6.el7_8.x86_64 需要
--> 正在处理依赖关系 libfuse3.so.3()(64bit)，它被软件包 fuse-overlayfs-0.7.2-6.el7_8.x86_64 需要
---> 软件包 policycoreutils-python.x86_64.0.2.5-34.el7 将被 安装
--> 正在处理依赖关系 setools-libs >= 3.3.8-4，它被软件包 policycoreutils-python-2.5-34.el7.x86_64 需要
--> 正在处理依赖关系 libsemanage-python >= 2.5-14，它被软件包 policycoreutils-python-2.5-34.el7.x86_64 需要
--> 正在处理依赖关系 audit-libs-python >= 2.1.3-4，它被软件包 policycoreutils-python-2.5-34.el7.x86_64 需要
--> 正在处理依赖关系 python-IPy，它被软件包 policycoreutils-python-2.5-34.el7.x86_64 需要
--> 正在处理依赖关系 libqpol.so.1(VERS_1.4)(64bit)，它被软件包 policycoreutils-python-2.5-34.el7.x86_64 需要
--> 正在处理依赖关系 libqpol.so.1(VERS_1.2)(64bit)，它被软件包 policycoreutils-python-2.5-34.el7.x86_64 需要
--> 正在处理依赖关系 libapol.so.4(VERS_4.0)(64bit)，它被软件包 policycoreutils-python-2.5-34.el7.x86_64 需要
--> 正在处理依赖关系 checkpolicy，它被软件包 policycoreutils-python-2.5-34.el7.x86_64 需要
--> 正在处理依赖关系 libqpol.so.1()(64bit)，它被软件包 policycoreutils-python-2.5-34.el7.x86_64 需要
--> 正在处理依赖关系 libapol.so.4()(64bit)，它被软件包 policycoreutils-python-2.5-34.el7.x86_64 需要
---> 软件包 slirp4netns.x86_64.0.0.4.3-4.el7_8 将被 安装
--> 正在检查事务
---> 软件包 audit-libs-python.x86_64.0.2.8.5-4.el7 将被 安装
---> 软件包 checkpolicy.x86_64.0.2.5-8.el7 将被 安装
---> 软件包 fuse3-libs.x86_64.0.3.6.1-4.el7 将被 安装
---> 软件包 libsemanage-python.x86_64.0.2.5-14.el7 将被 安装
---> 软件包 python-IPy.noarch.0.0.75-6.el7 将被 安装
---> 软件包 setools-libs.x86_64.0.3.3.8-4.el7 将被 安装
--> 解决依赖关系完成

依赖关系解决

========================================================================================================================================================
 Package                                    架构                    版本                                        源                                 大小
========================================================================================================================================================
正在安装:
 containerd.io                              x86_64                  1.4.12-3.1.el7                              docker-ce-stable                   28 M
 docker-ce                                  x86_64                  3:20.10.12-3.el7                            docker-ce-stable                   23 M
 docker-ce-cli                              x86_64                  1:20.10.12-3.el7                            docker-ce-stable                   30 M
为依赖而安装:
 audit-libs-python                          x86_64                  2.8.5-4.el7                                 base                               76 k
 checkpolicy                                x86_64                  2.5-8.el7                                   base                              295 k
 container-selinux                          noarch                  2:2.119.2-1.911c772.el7_8                   extras                             40 k
 docker-ce-rootless-extras                  x86_64                  20.10.12-3.el7                              docker-ce-stable                  8.0 M
 docker-scan-plugin                         x86_64                  0.12.0-3.el7                                docker-ce-stable                  3.7 M
 fuse-overlayfs                             x86_64                  0.7.2-6.el7_8                               extras                             54 k
 fuse3-libs                                 x86_64                  3.6.1-4.el7                                 extras                             82 k
 libcgroup                                  x86_64                  0.41-21.el7                                 base                               66 k
 libsemanage-python                         x86_64                  2.5-14.el7                                  base                              113 k
 policycoreutils-python                     x86_64                  2.5-34.el7                                  base                              457 k
 python-IPy                                 noarch                  0.75-6.el7                                  base                               32 k
 setools-libs                               x86_64                  3.3.8-4.el7                                 base                              620 k
 slirp4netns                                x86_64                  0.4.3-4.el7_8                               extras                             81 k

事务概要
========================================================================================================================================================
安装  3 软件包 (+13 依赖软件包)

总下载量：95 M
安装大小：387 M
Background downloading packages, then exiting:
exiting because "Download Only" specified
```

可以看到 3 个软件包和 13 个依赖包都下载好了，我们将这 16 个包全部复制到离线机器上，运行 `yum install *.rpm` 即可。

除了 `yum --downloadonly` 实现离线安装之外，还有很多其他的方式，比如：搭建自己的本地 `yum` 源就是一种更通用的解决方案，可以根据参考链接尝试一下。

## 参考

1. [Install Docker Engine on CentOS](https://docs.docker.com/engine/install/centos/)
1. [curl - How To Use](https://curl.se/docs/manpage.html)
1. [Centos7通过reposync搭建本地Yum源](https://www.jianshu.com/p/6c3090968d71)

# WEEK062 - 通过 SSH 隧道从外网访问内网 Mac Mini 的共享屏幕

最近遇到了一个很常见的远程办公场景：我有一台 Mac Mini 放在公司内网，开启了 macOS 自带的"共享屏幕"功能（基于 VNC 协议，监听 5900 端口），平时在公司可以很方便地通过屏幕共享来远程操控它。但是回到家里，由于 Mac Mini 在内网，没有公网 IP，我就无法直接连接了。

好在我可以通过 SSH 连接到内网的一台服务器（这台服务器有公网 IP 或者通过 VPN 可达），再从这台服务器 SSH 到 Mac Mini。那么问题来了：能不能利用这条 SSH 链路，把 Mac Mini 的 VNC 端口"转发"出来，让我在家里也能用 macOS 的屏幕共享功能连接 Mac Mini 呢？

答案是可以的，这就是 **SSH 本地端口转发（Local Port Forwarding）** 的经典应用场景。

## 网络拓扑

先梳理一下整个网络链路：

```
家里的 Mac ──(互联网)──▶ 内网服务器（有公网 IP）──(内网)──▶ Mac Mini（VNC :5900）
```

家里的 Mac 可以 SSH 到内网服务器，内网服务器可以 SSH 到 Mac Mini，但家里的 Mac 无法直接访问 Mac Mini 的任何端口。我们的目标是在家里的 Mac 上打开屏幕共享，连接到 Mac Mini。

## SSH 本地端口转发

SSH 的 `-L` 参数可以将本地端口的流量通过 SSH 隧道转发到远端网络中的某个地址和端口。语法如下：

```
ssh -L 本地端口:目标地址:目标端口 SSH服务器
```

它的工作原理是：在本地监听指定端口，当有连接进来时，将流量通过 SSH 隧道发送到 SSH 服务器，再由 SSH 服务器去连接目标地址的目标端口，相当于 SSH 服务器充当了一个"跳板"。

对于我们的场景，命令如下：

```
$ ssh -L 15900:Mac-Mini内网IP:5900 用户名@内网服务器地址
```

> 这里用 15900 而不是 5900 作为本地端口，是因为家里的 Mac 自身可能也在监听 5900 端口（如果你开启了屏幕共享的话），使用一个不同的端口可以避免冲突。

执行成功后，在家里的 Mac 上打开 Finder，按 `Cmd + K`（或者菜单栏 前往 → 连接服务器），输入：

```
vnc://localhost:15900
```

如果一切顺利，你就可以看到 Mac Mini 的桌面了。

## 遇到 `administratively prohibited` 错误

然而，当我按照上面的步骤操作时，SSH 隧道看起来建立成功了，但在用屏幕共享连接时，终端里出现了这样的错误：

```
channel 3: open failed: administratively prohibited: open failed
```

这个错误的意思是 SSH 服务器**拒绝了 TCP 端口转发请求**。这是因为内网服务器的 SSH 配置中禁用了 `AllowTcpForwarding`。可以登录到内网服务器上检查一下：

```
$ grep -i allowtcpforwarding /etc/ssh/sshd_config
AllowTcpForwarding no
```

果然，`AllowTcpForwarding` 被设置为了 `no`。

如果你有服务器的 root 权限，可以将其改为 `yes`，然后重启 sshd 服务：

```
$ sudo vi /etc/ssh/sshd_config
# 将 AllowTcpForwarding no 改为 AllowTcpForwarding yes

$ sudo systemctl restart sshd
```

但如果你没有 root 权限，或者不想修改服务器配置，还有另一种方式可以绕过这个限制。

## 使用 ProxyJump 绕过限制

SSH 的 `-J` 参数（ProxyJump）提供了一种不同的转发机制。和 `-L` 不同，`-J` 走的是 **SSH 自身的 stdio 转发**，它不依赖 `AllowTcpForwarding` 配置，因此通常不会被拦截。

命令如下：

```
$ ssh -L 15900:localhost:5900 -J 用户名@内网服务器地址 用户名@Mac-Mini内网IP
```

这条命令做了两件事：

1. 通过 `-J` 参数，以内网服务器为跳板，SSH 连接到 Mac Mini；
2. 通过 `-L` 参数，将本地的 15900 端口转发到 Mac Mini 的 localhost:5900。

注意这里转发目标写的是 `localhost:5900` 而不是 `Mac-Mini内网IP:5900`，因为此时 SSH 已经连接到了 Mac Mini 上，端口转发是由 Mac Mini 自己来执行的，所以用 `localhost` 就可以了。

整个流量链路变成了：

```
家里 Mac(:15900) ──SSH──▶ 内网服务器(跳板) ──SSH──▶ Mac Mini ──本地访问──▶ localhost:5900
```

执行命令后，再次在屏幕共享中连接 `vnc://localhost:15900`，这次顺利连接成功了。

## 让隧道在后台运行

每次都要开一个终端窗口来维持 SSH 连接并不方便，可以加上 `-fN` 参数让隧道在后台运行：

```
$ ssh -fN -L 15900:localhost:5900 -J 用户名@内网服务器地址 用户名@Mac-Mini内网IP
```

- `-f`：SSH 在认证成功后进入后台运行
- `-N`：不执行远程命令，只做端口转发

这样终端就不会被占用了。如果想关闭隧道，可以用 `ps` 找到对应的 SSH 进程然后 `kill` 掉：

```
$ ps aux | grep ssh
$ kill <PID>
```

## 配置 SSH Config 简化命令

如果经常使用，每次都敲这么长一串命令还是比较麻烦的，可以在 `~/.ssh/config` 中配置好：

```
Host tunnel-mini
    HostName Mac-Mini内网IP
    User Mac-Mini用户名
    ProxyJump 用户名@内网服务器地址
    LocalForward 15900 localhost:5900
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

- `ProxyJump` 对应 `-J` 参数
- `LocalForward` 对应 `-L` 参数
- `ServerAliveInterval` 和 `ServerAliveCountMax` 用于保活，防止连接因为空闲而被断开

之后只需要：

```
$ ssh -fN tunnel-mini
```

然后 `vnc://localhost:15900` 即可连接 Mac Mini 的屏幕共享。

## 两种方式的区别

最后总结一下 `-L` 直接转发和 `-J` 跳板转发这两种方式的区别：

| | `-L` 直接转发 | `-J` 跳板转发 |
|---|---|---|
| 原理 | SSH 服务器作为代理去连接目标端口 | SSH 通过跳板机建立到目标机器的连接，再在目标机器上做本地转发 |
| 依赖 | 需要 SSH 服务器开启 `AllowTcpForwarding` | 不依赖中间服务器的 `AllowTcpForwarding` |
| 目标机器需要开 SSH | 不需要 | 需要 |
| 命令 | `ssh -L 15900:目标IP:5900 跳板机` | `ssh -L 15900:localhost:5900 -J 跳板机 目标机` |

在实际使用中，如果 `-L` 方式遇到了 `administratively prohibited` 错误，换成 `-J` 方式通常就能解决问题。

## 参考

1. [SSH Port Forwarding - Local, Remote, and Dynamic](https://www.ssh.com/academy/ssh/tunneling-example)
2. [OpenSSH Manual - ssh_config](https://man.openbsd.org/ssh_config)
3. [SSH Tunneling (Port Forwarding) 详解](https://www.ruanyifeng.com/blog/2011/12/ssh_port_forwarding.html)

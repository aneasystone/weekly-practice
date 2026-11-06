# WEEK063 - 用 SSH 反向隧道把没有公网 IP 的内网机器"暴露"出来

[上一周](../week062-ssh-tunnel-vnc-remote-access/README.md) 我用 SSH 的本地端口转发（`-L`）从家里访问到了公司内网的 Mac Mini。那个场景能成立有一个前提：**家里能 SSH 到公司内网的一台机器**——它有公网 IP，可以当跳板。

但还有一类更尴尬的场景：内网那台机器**完全没有公网入口**，外面任何方向都够不着它，连跳板都没有。比如放在家里 NAT 路由器后面的一台树莓派、公司内网里一台只能出不能进的服务器。这时候 `-L` 就用不上了，因为 `-L` 是"访问方主动伸手进去拿"，可现在根本伸不进去。

解决办法是反过来：**让内网那台机器自己主动向外打一条隧道**，连到一台你掌握的公网服务器上，并在公网服务器上"挂"出一个端口。之后你连这个端口，流量就顺着隧道回到内网机器。这就是 SSH 的 **远程端口转发（Remote Port Forwarding）**，也常被叫做"反向隧道"或"内网穿透"。

## 网络拓扑

```
                       ┌─────────────────────────┐
内网机器(无公网IP) ──SSH──▶│ 公网 VPS :2222 (监听)   │◀── 你从外面连 VPS:2222
   (主动发起出站连接)       └─────────────────────────┘    流量顺隧道回到内网机器:22
```

注意箭头方向：隧道是**内网机器主动发起**的（它能出站访问公网 VPS，反过来 VPS 连不进内网机器）。隧道一旦建好，VPS 上就多了一个监听端口，谁连这个端口，等于连到了内网机器。

## SSH 远程端口转发

`ssh` 的 `-R` 参数语法：

```
ssh -R [绑定地址:]远程端口:目标地址:目标端口 用户名@SSH服务器
```

工作原理：在 **SSH 服务器（这里是公网 VPS）** 上监听"远程端口"，当有连接进来，把流量通过隧道送回**发起 SSH 的这一端**，再由它去连"目标地址:目标端口"。

把内网机器自己的 SSH（22 端口）暴露到 VPS 的 2222：

```
# 在内网机器上执行
$ ssh -R 2222:localhost:22 root@vps-ip
```

`localhost:22` 是相对于内网机器说的——隧道的目标是"内网机器自己的 22 端口"。

之后在 VPS 上：

```
$ ssh -p 2222 localhost
```

就连到了内网机器。如果想从**第三台机器**（不是 VPS 本机）连，得让 2222 监听在 `0.0.0.0` 而不是 `127.0.0.1`，见下一节。

## 坑一：监听地址默认是 127.0.0.1

我把命令改成了 `-R 0.0.0.0:2222:localhost:22`，想让别的机器也能连这个 2222 端口，结果在 VPS 上 `ss -tlnp | grep 2222` 看到的还是 `127.0.0.1:2222`。

原因是：服务器端 `sshd` 默认**不允许**远程转发绑定到非回环地址，由 VPS 的 `/etc/ssh/sshd_config` 里的 `GatewayPorts` 控制，**和客户端怎么写无关**。它默认是 `no`，此时不管你 `-R` 前面写 `0.0.0.0` 还是 `*`，sshd 都强制改回 `127.0.0.1`。

`GatewayPorts` 三个取值：

| 值 | 行为 |
|---|---|
| `no`（默认） | 强制只绑 `127.0.0.1`，客户端指定的绑定地址被忽略 |
| `yes` | 一律绑到所有网卡（`0.0.0.0`） |
| `clientspecified` | 听客户端的：`-R 0.0.0.0:2222:...` 绑全部，`-R 127.0.0.1:2222:...` 只绑本地，`-R 1.2.3.4:2222:...` 绑指定 IP |

推荐 `clientspecified`——默认行为仍然安全（不写绑定地址就只绑本地），需要对外时显式写 `0.0.0.0`，控制权在建隧道的人手里。改 VPS 的 `/etc/ssh/sshd_config`：

```
GatewayPorts clientspecified
```

然后重启 sshd。我这台 VPS 是 Ubuntu 14.04（用的是 Upstart，没有 systemd），所以是：

```
$ service ssh restart      # 注意服务名是 ssh 不是 sshd
```

> 用 systemd 的系统是 `systemctl restart sshd`；OpenRC（如 Alpine）是 `rc-service sshd restart`。重启 sshd 不会踢掉当前已建立的 SSH 会话，放心。

验证：

```
$ sshd -T | grep -i gatewayports
gatewayports clientspecified

$ ss -tlnp | grep 2222
LISTEN 0 128 0.0.0.0:2222 0.0.0.0:* users:(("sshd",...))
```

还有一点别忘了：如果 VPS 在云厂商那里（阿里云、腾讯云之类），**安全组 / 防火墙也要放行 2222 入站**，否则外部还是连不上。

## 坑二：隧道会断，要保活 + 自动重连

直接 `ssh -R ...` 跑着的隧道，时间一长——NAT 超时、网络抖动、对端重启——就会悄无声息地断掉，而且不会自己恢复。两件事要做：

**1. SSH 自身的保活**，让它能及时发现连接死了：

```
-o "ServerAliveInterval 30" -o "ServerAliveCountMax 3"
```

每 30 秒发一个探测包，连续 3 次（约 90 秒）没回应就判定断开。

**2. 用 `autossh` 包一层**，断了自动重连：

```
$ autossh -M 0 -N \
    -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" \
    -R 0.0.0.0:2222:localhost:22 root@vps-ip
```

逐段解释：

| 部分 | 含义 |
|---|---|
| `autossh` | ssh 的包装器，监控连接、断了自动重连 |
| `-M 0` | 关闭 autossh 自带的"监控端口"机制，改为完全依赖上面的 `ServerAlive*` 来判断连接死活——这是现在推荐的用法 |
| `-N` | 不执行远程命令，只做端口转发 |
| `-R 0.0.0.0:2222:localhost:22` | 在 VPS 上监听 `0.0.0.0:2222`，转发到内网机器的 `localhost:22` |
| `root@vps-ip` | 登录公网 VPS 的账号 |

这条命令在内网机器上跑起来后，从外面任意一台机器：

```
$ ssh -p 2222 your-user@vps-ip
```

就连进了内网机器。

> 不只 SSH，把 `localhost:22` 换成内网机器上别的服务即可转发其它端口，比如 `-R 0.0.0.0:8080:localhost:80` 把内网的 Web 服务暴露出来。

## 让它开机自启、常驻后台

反向隧道通常是要"长期在线"的，所以最好做成服务。如果内网机器是 systemd 系统，写一个 unit：

```ini
# /etc/systemd/system/reverse-tunnel.service
[Unit]
Description=Reverse SSH tunnel to VPS
After=network-online.target
Wants=network-online.target

[Service]
User=tunnel
Environment=AUTOSSH_GATETIME=0
ExecStart=/usr/bin/autossh -M 0 -N \
  -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" \
  -o "ExitOnForwardFailure yes" -o "StrictHostKeyChecking accept-new" \
  -R 0.0.0.0:2222:localhost:22 root@vps-ip
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

几个补充：

- `AUTOSSH_GATETIME=0`：让 autossh 即使第一次就连失败也持续重试（默认它要求第一次连接活够一段时间才肯重连）。
- `ExitOnForwardFailure yes`：如果端口转发没建立成功（比如 VPS 上 2222 被占了），直接退出，交给 systemd 重启，避免出现"SSH 连上了但隧道是死的"这种假活状态。
- 隧道账号要配好**免密登录**（密钥），并且密钥**不能设密码短语**，否则服务起不来。
- 不想用 systemd，最低限度也可以 `nohup autossh ... &` 加进 `rc.local` / crontab `@reboot`，或者塞进 `tmux`。

启用：

```
$ sudo systemctl daemon-reload
$ sudo systemctl enable --now reverse-tunnel
$ systemctl status reverse-tunnel
```

## 安全：等于把内网机器的 SSH 摆到了公网上

这一步做完，VPS 的 2222 端口背后就是内网机器的 SSH——全世界的扫描器、爆破脚本天天扫，默认配置往往不够"硬"。在**内网那台机器**上至少做这些（改 `/etc/ssh/sshd_config`，改完重启 sshd）：

```
PasswordAuthentication no       # 禁用密码登录，只允许密钥 —— 最重要的一条
PermitRootLogin no              # 禁止 root 直接 SSH（或 prohibit-password）
PermitEmptyPasswords no
AllowUsers youruser             # 只允许特定用户登录
MaxAuthTries 3
```

> 关密码登录前，**先确认密钥能登进去**，否则会把自己锁在外面。

再加几样：

- 装 `fail2ban`，自动封禁短时间内多次登录失败的 IP，能挡掉绝大多数无脑爆破；
- 用 `clientspecified` + `-R <你的固定出口IP>:2222:...` 在隧道层就把来源收窄；
- 隧道账号在 VPS 上建个专用低权限账号，别用 root；可以在它的 `authorized_keys` 里加 `command="",no-pty,no-X11-forwarding,permitlisten="2222"` 之类的限制，让这把密钥只能用来打隧道，不能登 shell。

一句话：公网上暴露一个允许密码登录的 SSH，被爆破只是时间问题——**密钥登录 + 禁 root + 禁密码 + fail2ban** 配齐再上线。

## 顺手记一下：前台进程怎么转后台还不退出

调试隧道时常用到。一个已经在前台跑的程序：

```
Ctrl+Z      # 挂起，交回 shell
$ bg        # 让它在后台继续运行
$ disown    # 从当前 shell 的任务列表摘出去，关终端也不影响它
```

`Ctrl+Z` → `bg` → `disown` 三步。不过要留日志的话，更推荐一开始就 `nohup cmd > out.log 2>&1 &`，或者直接用 `tmux` / `screen`。

## `-L` 和 `-R` 的区别

接着 week062 一起对照：

| | `-L` 本地转发（week062） | `-R` 远程转发 / 反向隧道（本周） |
|---|---|---|
| 谁发起隧道 | 访问方（家里的 Mac） | 被访问的内网机器 |
| 适用场景 | 我能 SSH 到跳板，借它访问内网某端口 | 内网机器没有公网入口，需要它主动暴露自己 |
| 中间服务器角色 | 被动跳板 | 隧道的汇聚点，对外监听端口 |
| 关键服务器配置 | `AllowTcpForwarding`（`-J` 可绕过） | `GatewayPorts`（要让别的机器也能连那个端口时） |
| 典型形态 | 临时、用完即走 | 长驻，配 autossh + systemd 保活 |
| 形象比喻 | 我从外面伸手进去拿 | 让里面的人把东西递出来 |

选哪个，就看那台你想访问的机器**有没有一个能让你 SSH 进去的入口**：有（哪怕是个跳板）→ 用 `-L`/`-J`，内网机器上啥都不用装；没有 → 用 `-R` + autossh，让它自己打洞出来。

## 参考

1. [autossh - Automatically restart SSH sessions and tunnels](https://www.harding.motd.ca/autossh/)
2. [OpenSSH Manual - ssh(1)](https://man.openbsd.org/ssh)，`-R` 与 `-L` 部分
3. [OpenSSH Manual - sshd_config(5)](https://man.openbsd.org/sshd_config)，`GatewayPorts`、`AllowTcpForwarding` 部分
4. [SSH Port Forwarding - Local, Remote, and Dynamic](https://www.ssh.com/academy/ssh/tunneling-example)

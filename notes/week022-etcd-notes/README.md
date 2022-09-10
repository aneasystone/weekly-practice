# WEEK022 - etcd 学习笔记

[etcd](https://etcd.io/) 是一个使用 Go 语言编写的用于存储分布式系统中的数据的高可用键值数据库（key-value store），它是 CoreOS 团队在 2013 年 6 月发起的开源项目，并在 2018 年 12 月正式加入 [CNCF](https://www.cncf.io/)。我们知道在 Linux 操作系统中有一个目录叫 `/etc`，它是专门用来存储操作系统配置的地方，`etcd` 这个名词就是源自于此，`etcd = etc + distibuted`，所以它的目的就是用来存储分布式系统中的关键数据。

![](./images/etcd.png)

etcd 内部采用 [Raft 一致性算法](http://thesecretlivesofdata.com/raft/)，以一致和容错的方式存储元数据。利用 etcd 可以实现包括配置管理、服务发现和协调分布式任务这些功能，另外 etcd 还提供了一些常用的分布式模式，包括领导选举，分布式锁和监控机器活动等。

etcd 已经被各大公司和开源项目广泛使用，最著名的莫过于 Kubernetes 就是使用 etcd 来存储配置数据的，etcd 的一致性对于正确安排和运行服务至关重要，Kubernetes 的 API Server 将集群状态持久化在 etcd 中，通过 etcd 的 Watch API 监听集群，并发布关键的配置更改。

![](./images/k8s-apiserver-etcd.png)

## 快速开始

这一节我们将学习如何在本地快速启动一个单节点的 etcd 服务，并学习 etcd 的基本使用。

### 安装

首先从 [GitHub Releases](https://github.com/etcd-io/etcd/releases/) 页面下载和你的操作系统对应的最新版本：

```
$ curl -LO https://github.com/etcd-io/etcd/releases/download/v3.4.20/etcd-v3.4.20-linux-amd64.tar.gz
```

解压并安装到 `/usr/local/etcd` 目录：

```
$ tar xzvf etcd-v3.4.20-linux-amd64.tar.gz -C /usr/local/etcd --strip-components=1
```

目录下包含了 `etcd` 和 `etcdctl` 两个可执行文件，`etcdctl` 是 `etcd` 的命令行客户端。另外，还包含一些 Markdown 文档：

```
$ ls /usr/local/etcd
Documentation  README-etcdctl.md  README.md  READMEv2-etcdctl.md  etcd  etcdctl
```

然后将 `/usr/local/etcd` 目录添加到 `PATH` 环境变量（如果要让配置永远生效，可以将下面一行添加到 `~/.profile` 文件中）：

```
export PATH=$PATH:/usr/local/etcd
```

至此，etcd 就安装好了，使用 `etcd --version` 检查版本：

```
$ etcd --version
etcd Version: 3.4.20
Git SHA: 1e26823
Go Version: go1.16.15
Go OS/Arch: linux/amd64
```

### 启动

直接不带参数运行 `etcd` 命令，即可（a single-member cluster of etcd）：

```
$ etcd
[WARNING] Deprecated '--logger=capnslog' flag is set; use '--logger=zap' flag instead
2022-09-06 07:21:49.244548 I | etcdmain: etcd Version: 3.4.20
2022-09-06 07:21:49.253270 I | etcdmain: Git SHA: 1e26823
2022-09-06 07:21:49.253486 I | etcdmain: Go Version: go1.16.15
2022-09-06 07:21:49.253678 I | etcdmain: Go OS/Arch: linux/amd64
2022-09-06 07:21:49.253846 I | etcdmain: setting maximum number of CPUs to 8, total number of available CPUs is 8
2022-09-06 07:21:49.253981 W | etcdmain: no data-dir provided, using default data-dir ./default.etcd
2022-09-06 07:21:49.254907 N | etcdmain: the server is already initialized as member before, starting as etcd member...
[WARNING] Deprecated '--logger=capnslog' flag is set; use '--logger=zap' flag instead
2022-09-06 07:21:49.264084 I | embed: name = default
2022-09-06 07:21:49.264296 I | embed: data dir = default.etcd
2022-09-06 07:21:49.264439 I | embed: member dir = default.etcd/member
2022-09-06 07:21:49.264667 I | embed: heartbeat = 100ms
2022-09-06 07:21:49.264885 I | embed: election = 1000ms
2022-09-06 07:21:49.265079 I | embed: snapshot count = 100000
2022-09-06 07:21:49.265244 I | embed: advertise client URLs = http://localhost:2379
2022-09-06 07:21:49.265389 I | embed: initial advertise peer URLs = http://localhost:2380
2022-09-06 07:21:49.265681 I | embed: initial cluster =
2022-09-06 07:21:49.302456 I | etcdserver: restarting member 8e9e05c52164694d in cluster cdf818194e3a8c32 at commit index 5
raft2022/09/06 07:21:49 INFO: 8e9e05c52164694d switched to configuration voters=()
raft2022/09/06 07:21:49 INFO: 8e9e05c52164694d became follower at term 2
raft2022/09/06 07:21:49 INFO: newRaft 8e9e05c52164694d [peers: [], term: 2, commit: 5, applied: 0, lastindex: 5, lastterm: 2]
2022-09-06 07:21:49.312871 W | auth: simple token is not cryptographically signed
2022-09-06 07:21:49.319814 I | etcdserver: starting server... [version: 3.4.20, cluster version: to_be_decided]
raft2022/09/06 07:21:49 INFO: 8e9e05c52164694d switched to configuration voters=(10276657743932975437)
2022-09-06 07:21:49.329816 I | etcdserver/membership: added member 8e9e05c52164694d [http://localhost:2380] to cluster cdf818194e3a8c32
2022-09-06 07:21:49.331278 N | etcdserver/membership: set the initial cluster version to 3.4
2022-09-06 07:21:49.331489 I | etcdserver/api: enabled capabilities for version 3.4
2022-09-06 07:21:49.333146 I | embed: listening for peers on 127.0.0.1:2380
raft2022/09/06 07:21:50 INFO: 8e9e05c52164694d is starting a new election at term 2
raft2022/09/06 07:21:50 INFO: 8e9e05c52164694d became candidate at term 3
raft2022/09/06 07:21:50 INFO: 8e9e05c52164694d received MsgVoteResp from 8e9e05c52164694d at term 3
raft2022/09/06 07:21:50 INFO: 8e9e05c52164694d became leader at term 3
raft2022/09/06 07:21:50 INFO: raft.node: 8e9e05c52164694d elected leader 8e9e05c52164694d at term 3
2022-09-06 07:21:50.419379 I | etcdserver: published {Name:default ClientURLs:[http://localhost:2379]} to cluster cdf818194e3a8c32
2022-09-06 07:21:50.419988 I | embed: ready to serve client requests
2022-09-06 07:21:50.427600 N | embed: serving insecure client requests on 127.0.0.1:2379, this is strongly discouraged!
```

该命令会在当前位置创建一个 `./default.etcd` 目录作为数据目录，并监听 2379 和 2380 两个端口，`http://localhost:2379` 为 `advertise-client-urls`，表示建议使用的客户端通信 url，可以配置多个，`etcdctl` 就是通过这个 url 来访问 `etcd` 的；`http://localhost:2380` 为 `advertise-peer-urls`，表示用于节点之间通信的 url，也可以配置多个，集群内部通过这些 url 进行数据交互（如选举，数据同步等）。

### 测试

打开另一个终端，输入 `etcdctl put` 命令可以向 etcd 中以键值对的形式写入数据：

```
$ etcdctl put hello world
OK
```

然后使用 `etcdctl get` 命令可以根据键值读取数据：

```
$ etcdctl get hello
hello
world
```

## 搭建 etcd 集群

上面的例子中，我们在本地启动了一个单节点的 etcd 服务，一般用于开发和测试。在生产环境中，我们需要搭建高可用的 etcd 集群。

启动一个 etcd 集群要求集群中的每个成员都要知道集群中的其他成员，最简单的做法是在启动 etcd 服务时加上 `--initial-cluster` 参数告诉 etcd 初始集群中有哪些成员，这种方法也被称为 **静态配置**。

我们在本地打开三个终端，并在三个终端中分别运行下面三个命令：

```
$ etcd --name infra1 \
	--listen-client-urls http://127.0.0.1:12379 \
	--advertise-client-urls http://127.0.0.1:12379 \
	--listen-peer-urls http://127.0.0.1:12380 \
	--initial-advertise-peer-urls http://127.0.0.1:12380 \
	--initial-cluster-token etcd-cluster-demo \
	--initial-cluster 'infra1=http://127.0.0.1:12380,infra2=http://127.0.0.1:22380,infra3=http://127.0.0.1:32380' \
	--initial-cluster-state new
```

```
$ etcd --name infra2 \
	--listen-client-urls http://127.0.0.1:22379 \
	--advertise-client-urls http://127.0.0.1:22379 \
	--listen-peer-urls http://127.0.0.1:22380 \
	--initial-advertise-peer-urls http://127.0.0.1:22380 \
	--initial-cluster-token etcd-cluster-demo \
	--initial-cluster 'infra1=http://127.0.0.1:12380,infra2=http://127.0.0.1:22380,infra3=http://127.0.0.1:32380' \
	--initial-cluster-state new
```

```
$ etcd --name infra3 \
	--listen-client-urls http://127.0.0.1:32379 \
	--advertise-client-urls http://127.0.0.1:32379 \
	--listen-peer-urls http://127.0.0.1:32380 \
	--initial-advertise-peer-urls http://127.0.0.1:32380 \
	--initial-cluster-token etcd-cluster-demo \
	--initial-cluster 'infra1=http://127.0.0.1:12380,infra2=http://127.0.0.1:22380,infra3=http://127.0.0.1:32380' \
	--initial-cluster-state new
```

> 我们可以使用 [Foreman](https://github.com/ddollar/foreman) 这个小工具来简化上面的过程，Foreman 通过一个 [Procfile](https://github.com/etcd-io/etcd/blob/main/Procfile) 文件在本地启动和管理多个进程。

我们随便选择一个节点，通过 `member list` 都可以查询集群中的所有成员：

```
$ etcdctl --write-out=table --endpoints=localhost:12379 member list
+------------------+---------+--------+------------------------+------------------------+------------+
|        ID        | STATUS  |  NAME  |       PEER ADDRS       |      CLIENT ADDRS      | IS LEARNER |
+------------------+---------+--------+------------------------+------------------------+------------+
| b217c7a319e4e4f8 | started | infra2 | http://127.0.0.1:22380 | http://127.0.0.1:22379 |      false |
| d35bfbeb1c7fbfcf | started | infra1 | http://127.0.0.1:12380 | http://127.0.0.1:12379 |      false |
| d425e5b1e0d8a751 | started | infra3 | http://127.0.0.1:32380 | http://127.0.0.1:32379 |      false |
+------------------+---------+--------+------------------------+------------------------+------------+
```

测试往集群中写入数据：

```
$ etcdctl --endpoints=localhost:12379 put hello world
OK
```

换一个节点也可以查出数据：

```
$ etcdctl --endpoints=localhost:22379 get hello
hello
world
```

但是一般为了保证高可用，我们会在 `--endpoints` 里指定集群中的所有成员：

```
$ etcdctl --endpoints=localhost:12379,localhost:22379,localhost:32379 get hello
hello
world
```

然后我们停掉一个 etcd 服务，可以发现集群还可以正常查询，说明高可用生效了，然后我们再停掉一个 etcd 服务，此时集群就不可用了，这是因为 Raft 协议必须要保证集群中一半以上的节点存活才能正常工作，可以看到集群中的唯一节点也异常退出了：

```
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x18 pc=0x75745b]

goroutine 188 [running]:
go.uber.org/zap.(*Logger).check(0x0, 0x1, 0x10a3ea5, 0x36, 0xc002068900)
        /root/go/pkg/mod/go.uber.org/zap@v1.10.0/logger.go:264 +0x9b
go.uber.org/zap.(*Logger).Warn(0x0, 0x10a3ea5, 0x36, 0xc002068900, 0x2, 0x2)
        /root/go/pkg/mod/go.uber.org/zap@v1.10.0/logger.go:194 +0x45
go.etcd.io/etcd/etcdserver.(*EtcdServer).requestCurrentIndex(0xc0002b4000, 0xc001fef200, 0xbfcf831fa9e8b606, 0x0, 0x0, 0x0)
        /tmp/etcd-release-3.4.20/etcd/release/etcd/etcdserver/v3_server.go:805 +0x873
go.etcd.io/etcd/etcdserver.(*EtcdServer).linearizableReadLoop(0xc0002b4000)
        /tmp/etcd-release-3.4.20/etcd/release/etcd/etcdserver/v3_server.go:721 +0x2d6
go.etcd.io/etcd/etcdserver.(*EtcdServer).goAttach.func1(0xc0002b4000, 0xc00011c4a0)
        /tmp/etcd-release-3.4.20/etcd/release/etcd/etcdserver/server.go:2698 +0x57
created by go.etcd.io/etcd/etcdserver.(*EtcdServer).goAttach
        /tmp/etcd-release-3.4.20/etcd/release/etcd/etcdserver/server.go:2696 +0x1b1
```

使用静态的方法运行 etcd 集群虽然简单，但是这种方法必须提前规划好集群中所有成员的 IP 和端口，在有些场景下成员的地址是无法提前知道的，这时我们可以使用 **动态配置** 的方法来初始化集群，etcd 提供了两种动态配置的机制：**etcd Discovery** 和 **DNS Discovery**，具体的内容可以参考 [Clustering Guide](https://etcd.io/docs/v3.5/op-guide/clustering/) 和 [Discovery service protocol](https://etcd.io/docs/v3.5/dev-internal/discovery_protocol/)。

## 操作 etcd

有多种不同的途径来操作 etcd，比如使用 etcdctl 命令行，使用 API 接口，或者使用 etcd 提供的不同语言的 SDK。

### 使用 etcdctl 命令行操作 etcd

在快速开始一节，我们使用 `etcdctl put` 和 `etcdctl get` 来测试 etcd 是否可以正常写入和读取数据，这是 etcdctl 最常用的命令。

#### 查看版本

通过 `etcdctl version` 查看 etcdctl 客户端和 etcd API 的版本：

```
$ etcdctl version
etcdctl version: 3.4.20
API version: 3.4
```

#### 写入数据

通过 `etcdctl put` 将数据存储在 etcd 的某个键中，每个存储的键通过 Raft 协议复制到 etcd 集群的所有成员来实现一致性和可靠性。下面的命令将键 `hello` 的值设置为 `world`:

```
$ etcdctl put hello world
OK
```

etcd 支持为每个键设置 TTL 过期时间，这是通过租约（`--lease`）实现的。首先我们创建一个 100s 的租约：

```
$ etcdctl lease grant 100
lease 694d8324b408010a granted with TTL(100s)
```

然后写入键值时带上这个租约：

```
$ etcdctl put foo bar --lease=694d8324b408010a
OK
```

`foo` 这个键将在 100s 之后自动过期。

#### 读取数据

我们提前往 etcd 中写入如下数据：

```
$ etcdctl put foo bar
$ etcdctl put foo1 bar1
$ etcdctl put foo2 bar2
$ etcdctl put foo3 bar3
```

读取某个键的值：

```
$ etcdctl get foo
foo
bar
```

默认情况下会将键和值都打印出来，使用 `--print-value-only` 可以只打印值：

```
$ etcdctl get foo --print-value-only
bar
```

或者使用 `--keys-only` 只打印键。

我们也可以使用两个键进行范围查询：

```
$ etcdctl get foo foo3
foo
bar
foo1
bar1
foo2
bar2
```

可以看出查询的范围为半开区间 `[foo, foo3)`，

或者使用 `--prefix` 参数进行前缀查询，比如查询所有 `foo` 开头的键：

```
$ etcdctl get foo --prefix
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

我们甚至可以使用 `etcdctl get "" --prefix` 查询出所有的键。使用 `--limit` 限制查询数量：

```
$ etcdctl get "" --prefix --limit=2
foo
bar
foo1
bar1
```

#### 删除数据

和 `etcdctl get` 一样，我们可以从 etcd 中删除一个键：

```
$ etcdctl del foo
1
```

也可以范围删除：

```
$ etcdctl del foo foo3
2
```

或者根据前缀删除：

```
$ etcdctl del --prefix foo
1
```

#### 历史版本

etcd 会记录所有键的修改历史版本，每次对 etcd 进行修改操作时，版本号就会加一。使用 `etcdctl get foo` 查看键值时，可以通过 `--write-out=json` 参数看到版本号：

```
$ etcdctl get foo --write-out=json | jq
{
    "header": {
        "cluster_id": 14841639068965178418,
        "member_id": 10276657743932975437,
        "revision": 9,
        "raft_term": 2
    },
    "kvs": [
        {
            "key": "Zm9v",
            "create_revision": 5,
            "mod_revision": 5,
            "version": 1,
            "value": "YmFy"
        }
    ],
    "count": 1
}
```

其中 `"revision": 9` 就是当前的版本号，注意 JSON 格式输出中 key 和 value 是 BASE64 编码的。

修改 `foo` 的值：

```
$ etcdctl put foo bar_new
OK
```

查看最新的键值和版本：

```
$ etcdctl get foo --write-out=json | jq
{
    "header": {
        "cluster_id": 14841639068965178418,
        "member_id": 10276657743932975437,
        "revision": 10,
        "raft_term": 2
    },
    "kvs": [
        {
            "key": "Zm9v",
            "create_revision": 5,
            "mod_revision": 10,
            "version": 2,
            "value": "YmFyX25ldw=="
        }
    ],
    "count": 1
}
```

发现版本号已经加一变成了 10，此时如果使用 `etcdctl get foo` 查看的当前最新版本的值，也可以通过 `--rev` 参数查看历史版本的值：

```
$ etcdctl get foo
foo
bar_new

$ etcdctl get foo --rev=9
foo
bar
```

过多的历史版本会占用 etcd 的资源，我们可以将不要的历史记录清除掉：

```
$ etcdctl compact 10
compacted revision 10
```

上面的命令将版本号为 10 之前的历史记录删除掉，此时再查询 10 之前版本就会报错：

```
$ etcdctl get foo --rev=9
{"level":"warn","ts":"2022-09-10T09:48:41.021+0800","caller":"clientv3/retry_interceptor.go:62","msg":"retrying of unary invoker failed","target":"endpoint://client-ae27c266-06c4-4be8-9659-47b9318ec8f4/127.0.0.1:2379","attempt":0,"error":"rpc error: code = OutOfRange desc = etcdserver: mvcc: required revision has been compacted"}
Error: etcdserver: mvcc: required revision has been compacted
```

#### 监听键值变化

使用 `etcdctl watch` 可以监听某个键的变动情况：

```
$ etcdctl watch foo
```

打开另一个终端修改 `foo` 的值，然后将键删除：

```
$ etcdctl put foo bar_new
OK
$ etcdctl del foo
1
```

在监听窗口我们可以实时看到键值的变化：

```
$ etcdctl watch foo
PUT
foo
bar_new
DELETE
foo

```

也可以监听某个范围内的键：

```
$ etcdctl watch foo foo3
```

或以监听指定前缀的所有键：

```
$ etcdctl watch --prefix foo
```

如果要监听的键没有相同的前缀，也不是在某个范围内，可以通过 `watch -i` 以交互的形式手工设置监听多个键：

```
$ etcdctl watch -i
watch foo
watch hello
```

另外通过 watch 命令还可以查看某个键的所有历史修改记录：

```
$ etcdctl watch --rev=1 foo
PUT
foo
bar
DELETE
foo

PUT
foo
bar
PUT
foo
bar_new
```

#### 租约

在上面使用 `etcdctl put` 写入数据时，已经介绍了可以通过租约实现 TTL 功能，每个租约都带有一个存活时间，一旦租约到期，它绑定的所有键都将被删除。

创建一个租约：

```
$ etcdctl lease grant 100
lease 694d8324b4080150 granted with TTL(100s)
```

查询租约信息：

```
$ etcdctl lease timetolive 694d8324b4080150
lease 694d8324b4080150 granted with TTL(100s), remaining(96s)
```

查询租约信息时，也可以加上 `--keys` 参数查询该租约关联的键：

```
$ etcdctl lease timetolive --keys 694d8324b4080150
lease 694d8324b4080150 granted with TTL(100s), remaining(93s), attached keys([foo])
```

还可以通过 `keep-alive` 命令自动维持租约：

```
$ etcdctl lease keep-alive 694d8324b4080150
```

etcd 会每隔一段时间刷新该租约的到期时间，保证该租约一直处于存活状态。

最后我们通过 `revoke` 命令撤销租约：

```
$ etcdctl lease revoke 694d8324b4080150
lease 694d8324b4080150 revoked
```

租约撤销后，和该租约关联的键也会一并被删除掉。

#### 其他命令

使用 `etcdctl --help` 查看支持的其他命令。

### 使用 etcd API 操作 etcd

etcd 支持的大多数基础 API 都定义在 [api/etcdserverpb/rpc.proto](https://github.com/etcd-io/etcd/blob/main/api/etcdserverpb/rpc.proto) 文件中，官方的 [API reference](https://etcd.io/docs/v3.5/dev-guide/api_reference_v3/) 就是根据这个文件生成的。

etcd 将这些 API 分为 6 大类：

* service `KV`
    * Range
    * Put
    * DeleteRange
    * Txn
    * Compact
* service `Watch`
    * Watch
* service `Lease`
    * LeaseGrant
    * LeaseRevoke
    * LeaseKeepAlive
    * LeaseTimeToLive
    * LeaseLeases
* service `Cluster`
    * MemberAdd
    * MemberRemove
    * MemberUpdate
    * MemberList
    * MemberPromote
* service `Maintenance`
    * Alarm
    * Status
    * Defragment
    * Hash
    * HashKV
    * Snapshot
    * MoveLeader
    * Downgrade
* service `Auth`
    * AuthEnable
    * AuthDisable
    * AuthStatus
    * Authenticate
    * UserAdd
    * UserGet
    * UserList
    * UserDelete
    * UserChangePassword
    * UserGrantRole
    * UserRevokeRole
    * RoleAdd
    * RoleGet
    * RoleList
    * RoleDelete
    * RoleGrantPermission
    * RoleRevokePermission

实际上，每个接口都对应一个 HTTP 请求，比如上面执行的 `etcdctl put` 命令就是调用 `KV.Put` 接口，而 `etcdctl get` 命令就是调用 `KV.Range` 接口。

调用 `KV.Put` 写入数据（注意接口中键值对使用 BASE64 编码，这里的键为 key，值为 value）：

```
$ curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "a2V5", "value": "dmFsdWU="}'
{"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"24","raft_term":"3"}}
```

调用 `KV.Range` 查询数据：

```
curl -L http://localhost:2379/v3/kv/range \
  -X POST -d '{"key": "a2V5"}'
{"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"24","raft_term":"3"},"kvs":[{"key":"a2V5","create_revision":"24","mod_revision":"24","version":"1","value":"dmFsdWU="}],"count":"1"}
```

这和使用 `etcdctl` 命令行查询效果是一样的：

```
$ etcdctl get key
key
value
```

除了这 6 类基础 API，etcd 还提供了两个并发类 API，包括分布式锁和集群选主：

* [service `Lock`](https://github.com/etcd-io/etcd/blob/main/server/etcdserver/api/v3lock/v3lockpb/v3lock.proto)
    * Lock
    * Unlock
* [service `Election`](https://github.com/etcd-io/etcd/blob/main/server/etcdserver/api/v3election/v3electionpb/v3election.proto)
    * Campaign
    * Proclaim
    * Leader
    * Observe
    * Resign

### 使用 Go 语言操作 etcd

## 安全性

### 开启用户角色认证

https://etcd.io/docs/v3.5/op-guide/authentication/rbac/

### 开启 TLS 证书认证

https://etcd.io/docs/v3.5/op-guide/security/

## etcd 和 其他键值存储的区别

### etcd vs. Redis

Redis 和 etcd 一样，支持键值存储，而且也支持分布式特性，他们之间的差异如下：

* Redis 支持的数据类型比 etcd 更丰富
* Redis 在分布式环境下不是强一致的，可能会丢数据或读取不到最新数据
* Redis 的数据监听机制没有 etcd 完善
* etcd 为了保证强一致性，性能要低于 Redis

综上考虑，Redis 适用于缓存，需要频繁读写，但对系统没有强一致性的要求，etcd 适用于系统读写较少，但是对系统有强一致性要求的场景，比如存储分布式系统的元数据。

### etcd vs. ZooKeeper

ZooKeeper 和 etcd 的定位都是分布式协调系统，ZooKeeper 起源于 Hadoop 生态系统，etcd 则是跟着 Kubernetes 的流行而流行。他们都是顺序一致性的（满足 CAP 的 CP），意味着无论你访问任意节点，都将获得最终一致的数据。他们之间的差异如下：

* ZooKeeper 从逻辑上来看是一种目录结构，而 etcd 从逻辑上来看就是一个 KV 结构，不过 etcd 的 Key 可以是任意字符串，所以也可以模拟出目录结构
* etcd 使用 Raft 算法实现一致性，比 ZooKeeper 的 ZAB 算法更简单
* ZooKeeper 采用 Java 编写，etcd 采用 Go 编写，相比而言 ZooKeeper 的部署复杂度和维护成本要高一点，而且 ZooKeeper 的官方只提供了 Java 和 C 的客户端，对其他编程语言不是很友好
* ZooKeeper 属于 Apache 基金会顶级项目，发展较缓慢，而 etcd 得益于云原生，近几年发展势头迅猛
* etcd 提供了 gRPC 或 HTTP 接口使用起来更简单
* ZooKeeper 使用 SASL 进行安全认证，而 etcd 支持 TLS 客户端安全认证，更容易使用

总体来说，ZooKeeper 和 etcd 还是很相似的，在 [week019-various-usage-of-zookeeper](../week019-various-usage-of-zookeeper/README.md) 这篇文章中介绍了一些 ZooKeeper 的使用场景，我们使用 etcd 同样也都可以实现。在具体选型上，我们应该更关注是否契合自己所使用的技术栈。

## 参考

1. [Etcd Quickstart](https://etcd.io/docs/v3.5/quickstart/) - Get etcd up and running in less than 5 minutes!
1. [Etcd 中文文档](http://www.zhaowenyu.com/etcd-doc/)
1. [Etcd 官方文档中文版](https://doczhcn.gitbook.io/etcd/)
1. [Etcd 教程 | 编程宝库](http://www.codebaoku.com/etcd/etcd-index.html)
1. [etcd 教程 | 梯子教程](https://www.tizi365.com/archives/557.html)
1. [七张图了解Kubernetes内部的架构](https://segmentfault.com/a/1190000022973856)

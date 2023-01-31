# WEEK030 - APISIX 使用小记

[Apache APISIX](https://apisix.apache.org/zh/) 是基于 Nginx/OpenResty + Lua 方案打造的一款 **动态**、**实时**、**高性能** 的 **云原生** API 网关，提供了负载均衡、动态上游、灰度发布、服务熔断、身份认证、可观测性等丰富的流量管理功能。APISIX 由国内初创公司 [支流科技](https://www.apiseven.com/) 于 2019 年 6 月开源，并于 7 月纳入 CNCF 全景图，10 月进入 Apache 孵化器，次年 7 月 毕业，成为国内唯一一个由初创公司贡献的项目，也是中国最快毕业的 Apache 顶级项目。

## 入门示例

学习一门技术最好的方法就是使用它。这一节，我们将通过官方的入门示例，对 APISIX 的概念和用法有个基本了解。

首先，我们下载 [apisix-docker](https://github.com/apache/apisix-docker) 仓库：

```
git clone https://github.com/apache/apisix-docker.git
```

这个仓库主要是用来指导用户如何使用 Docker 部署 APISIX 的，其中有一个 example 目录，是官方提供的入门示例，我们可以直接使用 `docker-compose` 运行它：

```
$ cd apisix-docker/example
$ docker-compose up -d
[+] Running 8/8
 - Network example_apisix                Created                         0.9s
 - Container example-web2-1              Started                         5.1s
 - Container example-web1-1              Started                         4.0s
 - Container example-prometheus-1        Started                         4.4s
 - Container example-grafana-1           Started                         5.8s
 - Container example-apisix-dashboard-1  Started                         6.0s
 - Container example-etcd-1              Started                         5.1s
 - Container example-apisix-1            Started                         7.5s
```

可以看到创建了一个名为 `example_apisix` 的网络，并在这个网络里启动了 7 个容器：

* `etcd` - APISIX 使用 etcd 作为配置中心，它通过监听 etcd 的变化来实时更新路由
* `apisix` - APISIX 网关
* `apisix-dashboard` - APISIX 管理控制台，可以在这里对 APISIX 的 Route、Upstream、Service、Consumer、Plugin、SSL 等进行管理
* `prometheus` - 这个例子使用了 APISIX 的 `prometheus` 插件，用于暴露 APISIX 的指标，Prometheus 服务用于采集这些指标
* `grafana` - Grafana 面板以图形化的方式展示 Prometheus 指标
* `web1` - 测试服务
* `web2` - 测试服务

部署之后可以使用 APISIX 的 [Admin API](https://apisix.apache.org/zh/docs/apisix/admin-api/) 检查其是否启动成功：

```
$ curl http://127.0.0.1:9180/apisix/admin/routes \
	-H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1'
{"list":[],"total":0}
```

目前我们还没有创建任何路由，所以 `/apisix/admin/routes` 接口返回的结果为空。我们可以使用 Admin API 和 Dashboard 两种方式来创建路由：

### 使用 Admin API 创建路由

**路由（ Route ）** 是 APISIX 中最基础和最核心的资源对象，APISIX 通过路由定义规则来匹配客户端请求，根据匹配结果加载并执行相应的插件，最后将请求转发给到指定的上游服务。一条路由主要包含三部分信息：

* 匹配规则：比如 `uri`、`host`、`remote_addr` 等等，你也可以自定义匹配规则。详细信息可参考 [Route body 请求参数](https://apisix.apache.org/zh/docs/apisix/admin-api/#route-request-body-parameters)；
* 插件配置：这是可选的，你可以根据需要，在路由中配置相应的插件来实现某些功能。详细信息可参考 [Plugin](https://apisix.apache.org/zh/docs/apisix/terminology/plugin/) 和 [Plugin Config](https://apisix.apache.org/zh/docs/apisix/terminology/plugin-config/)；
* 上游信息：路由会根据配置的负载均衡信息，将请求按照规则转发至相应的上游。详细信息可参考 [Upstream](https://apisix.apache.org/zh/docs/apisix/terminology/upstream/)。

下面的例子将入门示例中的 web1 服务添加到路由中：

```
$ curl -X PUT http://127.0.0.1:9180/apisix/admin/routes/1 \
-H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' -i -d '
{
    "uri": "/web1",
    "upstream": {
        "type": "roundrobin",
        "nodes": {
            "web1:80": 1
        }
    }
}'
```

如果路由创建成功，将返回下面的 `201 Created` 信息：

```
HTTP/1.1 201 Created
Connection: close
Transfer-Encoding: chunked
Access-Control-Allow-Credentials: true
Access-Control-Allow-Origin: *
Access-Control-Expose-Headers: *
Access-Control-Max-Age: 3600
Content-Type: application/json
Date: Tue, 31 Jan 2023 00:19:03 GMT
Server: APISIX/3.1.0
X-Api-Version: v3

{"key":"\/apisix\/routes\/1","value":{"create_time":1675124057,"uri":"\/web1","status":1,"upstream":{"pass_host":"pass","scheme":"http","nodes":{"web1:80":1},"hash_on":"vars","type":"roundrobin"},"priority":0,"update_time":1675124057,"id":"1"}}
```

然后我们就可以通过上面定义的 `uri` 来访问 web1 服务了：

```
$ curl http://localhost:9080/web1
hello web1
```

### 使用 Dashboard 创建路由

## 参考

1. [快速入门指南 | Apache APISIX® -- Cloud-Native API Gateway](https://apisix.apache.org/zh/docs/apisix/getting-started/)
1. [从 Apache APISIX 来看 API 网关的演进](https://opentalk-blog.b0.upaiyun.com/prod/2019-12-14/a4ae6b3784b87a46a3f43ed062e47391.pdf)
1. [云原生时代的中外 API 网关之争](https://2d2d.io/s1/kong-vs-apisix/)
1. [Apache APISIX 借助服务网格实现统一技术栈的全流量管理](https://cloudnative.to/blog/2022-service-mesh-summit-apache-apisix-mesh/)
1. [如何将 Apache APISIX 扩展为一个服务网格的边车](https://apisix.apache.org/articles/How-To-Extend-Apache-APISIX-into-a-Service-Mesh-Sidecar/)
1. [将 Apache APISIX 扩展为服务网格边车的探索与实践](https://www.infoq.cn/article/fuhshcgz7jp8gyowypbr)
1. [深度剖析 Apache APISIX Mesh Agent](https://www.apiseven.com/blog/how-to-use-mesh-agent)
1. [api7/apisix-mesh-agent](https://github.com/api7/apisix-mesh-agent)

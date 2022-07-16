# WEEK014 - 实战 ELK 搭建日志系统

`ELK` 是 `Elasticsearch` + `Logstash` + `Kibana` 的简称。`Elasticsearch` 是一个基于 `Lucene` 的分布式全文搜索引擎，提供 RESTful API 进行数据读写；`Logstash` 是一个收集，处理和转发事件和日志消息的工具；而 `Kibana` 是 Elasticsearch 的开源数据可视化插件，为查看存储在 Elasticsearch 提供了友好的 Web 界面，并提供了条形图，线条和散点图，饼图和地图等分析工具。

总的来说，Elasticsearch 负责存储数据，Logstash 负责收集日志，并将日志格式化后写入 Elasticsearch，Kibana 提供可视化访问 Elasticsearch 数据的功能。

## 安装 Elasticsearch

使用下面的 Docker 命令启动一个单机版 Elasticsearch 实例：

```
> docker run --name es -p 9200:9200 -p 9300:9300 -e ELASTIC_PASSWORD=123456 -d docker.elastic.co/elasticsearch/elasticsearch:8.3.2
```

从 Elasticsearch 8.0 开始，默认会开启安全特性，我们通过 `ELASTIC_PASSWORD` 环境变量设置访问密码，如果不设置，Elasticsearch 会在第一次启动时随机生成密码，查看启动日志可以发现类似下面这样的信息：

```
-------------------------------------------------------------------------------------------------------------------------------------
-> Elasticsearch security features have been automatically configured!
-> Authentication is enabled and cluster connections are encrypted.

->  Password for the elastic user (reset with `bin/elasticsearch-reset-password -u elastic`):
  dV0dN=eiH7CDtoe1IVS0

->  HTTP CA certificate SHA-256 fingerprint:
  4032719061cbafe64d5df5ef29157572a98aff6dae5cab99afb84220799556ff

->  Configure Kibana to use this cluster:
* Run Kibana and click the configuration link in the terminal when Kibana starts.
* Copy the following enrollment token and paste it into Kibana in your browser (valid for the next 30 minutes):
  eyJ2ZXIiOiI4LjMuMiIsImFkciI6WyIxNzIuMTcuMC4zOjkyMDAiXSwiZmdyIjoiNDAzMjcxOTA2MWNiYWZlNjRkNWRmNWVmMjkxNTc1NzJhOThhZmY2ZGFlNWNhYjk5YWZiODQyMjA3OTk1NTZmZiIsImtleSI6InNLUzdCSUlCU1dmOFp0TUg4M0VKOnVTaTRZYURlUk1LMXU3SUtaQ3ZzbmcifQ==

-> Configure other nodes to join this cluster:
* Copy the following enrollment token and start new Elasticsearch nodes with `bin/elasticsearch --enrollment-token <token>` (valid for the next 30 minutes):
  eyJ2ZXIiOiI4LjMuMiIsImFkciI6WyIxNzIuMTcuMC4zOjkyMDAiXSwiZmdyIjoiNDAzMjcxOTA2MWNiYWZlNjRkNWRmNWVmMjkxNTc1NzJhOThhZmY2ZGFlNWNhYjk5YWZiODQyMjA3OTk1NTZmZiIsImtleSI6InJxUzdCSUlCU1dmOFp0TUg4bkg3OmlLMU1tMUM3VFBhV2V1OURGWEFsWHcifQ==

  If you're running in Docker, copy the enrollment token and run:
  `docker run -e "ENROLLMENT_TOKEN=<token>" docker.elastic.co/elasticsearch/elasticsearch:8.3.2`
-------------------------------------------------------------------------------------------------------------------------------------
```

另外 Elasticsearch 使用了 HTTPS 通信，不过这个证书是不可信的，在浏览器里访问会有不安全的警告，使用 `curl` 访问时注意使用 `-k` 或 `--insecure` 忽略证书校验：

```
$ curl -X GET -s -k -u elastic:123456 https://localhost:9200 | jq
{
  "name": "2460ab74bdf6",
  "cluster_name": "docker-cluster",
  "cluster_uuid": "Yip76XCuQHq9ncLfzt_I1A",
  "version": {
    "number": "8.3.2",
    "build_type": "docker",
    "build_hash": "8b0b1f23fbebecc3c88e4464319dea8989f374fd",
    "build_date": "2022-07-06T15:15:15.901688194Z",
    "build_snapshot": false,
    "lucene_version": "9.2.0",
    "minimum_wire_compatibility_version": "7.17.0",
    "minimum_index_compatibility_version": "7.0.0"
  },
  "tagline": "You Know, for Search"
}
```

不过更安全的做法是将证书文件拷贝出来：

```
$ docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
```

然后使用证书访问 Elasticsearch：

```
$ curl --cacert http_ca.crt -u elastic https://localhost:9200
```

## 安装 Logstash

## 安装 Kibana

## 参考

1. [Install Elasticsearch with Docker](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)
1. [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
1. [Logstash Guide](https://www.elastic.co/guide/en/logstash/current/index.html)
1. [Filebeat Guide](https://www.elastic.co/guide/en/beats/filebeat/current/index.html)
1. [Kibana Guide](https://www.elastic.co/guide/en/kibana/current/index.html)
1. [ELK6.0部署：Elasticsearch+Logstash+Kibana搭建分布式日志平台](https://ken.io/note/elk-deploy-guide)
1. https://github.com/xuwujing/java-study
1. https://fuxiaopang.gitbooks.io/learnelasticsearch/
1. https://doc.yonyoucloud.com/doc/logstash-best-practice-cn/index.html
1. https://www.ibm.com/developerworks/cn/opensource/os-cn-elk-filebeat/index.html
1. https://blog.csdn.net/mawming/article/details/78344939

## 更多

### 在 WSL Ubuntu 中访问 Docker Desktop

在 WSL Ubuntu 中安装 docker 客户端：

```
$ curl -O https://download.docker.com/linux/static/stable/x86_64/docker-20.10.9.tgz
$ sudo tar xzvf docker-20.10.9.tgz --strip=1 -C /usr/local/bin docker/docker
```

然后确保 Docker Desktop 开启了 2375 端口：

![](./images/tcp-2375.png)

设置环境变量 `DOCKER_HOST`：

```
$ export DOCKER_HOST=tcp://localhost:2375
```

这样就可以在 WSL Ubuntu 中访问 Docker Desktop 了：

```
$ docker ps
```

如果想每次打开 WSL Ubuntu 时，环境变量都生效，可以将上面的 export 命令加到 `~/.profile` 文件中。

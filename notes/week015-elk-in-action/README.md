# WEEK015 - 实战 ELK 搭建日志系统

`ELK` 是 `Elasticsearch` + `Logstash` + `Kibana` 的简称。`Elasticsearch` 是一个基于 `Lucene` 的分布式全文搜索引擎，提供 RESTful API 进行数据读写；`Logstash` 是一个收集，处理和转发事件和日志消息的工具；而 `Kibana` 是 Elasticsearch 的开源数据可视化插件，为查看存储在 Elasticsearch 提供了友好的 Web 界面，并提供了条形图，线条和散点图，饼图和地图等分析工具。

总的来说，Elasticsearch 负责存储数据，Logstash 负责收集日志，并将日志格式化后写入 Elasticsearch，Kibana 提供可视化访问 Elasticsearch 数据的功能。

## 安装 Elasticsearch

使用下面的 Docker 命令启动一个单机版 Elasticsearch 实例：

```
> docker run --name es \
  -p 9200:9200 -p 9300:9300 \
  -e ELASTIC_PASSWORD=123456 \
  -d docker.elastic.co/elasticsearch/elasticsearch:8.3.2
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
$ docker cp es:/usr/share/elasticsearch/config/certs/http_ca.crt .
```

然后使用证书访问 Elasticsearch：

```
$ curl --cacert http_ca.crt -u elastic https://localhost:9200
```

## 安装 Logstash

使用下面的 Docker 命令启动一个最简单的 Logstash 实例：

```
$ docker run --name logstash \
  -e XPACK_MONITORING_ENABLED=false \
  -it --rm docker.elastic.co/logstash/logstash:8.3.2 \
  -e 'input { stdin { } } output { stdout {} }'
```

默认情况下，Logstash 会开启 X-Pack 监控，使用环境变量 `XPACK_MONITORING_ENABLED=false` 可以禁用它。另外，我们使用了 `-e 'input { stdin { } } output { stdout {} }'` 参数，表示让 Logstash 从标准输入 `stdin` 读取输入，并将结果输出到标注输出 `stdout`。

```
2022/07/17 05:34:19 Setting 'xpack.monitoring.enabled' from environment.
Using bundled JDK: /usr/share/logstash/jdk
OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was deprecated in version 9.0 and will likely be removed in a future release.
Sending Logstash logs to /usr/share/logstash/logs which is now configured via log4j2.properties
[2022-07-17T05:34:34,231][INFO ][logstash.runner          ] Log4j configuration path used is: /usr/share/logstash/config/log4j2.properties
[2022-07-17T05:34:34,257][INFO ][logstash.runner          ] Starting Logstash {"logstash.version"=>"8.3.2", "jruby.version"=>"jruby 9.2.20.1 (2.5.8) 2021-11-30 2a2962fbd1 OpenJDK 64-Bit Server VM 11.0.15+10 on 11.0.15+10 +indy +jit [linux-x86_64]"}
[2022-07-17T05:34:34,261][INFO ][logstash.runner          ] JVM bootstrap flags: [-Xms1g, -Xmx1g, -XX:+UseConcMarkSweepGC, -XX:CMSInitiatingOccupancyFraction=75, -XX:+UseCMSInitiatingOccupancyOnly, -Djava.awt.headless=true, -Dfile.encoding=UTF-8, -Djruby.compile.invokedynamic=true, -Djruby.jit.threshold=0, -XX:+HeapDumpOnOutOfMemoryError, -Djava.security.egd=file:/dev/urandom, -Dlog4j2.isThreadContextMapInheritable=true, -Dls.cgroup.cpuacct.path.override=/, -Dls.cgroup.cpu.path.override=/, -Djruby.regexp.interruptible=true, -Djdk.io.File.enableADS=true, --add-opens=java.base/java.security=ALL-UNNAMED, --add-opens=java.base/java.io=ALL-UNNAMED, --add-opens=java.base/java.nio.channels=ALL-UNNAMED, --add-opens=java.base/sun.nio.ch=ALL-UNNAMED, --add-opens=java.management/sun.management=ALL-UNNAMED]
[2022-07-17T05:34:34,317][INFO ][logstash.settings        ] Creating directory {:setting=>"path.queue", :path=>"/usr/share/logstash/data/queue"}
[2022-07-17T05:34:34,347][INFO ][logstash.settings        ] Creating directory {:setting=>"path.dead_letter_queue", :path=>"/usr/share/logstash/data/dead_letter_queue"}
[2022-07-17T05:34:34,917][WARN ][logstash.config.source.multilocal] Ignoring the 'pipelines.yml' file because modules or command line options are specified
[2022-07-17T05:34:34,942][INFO ][logstash.agent           ] No persistent UUID file found. Generating new UUID {:uuid=>"b1e18429-eb7f-4669-9271-0d75fed547c1", :path=>"/usr/share/logstash/data/uuid"}
[2022-07-17T05:34:36,221][INFO ][logstash.agent           ] Successfully started Logstash API endpoint {:port=>9600, :ssl_enabled=>false}
[2022-07-17T05:34:36,474][INFO ][org.reflections.Reflections] Reflections took 67 ms to scan 1 urls, producing 124 keys and 408 values
[2022-07-17T05:34:36,882][INFO ][logstash.javapipeline    ] Pipeline `main` is configured with `pipeline.ecs_compatibility: v8` setting. All plugins in this pipeline will default to `ecs_compatibility => v8` unless explicitly configured otherwise.
[2022-07-17T05:34:36,995][INFO ][logstash.javapipeline    ][main] Starting pipeline {:pipeline_id=>"main", "pipeline.workers"=>2, "pipeline.batch.size"=>125, "pipeline.batch.delay"=>50, "pipeline.max_inflight"=>250, "pipeline.sources"=>["config string"], :thread=>"#<Thread:0x44c28a87 run>"}
[2022-07-17T05:34:37,452][INFO ][logstash.javapipeline    ][main] Pipeline Java execution initialization time {"seconds"=>0.45}
[2022-07-17T05:34:37,521][INFO ][logstash.javapipeline    ][main] Pipeline started {"pipeline.id"=>"main"}
The stdin plugin is now waiting for input:
[2022-07-17T05:34:37,603][INFO ][logstash.agent           ] Pipelines running {:count=>1, :running_pipelines=>[:main], :non_running_pipelines=>[]}
```

等 Logstash 启动完毕，在控制台随便输入文本，然后回车，就可以看到 Logstash 将其转换为输出结果：

```
hello world
{
       "message" => "hello world",
      "@version" => "1",
    "@timestamp" => 2022-07-17T05:46:57.976318Z,
          "host" => {
        "hostname" => "6573ef0db968"
    },
         "event" => {
        "original" => "hello world"
    }
}
```

在上面的例子中，我们使用了 `-e` 参数来指定 Logstash 的 pipeline 配置，这个参数一般是用来调试 Logstash 的，真实场景下我们会将配置写在配置文件中，默认情况下，Logstash 的 pipeline 配置文件位于 `/usr/share/logstash/pipeline/logstash.conf`，内容如下：

```
input {
  beats {
    port => 5044
  }
}

output {
  stdout {
    codec => rubydebug
  }
}
```

其中 `input` 表示通过 5044 端口接收从 Filebeat 发送过来的数据，`output` 表示将结果输出到标准输出 `stdout`，并指定编码方式为 `rubydebug`，它会以格式化的 JSON 输出结果。接下来，我们要将我们的输出保存到 Elasticsearch，将配置文件修改如下：

```
input {
  stdin {
  }
}

output {
  stdout {
    codec => json_lines
  }
  elasticsearch {
    hosts => ["https://172.17.0.4:9200"]
    user => "elastic"
    password => "123456"
    ssl => true
    cacert => "/usr/share/logstash/http_ca.crt"
    index => "logstash-%{+YYYY.MM.dd}"
  }
}
```

然后重新启动 Logstash：

```
$ docker run --name logstash \
  -e XPACK_MONITORING_ENABLED=false \
  -v "/home/aneasystone/logstash/pipeline/logstash.conf":/usr/share/logstash/pipeline/logstash.conf \
  -v "/home/aneasystone/logstash/http_ca.crt":/usr/share/logstash/http_ca.crt \
  -it --rm docker.elastic.co/logstash/logstash:8.3.2
```

其中 `http_ca.crt` 就是上面我们从 es 容器中复制出来的证书文件。这里有一点要注意的是，`hosts` 必须是容器里的 IP 地址，这是因为这个证书带有 `SAN（Subject Alternative Name）`，只能通过 `localhost` 或 容器中的地址来访问 Elasticsearch，如果使用其他地址会报错：

```
[2022-07-17T07:23:48,228][WARN ][logstash.outputs.elasticsearch][main] Attempted to resurrect connection to dead ES instance, but got an error {:url=>"https://elastic:xxxxxx@192.168.1.35:9200/", :exception=>LogStash::Outputs::ElasticSearch::HttpClient::Pool::HostUnreachableError, :message=>"Elasticsearch Unreachable: [https://192.168.1.35:9200/][Manticore::UnknownException] Certificate for <192.168.1.35> doesn't match any of the subject alternative names: [localhost, 876647d76274, 172.17.0.4, 127.0.0.1]"}
```

启动完成后，我们在控制台中随便输入文本，文本内容会自动输出到 Elasticsearch：

```
hello
{"@timestamp":"2022-07-17T07:40:23.556377Z","message":"hello","@version":"1","host":{"hostname":"988f1263897d"},"event":{"original":"hello"}}
world
{"@timestamp":"2022-07-17T07:50:00.327637Z","message":"world","@version":"1","host":{"hostname":"988f1263897d"},"event":{"original":"world"}}
hello world
{"@timestamp":"2022-07-17T07:50:04.285282Z","message":"hello world","@version":"1","host":{"hostname":"988f1263897d"},"event":{"original":"hello world"}}
```

我们通过 HTTP 接口查看 Elasticsearch 的索引：

```
$ curl -k -u elastic:123456 https://localhost:9200/_cat/indices
yellow open logstash-2022.07.17 9Anz9bHjSay-GEnANNluBA 1 1 3 0 18.3kb 18.3kb
```

可以看到自动为我们创建了一个 `logstash-2022.07.17` 索引，我们可以通过 HTTP 接口检索：

```
$ curl -s -k -u elastic:123456 https://localhost:9200/_search?q=hello | jq
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.9808291,
    "hits": [
      {
        "_index": "logstash-2022.07.17",
        "_id": "rGMZC4IBQ5UjjhVY6pAZ",
        "_score": 0.9808291,
        "_source": {
          "@timestamp": "2022-07-17T07:40:23.556377Z",
          "message": "hello",
          "@version": "1",
          "host": {
            "hostname": "988f1263897d"
          },
          "event": {
            "original": "hello"
          }
        }
      },
      {
        "_index": "logstash-2022.07.17",
        "_id": "rmMiC4IBQ5UjjhVYxZBt",
        "_score": 0.39019167,
        "_source": {
          "@timestamp": "2022-07-17T07:50:04.285282Z",
          "message": "hello world",
          "@version": "1",
          "host": {
            "hostname": "988f1263897d"
          },
          "event": {
            "original": "hello world"
          }
        }
      }
    ]
  }
}
```

## 安装 Kibana

使用下面的 Docker 命令启动 Kibana 服务：

```
$ docker run --name kibana \
  -p 5601:5601 \
  docker.elastic.co/kibana/kibana:8.3.2
```

等待 Kibana 启动完成：

```
[2022-07-17T22:57:20.266+00:00][INFO ][plugins-service] Plugin "cloudSecurityPosture" is disabled.
[2022-07-17T22:57:20.403+00:00][INFO ][http.server.Preboot] http server running at http://0.0.0.0:5601
[2022-07-17T22:57:20.446+00:00][INFO ][plugins-system.preboot] Setting up [1] plugins: [interactiveSetup]
[2022-07-17T22:57:20.448+00:00][INFO ][preboot] "interactiveSetup" plugin is holding setup: Validating Elasticsearch connection configuration…
[2022-07-17T22:57:20.484+00:00][INFO ][root] Holding setup until preboot stage is completed.


i Kibana has not been configured.

Go to http://0.0.0.0:5601/?code=395267 to get started.
```

启动完成后，在浏览器输入 `http://localhost:5601/?code=395267` 访问 Kibana，第一次访问 Kibana 时需要配置 Elasticsearch 的 `Enrollment token`：

![](./images/kibana-enrollment-token.png)

这个 `Enrollment token` 的值可以从 Elasticsearch 的启动日志中找到，也可以使用下面的命令生成：

```
$ docker exec -it es /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
```

注意访问 Kibana 的链接中带有一个 `code` 参数，这个参数为第一次访问 Kibana 时的验证码，如果不带参数访问，Kibana 会要求你填写：

![](./images/kibana-verification.png)

这个验证码可以从 Kibana 的启动日志中找到，也可以使用下面的命令得到：

```
$ docker exec -it kibana /usr/share/kibana/bin/kibana-verification-code
Your verification code is:  395 267
```

填写验证码之后，Kibana 会自动完成 Elasticsearch 的配置，然后进入登录页面：

![](./images/kibana-login.png)

我们输入用户名和密码 `elastic/123456` 即可进入 Kibana 首页：

![](./images/kibana-home.png)

打开 Discover 页面 `http://localhost:5601/app/discover#/`：

![](./images/kibana-discover.png)

第一次访问需要创建一个数据视图（`data view`），数据视图的名称必须要和索引相匹配，我们这里填入 `logstash-*`：

![](./images/kibana-create-data-view.png)

然后就可以输入关键字对 Elasticsearch 进行检索了：

![](./images/kibana-search.png)

这里的检索语法被称为 `KQL（Kibana Query Language）`，具体内容可 [参考官方文档](https://www.elastic.co/guide/en/kibana/8.3/kuery-query.html)。

## 配置 Logstash 采集日志文件

在前面的例子中，我们配置了 Logstash 从标准输入获取数据，并转发到标准输出或 Elasticsearch 中。一个完整的 Logstash 配置文件包含三个部分：`input`、`filter` 和 `output`，并且每个部分都是插件：

* [Input Plugins](https://www.elastic.co/guide/en/logstash/current/input-plugins.html)
* [Output Plugins](https://www.elastic.co/guide/en/logstash/current/output-plugins.html)
* [Filter Plugins](https://www.elastic.co/guide/en/logstash/current/filter-plugins.html)

这一节我们将改用 `file` 作为输入，从文件系统中采集日志文件内容，并转发到 Elasticsearch。首先修改 `logstash.conf` 中的 `input` 配置：

```
input {
  file {
    type => "log"
    path => ["/app/logs/*.log"]
  }
}
```

然后重新启动 Logstash 容器，并将日志目录挂载到 `/app/logs`：

```
$ docker run --name logstash \
  -e XPACK_MONITORING_ENABLED=false \
  -v "/home/aneasystone/logstash/pipeline/logstash-file.conf":/usr/share/logstash/pipeline/logstash.conf \
  -v "/home/aneasystone/logstash/http_ca.crt":/usr/share/logstash/http_ca.crt \
  -v "/home/aneasystone/logs":/app/logs \
  -it --rm docker.elastic.co/logstash/logstash:8.3.2
```

我们在 logs 目录下写入一点日志：

```
$ cd ~/logs
$ echo 'hello' > hello.log
$ echo 'hello world' >> hello.log
```

稍等片刻，就可以看到 Logstash 从日志文件中读取数据了：

```
{"event":{"original":"hello"},"@timestamp":"2022-07-18T23:48:27.709472Z","message":"hello","type":"log","@version":"1","host":{"name":"48bdb8490d22"},"log":{"file":{"path":"/app/logs/hello.log"}}}
{"event":{"original":"hello world"},"@timestamp":"2022-07-18T23:52:07.345525Z","message":"hello world","type":"log","@version":"1","host":{"name":"48bdb8490d22"},"log":{"file":{"path":"/app/logs/hello.log"}}}
```

## 使用 Filebeat 采集日志文件

尽管 Logstash 提供了 `file` 插件用于采集日志文件，但是一般在生产环境我们很少这样去用，因为 Logstash 相对来说还是太重了，它依赖于 JVM，当配置多个 `pipeline` 以及 `filter` 时，Logstash 会非常占内存。而采集日志的工作需要在每一台服务器上运行，我们希望采集日志消耗的资源越少越好。

于是 [Filebeat](https://www.elastic.co/cn/beats/filebeat) 就出现了。它采用 Go 编写，非常轻量，只专注于采集日志，并将日志转发给 Logstash 甚至直接转发给 Elasticsearch。如下图所示：

![](./images/efk.jpg)

那么有人可能会问，既然可以直接从 Filebeat 将日志转发给 Elasticsearch，那么 Logstash 是不是就没用了？其实这取决于你的使用场景，如果你只是想将原始的日志收集到 Elasticsearch 而不做任何处理，确实可以不用 Logstash，但是如果你要对日志进行过滤和转换处理，Logstash 就很有用了。不过 Filebeat 也提供了 `processors` 功能，可以对日志做一些简单的转换处理。

下面我们就来实践下这种场景。首先修改 Logstash 配置文件中的 `input`，让 Logstash 可以接收 Filebeat 的请求：

```
input {
  beats {
    port => 5044
  }
}
```

然后重新启动 Logstash 容器，注意将 5044 端口暴露出来：

```
$ docker run --name logstash \
  -e XPACK_MONITORING_ENABLED=false \
  -v "/home/aneasystone/logstash/pipeline/logstash-beat.conf":/usr/share/logstash/pipeline/logstash.conf \
  -v "/home/aneasystone/logstash/http_ca.crt":/usr/share/logstash/http_ca.crt \
  -p 5044:5044 \
  -it --rm docker.elastic.co/logstash/logstash:8.3.2
```

然后新建一个 Filebeat 的配置文件 `filebeat.yml`，内容如下：

```
filebeat.inputs:
- type: log
  paths:
    - /app/logs/*.log

output.logstash:
  hosts: ["192.168.1.35:5044"]
```

然后使用 Docker 启动 Filebeat 容器：

```
$ docker run --name filebeat \
  -v "/home/aneasystone/filebeat/filebeat.yml":/usr/share/filebeat/filebeat.yml \
  -v "/home/aneasystone/logs":/app/logs \
  -it --rm docker.elastic.co/beats/filebeat:8.3.2
```

这时只要我们向 logs 目录写入一点日志：

```
$ echo "This is a filebeat log" >> filebeat.log
```

Logstash 就可以收到 Filebeat 采集过来的日志了：

```
{"message":"This is a filebeat log","host":{"name":"8a7849b5c331"},"log":{"offset":0,"file":{"path":"/app/logs/filebeat.log"}},"event":{"original":"This is a filebeat log"},"input":{"type":"log"},"ecs":{"version":"8.0.0"},"@version":"1","agent":{"id":"3bd9b289-599f-4899-945a-94692bdaa690","name":"8a7849b5c331","ephemeral_id":"268a3170-0feb-4a86-ad96-7cce6a9643ec","version":"8.3.2","type":"filebeat"},"tags":["beats_input_codec_plain_applied"],"@timestamp":"2022-07-19T23:41:22.255Z"}
```

Filebeat 除了可以将日志推送给 Logstash，还支持很多其他的 [`output` 配置](https://www.elastic.co/guide/en/beats/filebeat/current/configuring-output.html)，比如 Elasticsearch、Kafka、Redis 或者写入文件等等。下面是将日志推送给 Elasticsearch 的例子：

```
output.elasticsearch:
  hosts: ["https://localhost:9200"]
  username: "username"
  password: "password" 
  ssl:
    enabled: true
    ca_trusted_fingerprint: "xxx"
```

## 日志格式转换

在实际的使用场景中，我们往往要对各个地方采集来的日志做一些格式转换，而不是直接将原始的日志写入 Elasticsearch 中，因为结构化的日志更方便检索和统计。比如在采集 Nginx 的 access log 时，原始的日志内容如下：

```
172.17.0.1 - - [20/Jul/2022:23:34:23 +0000] "GET / HTTP/1.1" 200 615 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" "-"
172.17.0.1 - - [20/Jul/2022:23:34:23 +0000] "GET /favicon.ico HTTP/1.1" 404 555 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" "-"
```

我们查看 Nginx 配置文件中的 `log_format` 可以知道，其实 access log 中的每一行都是由 `remote_addr`、`remote_user`、`time_local`、`request` 等字段构成的：

```
http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;
}
```

下面我们就通过 [Logstash 的 `filter` 插件](https://www.elastic.co/guide/en/logstash/current/filter-plugins.html) 或 [Filebeat 的 `processors` 功能](https://www.elastic.co/guide/en/beats/filebeat/current/filtering-and-enhancing-data.html) 来将这个日志转换为结构化的字段。

### Logstash 的 `filter` 插件

Logstash 自带大量的 filter 插件用于对日志做各种各样的处理，如果要从任意文本中抽取出结构化的字段，其中最常用的 filter 插件就是 [Dissect](https://www.elastic.co/guide/en/logstash/current/plugins-filters-dissect.html) 和 [Grok](https://www.elastic.co/guide/en/logstash/current/plugins-filters-grok.html)，其中 Dissect 使用固定的分割符来提取字段，没有使用正则表达式，所以处理速度非常快，不过它只对固定格式的日志有效，对于不固定的文本格式就无能为力了。而 Grok 要强大的多，它使用正则表达式，几乎可以处理任意文本。

这里我们将使用 Grok 来处理 Nginx 的 access log。

Grok 通过一堆的模式来匹配你的日志，一个 Grok 模式的语法如下：

```
%{SYNTAX:SEMANTIC}
```

其中，`SYNTAX` 为模式名称，比如 `NUMBER` 表示数字，`IP` 表示 IP 地址，等等，Grok 内置了很多可以直接使用的模式，[这里有一份完整列表](https://github.com/logstash-plugins/logstash-patterns-core/blob/main/patterns/legacy/grok-patterns)。`SEMANTIC` 为匹配模式的文本创建一个唯一标识。比如我们有下面这样一行日志：

```
55.3.244.1 GET /index.html 15824 0.043
```

可以使用下面的 Grok 模式来匹配：

```
%{IP:client} %{WORD:method} %{URIPATHPARAM:request} %{NUMBER:bytes} %{NUMBER:duration}
```

Logstash 配置类似如下：

```
filter {
  grok {
    match => { "message" => "%{IP:client} %{WORD:method} %{URIPATHPARAM:request} %{NUMBER:bytes} %{NUMBER:duration}" }
  }
}
```

其中 `match => { "message" => "..." }` 表示处理的是 `message` 字段。处理得到的结构化结果如下：

```
{
  "client": "55.3.244.1",
  "method": "GET",
  "request": "/index.html",
  "bytes": "15824",
  "duration": "0.043"
}
```

你可以使用 [Grok Debugger](https://grokdebug.herokuapp.com/) 或 [Grok Constructor](http://grokconstructor.appspot.com/) 对 Grok 模式在线进行调试。

#### 自定义 Grok 模式

另外，Logstash 内置的 Grok 模式可能不能满足你的需要，这时，你也可以自定义 Grok 模式。Grok 是基于正则表达式库 [Oniguruma](https://github.com/kkos/oniguruma) 实现的，所以我们可以使用 [Oniguruma 的语法](https://github.com/kkos/oniguruma/blob/master/doc/RE) 来创建自定义的 Grok 模式。

自定义 Grok 模式的方式有以下三种：

* 第一种是直接使用正则来定义 Grok 模式

```
filter {
  grok {
    match => { "message" => "(?<queue_id>[0-9A-F]{10,11})" }
  }
}
```

* 第二种是将 Grok 模式定义在模式文件中，比如创建一个名为 `patterns` 的目录，然后在目录下新建一个文件（文件名任意），文件内容如下：

```
# commnets
POSTFIX_QUEUEID [0-9A-F]{10,11}
```

然后，在 Logstash 配置文件中，通过配置参数 `patterns_dir` 指定刚刚创建的那个模式目录，这样就可以和内置 Grok 模式一样的使用我们自定义的模式了：

```
filter {
  grok {
    patterns_dir => ["./patterns"]
    match => { "message" => "%{POSTFIX_QUEUEID:queue_id}" }
  }
}
```

* 第三种是将 Grok 模式定义在 `pattern_definitions` 参数中，这种定义方式非常方便，不过这个模式只能在当前 grok 配置块内生效

```
filter {
  grok {
    pattern_definitions => {
      "POSTFIX_QUEUEID" => "[0-9A-F]{10,11}"
    }
    match => { "message" => "%{POSTFIX_QUEUEID:queue_id}" }
  }
}
```

#### 处理 Nginx access log

回到上面一开始的问题，我们希望将 Nginx access log 转换为结构化的格式。学习了 Grok 模式的知识之后，我们完全可以自己写出匹配 Nginx access log 的 Grok 模式，不过这样做有点繁琐。实际上，Logstash 已经内置了很多常用的系统日志格式，比如：Apache httpd、Redis、Mongo、Java、Maven 等，[参见这里](https://github.com/logstash-plugins/logstash-patterns-core/tree/main/patterns/legacy)。

虽然没有专门的 Nginx 格式，但是 Nginx 默认的 access log 是符合 Apache httpd 日志规范的，只要你在 Nginx 配置文件中没有随便修改 `log_format` 配置，我们都可以直接使用 Apache httpd 的 Grok 模式来匹配 Nginx 的日志。

[Apache httpd 的 Grok 模式](https://github.com/logstash-plugins/logstash-patterns-core/blob/main/patterns/legacy/httpd) 定义如下：

```
# Log formats
HTTPD_COMMONLOG %{IPORHOST:clientip} %{HTTPDUSER:ident} %{HTTPDUSER:auth} \[%{HTTPDATE:timestamp}\] "(?:%{WORD:verb} %{NOTSPACE:request}(?: HTTP/%{NUMBER:httpversion})?|%{DATA:rawrequest})" (?:-|%{NUMBER:response}) (?:-|%{NUMBER:bytes})
HTTPD_COMBINEDLOG %{HTTPD_COMMONLOG} %{QS:referrer} %{QS:agent}

# Deprecated
COMMONAPACHELOG %{HTTPD_COMMONLOG}
COMBINEDAPACHELOG %{HTTPD_COMBINEDLOG}
```

其中 `HTTPD_COMBINEDLOG` 就是 Apache httpd 的日志格式，在老的版本中通常使用 `COMBINEDAPACHELOG`，[Grok Debugger](https://grokdebug.herokuapp.com/) 就还是使用这个老的格式。

对比发现，Nginx 的日志比 Apache httpd 的日志就多了一个 `$http_x_forwarded_for` 字段，所以我们可以通过下面的配置来处理 Nginx access log：

```
filter {
  grok {
    match => { "message" => "%{HTTPD_COMBINEDLOG} %{QS:x_forwarded_for}" }
  }
}
```

### Filebeat 的 `processors` 功能

Filebeat 提供了 [很多的 `processors`](https://www.elastic.co/guide/en/beats/filebeat/current/filtering-and-enhancing-data.html) 可以对日志进行一些简单的处理，比如 `drop_event` 用于过滤日志，`convert` 用于转换数据类型，`rename` 用于重命名字段等。但是 Filebeat 的定位是轻量级日志采集工具，最大的理念在于 **轻量**，所以只能做些简单的处理，上面所说的 Logstash 的 Grok 就不支持。

如果你的日志是固定格式的，可以使用 [`dissect` 处理器](https://www.elastic.co/guide/en/beats/filebeat/current/dissect.html) 来进行处理，下面是一个 `dissect` 配置的例子：

```
processors:
  - dissect:
      tokenizer: '"%{pid|integer} - %{name} - %{status}"'
      field: "message"
      target_prefix: "service"
```

其中 `tokenizer` 用于定义日志的格式，上面的配置表示从日志中提取 `pid`、`name` 和 `status` 三个字段，`target_prefix` 表示将这三个字段放在 `service` 下面，默认情况是放在 `dissect` 下面。

这个处理器可以处理下面这种格式的日志：

```
"321 - App01 - WebServer is starting"
"321 - App01 - WebServer is up and running"
"321 - App01 - WebServer is scaling 2 pods"
"789 - App02 - Database is will be restarted in 5 minutes"
"789 - App02 - Database is up and running"
"789 - App02 - Database is refreshing tables"
```

处理之后的日志格式如下：

```
{
  "@timestamp": "2022-07-23T01:01:54.310Z",
  "@metadata": {
    "beat": "filebeat",
    "type": "_doc",
    "version": "8.3.2"
  },
  "log": {
    "offset": 0,
    "file": {
      "path": ""
    }
  },
  "message": "\"789 - App02 - Database is will be restarted in 5 minutes\"",
  "input": {
    "type": "stdin"
  },
  "host": {
    "name": "04bd0b21796b"
  },
  "agent": {
    "name": "04bd0b21796b",
    "type": "filebeat",
    "version": "8.3.2",
    "ephemeral_id": "64187690-291c-4647-b935-93c249e85d29",
    "id": "43a89e87-0d74-4053-8301-0e6e73a00e77"
  },
  "ecs": {
    "version": "8.0.0"
  },
  "service": {
    "name": "App02",
    "status": "Database is will be restarted in 5 minutes",
    "pid": 789
  }
}
```

#### 使用 `script` 处理器

虽然 Filebeat 不支持 Grok 处理器，但是它也提供了一种动态扩展的解决方案，那就是 [`script` 处理器](https://www.elastic.co/guide/en/beats/filebeat/current/processor-script.html)。在 `script` 处理器里，我们需要定义这样一个 `process` 方法：

```
function process(event) {
    // Put your codes here
}
```

Filebeat 在处理日志时，会将每一行日志都转换为一个 `event` 对象，然后调用这个 `process` 方法进行处理，`event` 对象提供了下面这些 API 用于处理日志：

* Get(string)
* Put(string, value)
* Rename(string, string)
* Delete(string)
* Cancel()
* Tag(string)
* AppendTo(string, string)

具体的使用方法可以参考官方文档。下面我们写一个简单的 `script` 处理器来处理上面例子中的日志格式：

```
processors:
  - script:
      lang: javascript
      source: >
        function process(event) {
            var message = event.Get('message');
            message = message.substring(1, message.length-1);
            var s = message.split(' - ');
            event.Put('service.pid', s[0]);
            event.Put('service.name', s[1]);
            event.Put('service.status', s[2]);
        }
```

处理之后的日志格式和上面使用 `dissect` 处理器是一样的。

我们知道 Grok 是基于正则表达式来处理日志的，当然也可以在 Javascript 脚本中使用正则表达式：

```
processors:
  - script:
      lang: javascript
      source: >
        function process(event) {
            var message = event.Get('message');
            var match = message.match(/"(.+) - (.+) - (.+)"/);
            event.Put('service.pid', match[1]);
            event.Put('service.name', match[2]);
            event.Put('service.status', match[3]);
        }
```

不过要注意的是，Filebeat 使用 [dop251/goja](https://github.com/dop251/goja) 这个库来解析 Javascript 脚本，目前只支持 ECMA 5.1 的语法规范（也就是 ECMAScript 2009），如果使用了最新的 Javascript 语法，可能会导致 Filebeat 异常退出。

比如我们使用正则表达式的命名捕获分组（`named capturing groups`）来优化上面的代码：

```
processors:
  - script:
      lang: javascript
      source: >
        function process(event) {
            var message = event.Get('message');
            var match = message.match(/"(?<pid>.+) - (?<name>.+) - (?<status>.+)"/);
            event.Put('service', match.groups);
        }
```

Filebeat 直接启动就报错了：

```
Exiting: error initializing processors: SyntaxError: Invalid regular expression (re2): "(?<pid>[^\r\n]+) - (?<name>[^\r\n]+) - (?<status>[^\r\n]+)" (error parsing regexp: invalid or unsupported Perl syntax: `(?<`) at 3:31
```

这是因为命名捕获分组这个特性，是在 ECMA 9（也就是 [ECMAScript 2018](https://262.ecma-international.org/9.0/)）中才引入的，所以在 `script` 处理器中编写 Javascript 代码时需要特别注意语法的版本问题。

#### 使用 Filebeat 的 `Modules` 功能

https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-modules.html

#### 使用 Elasticsearch 的 `Ingest pipelines` 功能

https://www.elastic.co/guide/en/beats/filebeat/current/configuring-ingest-node.html

https://www.elastic.co/guide/en/elasticsearch/reference/master/ingest.html

## 使用 Logback 对接 Logstash

https://github.com/logfellow/logstash-logback-encoder

## 参考

1. [Install Elasticsearch with Docker](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)
1. [Running Logstash on Docker](https://www.elastic.co/guide/en/logstash/current/docker.html)
1. [Install Kibana with Docker](https://www.elastic.co/guide/en/kibana/current/docker.html)
1. [ELK6.0部署：Elasticsearch+Logstash+Kibana搭建分布式日志平台](https://ken.io/note/elk-deploy-guide)
1. [Filebeat vs. Logstash: The Evolution of a Log Shipper](https://logz.io/blog/filebeat-vs-logstash/)
1. https://blog.csdn.net/mawming/article/details/78344939
1. https://www.feiyiblog.com/2020/03/06/ELK%E6%97%A5%E5%BF%97%E5%88%86%E6%9E%90%E7%B3%BB%E7%BB%9F/
1. [如何在 Filebeat 端进行日志处理](https://mritd.com/2020/08/19/how-to-modify-filebeat-source-code-to-processing-logs/)

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

另外有一点要注意的是，使用这种方式在 WSL Ubuntu 下运行 `docker -v` 挂载文件时，需要使用真实的 Windows 下的路径，而不是 Linux 下的路径。譬如下面的命令：

```
$ docker run --name logstash \
  -e XPACK_MONITORING_ENABLED=false \
  -v "/home/aneasystone/logstash/pipeline/logstash.conf":/usr/share/logstash/pipeline/logstash.conf \
  -v "/home/aneasystone/logstash/http_ca.crt":/usr/share/logstash/http_ca.crt \
  -it --rm docker.elastic.co/logstash/logstash:8.3.2
```

要改成这样：

```
$ docker run --name logstash \
  -e XPACK_MONITORING_ENABLED=false \
  -v "C:/Users/aneasystone/AppData/Local/Packages/CanonicalGroupLimited.Ubuntu18.04LTS_79rhkp1fndgsc/LocalState/rootfs/home/aneasystone/logstash/pipeline/logstash.conf":/usr/share/logstash/pipeline/logstash.conf \
  -v "C:/Users/aneasystone/AppData/Local/Packages/CanonicalGroupLimited.Ubuntu18.04LTS_79rhkp1fndgsc/LocalState/rootfs/home/aneasystone/logstash/http_ca.crt":/usr/share/logstash/http_ca.crt \
  -it --rm docker.elastic.co/logstash/logstash:8.3.2
```

其中，`C:/Users/aneasystone/AppData/Local/Packages/CanonicalGroupLimited.Ubuntu18.04LTS_79rhkp1fndgsc/LocalState/rootfs` 是 WSL Ubuntu 在 Windows 下的根路径。

### Elastic Beats

除了 Filebeat，Elastic 还提供了其他一些轻量型的数据采集器：

* [Filebeat](https://www.elastic.co/cn/beats/filebeat) - 日志文件
* [Metricbeat](https://www.elastic.co/beats/metricbeat) - 指标
* [Packetbeat](https://www.elastic.co/cn/beats/packetbeat) - 网络数据
* [Winlogbeat](https://www.elastic.co/cn/beats/winlogbeat) - Windows 事件日志
* [Auditbeat](https://www.elastic.co/cn/beats/auditbeat) - 审计日志
* [Heartbeat](https://www.elastic.co/cn/beats/heartbeat) - 运行时间监控
* [Functionbeat](https://www.elastic.co/cn/beats/functionbeat) - 无需服务器的采集器

### 其他学习资料

1. [Logstash 最佳实践](https://doc.yonyoucloud.com/doc/logstash-best-practice-cn/index.html)
1. [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
1. [Logstash Guide](https://www.elastic.co/guide/en/logstash/current/index.html)
1. [Filebeat Guide](https://www.elastic.co/guide/en/beats/filebeat/current/index.html)
1. [Kibana Guide](https://www.elastic.co/guide/en/kibana/current/index.html)
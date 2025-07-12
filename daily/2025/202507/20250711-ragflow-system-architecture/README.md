# 学习 RAGFlow 的系统架构

昨天，我们学习了 RAGFlow 的安装配置和基本使用，通过创建一个知识库并上传文档，完整地体验了 RAGFlow 从数据处理到智能问答的基本工作流程。作为一个 RAG 系统，这套流程也是 RAGFlow 的核心流程，下面是 RAGFlow 的系统架构图：

![](./images/ragflow-architecture.png)

上面的架构图中省略了中间件部分，包括 ES、MySQL、Redis 和 Minio 等，仅展示了 RAGFlow 的两个核心服务：**API 服务器（API Server）** 和 **任务执行器（Task Executor）**，其中 API 服务器负责提供外部接口，包括知识库管理、文件管理、搜索、聊天等功能，而任务执行器则负责文件的解析和切片任务，正所谓 **Quality in, quality out**，它的深度文档理解和智能文本切片是 RAGFlow 的关键特性。

今天我们就从物理部署的角度来看看 RAGFlow 的这两个服务。

## 深入 `entrypoint.sh` 脚本

我们昨天学习了构建 RAGFlow 镜像的过程，感兴趣的同学可以研究下 `Dockerfile` 文件，它通过 [多阶段构建（Multi-stage builds）](https://docs.docker.com/build/building/multi-stage/) 技巧，将构建过程分成基础（base）、构建（builder）、生产（production）三个阶段，大概的文件结构如下：

```dockerfile
# --------
# 基础阶段
# --------
FROM ubuntu:22.04 AS base
USER root
WORKDIR /ragflow

# 从资源镜像拷贝模型资源
# 安装所需的系统类库
# 安装 Python Git Nginx 等软件 ...
# 安装 JDK、Node.js 等 ...

# --------
# 构建阶段
# --------
FROM base AS builder

# 安装 Python 依赖...
# 编译 Web 页面 ...

# --------
# 生产阶段
# --------
FROM base AS production

# 拷贝 Python 包
# 拷贝 Web 页面 ...

ENTRYPOINT ["./entrypoint.sh"]
```

从最后的生产阶段可以看出，RAGFlow 镜像的入口文件为 `/ragflow/entrypoint.sh`，它的用法如下：

```sh
function usage() {
  echo "Usage: $0 [--disable-webserver] [--disable-taskexecutor] [--consumer-no-beg=<num>] [--consumer-no-end=<num>] [--workers=<num>] [--host-id=<string>]"
  echo
  echo "  --disable-webserver             Disables the web server (nginx + ragflow_server)."
  echo "  --disable-taskexecutor          Disables task executor workers."
  echo "  --enable-mcpserver              Enables the MCP server."
  echo "  --consumer-no-beg=<num>         Start range for consumers (if using range-based)."
  echo "  --consumer-no-end=<num>         End range for consumers (if using range-based)."
  echo "  --workers=<num>                 Number of task executors to run (if range is not used)."
  echo "  --host-id=<string>              Unique ID for the host (defaults to \`hostname\`)."
  echo
  echo "Examples:"
  echo "  $0 --disable-taskexecutor"
  echo "  $0 --disable-webserver --consumer-no-beg=0 --consumer-no-end=5"
  echo "  $0 --disable-webserver --workers=2 --host-id=myhost123"
  echo "  $0 --enable-mcpserver"
  exit 1
}
```

可以看到这个镜像可以以多种方式启动：

* `--disable-taskexecutor` 禁用任务执行器，仅启动 API 服务器
* `--disable-webserver` 禁用 API 服务器，仅启动任务执行器
* `--enable-mcpserver` 启动 MCP 服务器

RAGFlow 默认会在一个容器中同时启动 API 服务器和任务执行器，便于开发和测试，但是在生产环境中我们可以灵活地根据需要选择启动方式，将两者分开部署。

## 仅启动 API 服务器

我们可以修改 `docker/docker-compose.yml` 文件中的启动参数来做到这一点：

```yaml
services:
  ragflow:
    image: ${RAGFLOW_IMAGE}
    command:
      - --disable-taskexecutor
    container_name: ragflow-server
    # 其他配置 ...
```

在 `entrypoint.sh` 文件中，启动 API 服务器的代码如下：

```sh
if [[ "${ENABLE_WEBSERVER}" -eq 1 ]]; then
  echo "Starting nginx..."
  /usr/sbin/nginx

  echo "Starting ragflow_server..."
  while true; do
    "$PY" api/ragflow_server.py
  done &
fi
```

首先启动 Nginx，然后执行 `ragflow_server.py` 脚本，它是一个基于 Flask 开发的 Web 服务，默认监听 9380 端口。这里的  `while true; do ... done &` 的写法挺有意思，`while true` 表示无限循环，`&` 表示将脚本放入后台执行，这样做可以确保服务进程在崩溃或异常退出后能够自动重启，通过这种纯 Shell 的方式实现自动恢复机制，不依赖任何第三方进程管理器（如 `systemd`、`supervisor`）。

Nginx 用于托管 Web 前端页面以及透传 API 服务器的 HTTP 请求，它的配置位于 `ragflow.conf` 文件中，内容如下：

```
server {
  listen 80;
  server_name _;
  root /ragflow/web/dist;

  gzip on;

  location ~ ^/(v1|api) {
    proxy_pass http://ragflow:9380;
    include proxy.conf;
  }

  location / {
    index index.html;
    try_files $uri $uri/ /index.html;
  }

  # Cache-Control: max-age~@~AExpires
  location ~ ^/static/(css|js|media)/ {
    expires 10y;
    access_log off;
  }
}
```

如果要对外提供 HTTPS 服务，可以将 `docker/docker-compose.yml` 文件中的 `ragflow.conf` 替换成 `ragflow.https.conf`，并将证书文件挂到容器中：

```yaml
services:
  ragflow:
    volumes:
      # 证书文件
      - /path/to/fullchain.pem:/etc/nginx/ssl/fullchain.pem:ro
      - /path/to/privkey.pem:/etc/nginx/ssl/privkey.pem:ro
      # 使用 ragflow.https.conf 替换 ragflow.conf
      - ./nginx/ragflow.https.conf:/etc/nginx/conf.d/ragflow.conf
      # 其他配置 ...
```

同时编辑 `nginx/ragflow.https.conf` 文件，将 `my_ragflow_domain.com` 替换成你真实的域名。然后重启服务即可：

```bash
$ docker-compose down
$ docker-compose up -d
```

## 仅启动任务执行器

当处理的文档数量很多时，将任务执行器单独部署多个实例可以提高文档解析的速度。我们可以修改 `docker/docker-compose.yml` 文件，将 `ragflow` 配置复制一份出来，仅启动任务执行器：

```yaml
services:
  ragflow_task_executor:
    image: ${RAGFLOW_IMAGE}
    command:
      - --disable-webserver
      - --workers=5
    container_name: ragflow-task-executor
    # 其他配置 ...
```

我们可以通过 `--workers` 参数来指定启动的 worker 数量。启动任务执行器的代码如下：

```sh
if [[ "${ENABLE_TASKEXECUTOR}" -eq 1 ]]; then
    echo "Starting ${WORKERS} task executor(s) on host '${HOST_ID}'..."
    for (( i=0; i<WORKERS; i++ ))
    do
        task_exe "${i}" "${HOST_ID}" &
    done
fi
```

每个 worker 都会启动一个独立的进程，其中 `task_exe()` 函数定义如下：

```sh
function task_exe() {
    local consumer_id="$1"
    local host_id="$2"

    JEMALLOC_PATH="$(pkg-config --variable=libdir jemalloc)/libjemalloc.so"
    while true; do
        LD_PRELOAD="$JEMALLOC_PATH" \
        "$PY" rag/svr/task_executor.py "${host_id}_${consumer_id}"
    done
}
```

这里也用了 `while true` 的技巧，防止 worker 进程异常退出，每个 worker 进程执行 `task_executor.py` 脚本，并将 `${host_id}_${consumer_id}` 作为参数传入。任务执行器是一个基于 [Trio](https://github.com/python-trio/trio) 异步库开发的命令行程序，它通过监听 Redis 消息队列，对用户上传的文件进行解析处理。这里的 `${host_id}` 是当前的主机名，`${consumer_id}` 是指 worker 的序号，拼接起来用于区分不同的消费者。

## 启动 MCP 服务器

RAGFlow 还支持 MCP 服务器，开启方法很简单，只需将 `docker/docker-compose.yml` 文件中 `services.ragflow.command` 部分的注释去掉即可：

```yaml
services:
  ragflow:
    image: ${RAGFLOW_IMAGE}
    command:
      - --enable-mcpserver
      - --mcp-host=0.0.0.0
      - --mcp-port=9382
      - --mcp-base-url=http://127.0.0.1:9380
      - --mcp-script-path=/ragflow/mcp/server/server.py
      - --mcp-mode=self-host
      - --mcp-host-api-key=ragflow-xxxxxxx
```

关于 RAGFlow MCP 服务器的使用，我们今天暂且跳过，后面单开一篇介绍。

## 小结

通过今天的学习，我们了解了 RAGFlow 的系统架构，以及如何通过 `entrypoint.sh` 脚本启动不同的服务。接下来，我们将继续剖析 RAGFlow 的源码，探索 API 服务器和任务执行器的实现原理。

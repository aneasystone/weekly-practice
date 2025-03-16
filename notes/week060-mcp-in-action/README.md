# WEEK060 - 实战 Model Context Protocol

[2024 年 11 月 25 日](https://www.anthropic.com/news/model-context-protocol)，Anthropic，就是 Claude 背后的那家公司，推出了一个名为 MCP 的开放协议，它的全称为 [Model Context Protocol](https://modelcontextprotocol.io/introduction)（模型上下文协议），用于标准化大模型与各类外部工具和数据源之间的交互。

这个协议自推出以来，在 AI 圈一直不温不火，很多人认为 MCP 只是套壳的 API，并没有什么特别之处。但是近期，随着 [Manus](https://manus.im) 的爆火，MCP 的概念在社区中又逐渐流行开来，使用 MCP 打造一款本地的 Manus 成了大家乐此不疲的话题。

## MCP 架构

为了搞清楚什么是 MCP，让我们先来了解下它的基本架构。下面这张图非常形象地展示了 MCP 的基本架构（[图片来源](https://norahsakal.com/blog/mcp-vs-api-model-context-protocol-explained/)）：

![](./images/mcp-overview.png)

可以看到 MCP 采用了非常经典的 C/S 架构（客户端/服务器），主要包括三个部分：

* **主机（Host）**： 一般是基于大模型的 AI 应用，比如 Claude Desktop、ChatGPT Desktop、Cursor 等桌面应用，需要访问外部数据或工具；
* **客户端（Client）**：内置在应用中，与 MCP 服务器建立一对一的连接；
* **服务器（Server）**：连接本地或远程的数据源，提供特定功能；
    * 本地数据源：文件或数据库；
    * 远程服务：外部 API 或互联网服务；

MCP 协议将所有的外部数据或工具以一种统一的方式接入 AI 应用，这就好比 USB-C 接口，将各种不同的电子设备统一成一种接口，从而让用户不再为准备各种各样不同的线缆插头而烦恼。简单说，MCP 就像一座桥梁，它本身不处理复杂逻辑，只负责协调 AI 应用与外部资源之间的信息流动。

### MCP 和 API 的区别

在推出 MCP 之前，AI 应用如果要对接外部工具，通常需要单独整合多个不同的 API，每个 API 的接口可能都各不相同，认证方式和错误处理也可能不同，极大地增加了开发复杂度和维护成本。

所以说，传统 API 就像不同的门，每扇门都有一把不同的钥匙，而 MCP 像一把万能钥匙，AI 应用开发者只要集成了这个万能钥匙，就可以打开任意的门。下面是 MCP 和传统 API 的对比：

![](./images/mcp-vs-api.png)

## MCP 初体验

接下来，让我们在 Claude Desktop 中体验下 MCP 是如何工作的。

首先，下载并安装 [Claude for Desktop](https://claude.ai/download)，注册并登录账号后，确保 Claude 能正常对话：

![](./images/claude-hi.png)

然后，打开 `Settings` -> `Developer` 配置页面：

![](./images/claude-settings.png)

点击 `Edit Config` 按钮，进入 Claude 配置文件所在目录，打开 `claude_desktop_config.json` 配置文件，输入如下内容：

```
{
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "/Users/aneasystone/Downloads/demo"
            ]
        }
    }
}
```

这是官方开发的 [Filesystem MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)，用于操作你的本地文件，比如读取、编辑、搜索等。最后一个参数是文件路径，表示只允许 Claude 访问这个目录，可以添加一个或多个。

> 注意这里通过 `npx` 命令启动 MCP Server，所以需要提前安装 [Node.js](https://nodejs.org/)，使用 `node --version` 确认你的电脑上是否具备 Node.js 环境。

配置好 Filesystem MCP Server 之后，重启 Claude Desktop 应用，Claude Desktop 在启动时会自动加载所有的 MCP Server（其实就是为每个 Server 启动一个独立的进程，运行配置文件中的命令）。加载成功后，在对话框右下角会看到一个小锤子的图标：

![](./images/claude-mcp-hammer.png)

点击小图标，可以看到 Filesystem MCP Server 自带的所有工具列表：

![](./images/claude-mcp-tools.png)

这时我们就可以在对话时让 Claude 调用这些工具了：

![](./images/claude-file-list.png)

Claude 在调用工具之前会提醒用户，只有当用户确认允许后才会真正执行相应操作。

> 运行 `npx` 默认是从 Node.js 官方仓库下载包，有时会非常慢，导致 Claude 加载 MCP Server 失败，可以通过环境变量将仓库地址改为国内的源：
> ```
> {
>     "mcpServers": {
>         "filesystem": {
>             "command": "npx",
>             "args": ...
>             "env": {
>                 "NPM_CONFIG_REGISTRY": "https://mirrors.huaweicloud.com/repository/npm/"
>             }
>         }
>     }
> }
> ```

## MCP 开发者指南

### 开发 MCP Server

https://modelcontextprotocol.io/quickstart/server

https://modelcontextprotocol.io/examples

### 开发 MCP Client

https://modelcontextprotocol.io/quickstart/client

https://modelcontextprotocol.io/clients

### 深入 MCP 原理

https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/lifecycle/

## 参考

* [Get started with the Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction)
* [Model Context Protocol · GitHub](https://github.com/modelcontextprotocol)
* [How to debug the Claude Model Context Protocol?](https://pcarion.com/blog/claude_mcp/)
* [Using LangChain With Model Context Protocol (MCP)](https://cobusgreyling.medium.com/using-langchain-with-model-context-protocol-mcp-e89b87ee3c4c)
* [Model Context Protocol (MCP). I would like to make a point regarding…](https://cobusgreyling.medium.com/model-context-protocol-mcp-da3e0f912bbc)
* [Exploring Model Context Protocol (MCP) With Spring AI](https://www.baeldung.com/spring-ai-model-context-protocol-mcp)
* [Introducing the Model Context Protocol Java SDK](https://spring.io/blog/2025/02/14/mcp-java-sdk-released-2/)
* [为 AI 模型赋予「三头六臂」：MCP 服务实用指南](https://sspai.com/prime/story/mcp-tutorial)
* [Claude 的 MCP (模型上下文协议）有啥用？](https://sspai.com/post/94360)
* [Spring AI 再进化，支持 MCP 协议](https://my.oschina.net/giegie/blog/17113995)
* [什么是模型上下文协议（MCP）？它如何比传统API更简单地集成AI？](https://baoyu.io/translations/mcp-vs-api-model-context-protocol-explained)
* [通俗易懂说清楚MCP的原理](https://mp.weixin.qq.com/s/v06i4dRTp6K7X2c0T0lslg)
* [通俗易懂说清楚什么是MCP](https://mp.weixin.qq.com/s/MU3I9PETpVDOdw12XkJSOg)
* [深入浅出理解MCP：从技术原理到实战落地](https://mp.weixin.qq.com/s/7QlMWCceHldt_B0TSDijbA)

### MCP Servers

* [Github - modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
* [Smithery - Model Context Protocol Registry](https://smithery.ai/server/mcp-server-sqlite-npx/tools)
* [Github - punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
* [GitHub - ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp)
* [Chat2DB 实现：Spring AI MCP 直连数据库](https://my.oschina.net/giegie/blog/17138364)

# 让 Claude Code 接入其他大模型

尽管 Claude Code 非常好用，但它的费用还是太贵了，之前为了体验，在 Anthropic Console 充了 5 美刀，只用了几天，就所剩无几了：

![](./images/claude-cost.png)

如果能让 Claude Code 使用其他较便宜的大模型（比如 OpenAI 或 DeepSeek 等）或本地大模型（如 Ollama 或 LM Studio 等）来处理编程任务，那就太好了，我们今天就来学习下如何让 Claude Code 接入其他模型。

## 接入 Claude 云提供商

Claude Code 默认使用 Anthropic 的 Claude 模型，但是还有一些其他的供应商也提供 Claude 模型，比如 [Amazon Bedrock](https://docs.anthropic.com/zh-CN/docs/claude-code/amazon-bedrock) 和 [Google Vertex AI](https://docs.anthropic.com/zh-CN/docs/claude-code/google-vertex-ai)，Claude Code 也支持接入这些模型。要使用这些第三方供应商的模型，首先需要按照供应商的要求，配置好对应的 AWS 凭证 或 GCP 凭据，然后通过环境变量告诉 Claude Code 使用供应商模型。

设置以下环境变量以启用 Bedrock 模型：

```
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
```

设置以下环境变量以启用 Vertex AI 模型：

```
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID
```

另外，不同供应商对模型的命名也不同，因此 Claude Code 还提供了两个环境变量来配置使用的模型。比如使用推理配置文件 ID 来配置 Bedrock 模型:

```
export ANTHROPIC_MODEL='us.anthropic.claude-opus-4-20250514-v1:0'
export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-3-5-haiku-20241022-v1:0'
```

这里要配置两个模型，`ANTHROPIC_MODEL` 为主要模型，用于复杂的编程任务；`ANTHROPIC_SMALL_FAST_MODEL` 为小型快速模型，用于简单的辅助任务；Claude Code 会根据情况自动切换。

## 配置企业代理

有很多企业对网络有特定要求，比如需要通过特定的代理来路由所有进出企业的流量，以实现安全、合规和监控目的。Claude Code 支持标准的 HTTP/HTTPS 代理配置：

```
export HTTPS_PROXY=https://proxy.example.com:8080
export HTTP_PROXY=http://proxy.example.com:8080
```

> Claude Code 不支持 SOCKS 代理。

如果代理需要基本身份验证，可以在代理 URL 中包含凭据：

```
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

如果代理使用了自定义的 SSL 证书，还需要设置正确的证书路径：

```
export SSL_CERT_FILE=/path/to/certificate-bundle.crt
export NODE_EXTRA_CA_CERTS=/path/to/certificate-bundle.crt
```

另外要注意的是，Claude Code 在运行过程中需要访问下面这些 URL 地址：

* `api.anthropic.com` - Claude API 端点
* `statsig.anthropic.com` - 遥测和指标
* `sentry.io` - 错误报告

确保这些 URL 在代理配置和防火墙规则中被列入白名单。

## 配置 LLM 网关

还有很多企业对大模型的访问是集中管控的，以实现使用跟踪或预算控制等，为满足这一类企业的需求，Claude Code 支持配置 LLM 网关。通过 LLM 网关，企业可以做到：

* **集中身份验证** - 对大模型的 API 密钥进行集中管理
* **使用跟踪** - 监控团队和项目的使用情况
* **成本控制** - 实施预算和速率限制
* **审计日志** - 跟踪所有模型交互以确保合规性
* **模型路由** - 无需更改代码即可在提供商之间切换

通过 `ANTHROPIC_BASE_URL` 配置 LLM 网关：

```
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

这里的 `/anthropic` 地址是 LiteLLM 网关透传的 Anthropic 接口，本质上还是调用 `api.anthropic.com` 接口，因此，在启动 LiteLLM 时需要配置 Anthropic 的 API KEY：

```
export ANTHROPIC_API_KEY=sk-ant-apikey
```

这个值将作为 `X-Api-Key` 请求头发送。

如果 LLM 网关也开启了 API KEY 认证，则通过 `ANTHROPIC_AUTH_TOKEN` 配置：

```
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key
```

这个值将作为 `Authorization` 和 `Proxy-Authorization` 请求头发送。

## 安装 LiteLLM 网关

我们知道，[LiteLLM](https://github.com/BerriAI/litellm) 是一个小巧精悍的 Python 库，兼容 100+ 不同的大模型，所有的模型都使用标准化的输入/输出格式；我们之前学过不少项目（比如 SurfSense、Mem0 等）都是使用 LiteLLM SDK 来调用大模型服务的，其实 LiteLLM 还可以充当 [LLM 网关](https://docs.litellm.ai/docs/simple_proxy) 来使用，通过 LLM 网关代理，我们可以实现 Claude Code 与其他模型的集成。

首先安装 LiteLLM 及其代理功能：

```
$ pip3 install 'litellm[proxy]'
```

然后建一个 `config.yaml` 配置文件：

```
model_list:
- model_name: gpt-4o
  litellm_params:
    model: gpt-4o
    api_base: https://api.bianxie.ai/v1
    api_key: os.environ/OPENAI_API_KEY
- model_name: gpt-4o-mini
  litellm_params:
    model: gpt-4o-mini
    api_base: https://api.bianxie.ai/v1
    api_key: os.environ/OPENAI_API_KEY
- model_name: deepseek-v3
  litellm_params:
    model: openrouter/deepseek/deepseek-chat-v3-0324:free
    api_base: https://openrouter.ai/api/v1
    api_key: os.environ/OPENROUTER_API_KEY
- model_name: deepseek-r1
  litellm_params:
    model: openrouter/deepseek/deepseek-r1-0528:free
    api_base: https://openrouter.ai/api/v1
    api_key: os.environ/OPENROUTER_API_KEY
```

接着使用 `litellm -c config.yaml` 启动 LiteLLM 网关：

![](./images/litellm-c.png)

访问 `http://localhost:4000/` 地址，应该显示 LiteLLM API 的 Swagger UI 页面，则说明 LiteLLM 网关启动成功。使用下面的命令验证接口能否正常调用：

```
$ curl -X POST http://localhost:4000/v1/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -d '{
    "model": "gpt-4o",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }'
```

这里使用的是 Anthropic 的 [`v1/messages` 接口](https://docs.litellm.ai/docs/anthropic_unified)，而不是 OpenAI 的 `/v1/chat/completions` 接口，因为 Claude Code 默认使用 Anthropic 接口。LiteLLM 可以同时兼容两种接口格式，注意有些 LLM 网关只支持 OpenAI 格式，是不行的。

最后通过将环境变量 `ANTHROPIC_BASE_URL` 设置成 LiteLLM 网关地址，就可以让 Claude Code 使用自定义的模型服务了：

```
export ANTHROPIC_BASE_URL=http://localhost:4000
export ANTHROPIC_AUTH_TOKEN=sk-1234
export ANTHROPIC_API_KEY=
export ANTHROPIC_MODEL=gpt-4o
export ANTHROPIC_SMALL_FAST_MODEL=gpt-4o-mini
export DISABLE_PROMPT_CACHING=1
claude
```

注意这里的 `DISABLE_PROMPT_CACHING` 配置，表示禁用 [提示缓存](https://docs.anthropic.com/zh-CN/docs/build-with-claude/prompt-caching)，大多数的三方模型不支持该功能。

## 解决连接错误

通过上面的方法启动 Claude Code 后，你可能会和我一样遇到下面这样的连接问题：

```
> hello
  ⎿  API Error (Connection error.) · Retrying in 1 seconds… (attempt 1/10)
    ⎿  TypeError (fetch failed)
  ⎿  API Error (Connection error.) · Retrying in 1 seconds… (attempt 2/10)
    ⎿  TypeError (fetch failed)
  ⎿  API Error (Connection error.) · Retrying in 2 seconds… (attempt 3/10)
    ⎿  TypeError (fetch failed)
...
```

尝试用 Wireshark 抓包：

![](./images/wireshark.png)

可以发现 Claude Code 发出的请求源和目标都是 `::1`，很显然这是 IPV6 地址，猜测可能是 LiteLLM 没有监听这个地址，于是修改 LiteLLM 的启动参数：

```
$ litellm -c config.yaml --host ::1 
```

再次运行 Claude Code 即可：

![](./images/claude-code-litellm.png)

## 小结

通过本文的学习，我们掌握了让 Claude Code 接入其他大模型的完整方案。从官方支持的 AWS Bedrock 和 Google Vertex AI，到通过 LiteLLM 网关实现与 OpenAI、DeepSeek 等第三方模型的集成，这些方法不仅可以降低使用成本，也为开发者提供了更灵活的选择空间。

需要注意的是，不同模型的能力差异较大，建议根据实际场景进行测试选择；部分 Claude 特性（如提示缓存、内置搜索）可能需要禁用或通过 MCP 实现。

# 学习 LiteLLM 的认证机制

在之前的两篇文章中，我们分别学习了 LiteLLM 的快速入门和模型管理。我们了解到，LiteLLM 不仅是一个统一的 SDK，更是一个功能强大的企业级 LLM 网关。在生产环境中，如何确保 LLM 资源的安全访问？如何为不同用户和团队分配不同的权限？如何追踪每个用户的使用情况和成本？如何精确控制成本和防止滥用？这些都是访问控制需要解决的核心问题。

LiteLLM 的访问控制系统采用多层次的安全架构，从基础的 API Key 认证到企业级的 JWT 认证，从简单的用户管理到复杂的团队权限体系，为不同规模的应用提供了灵活的解决方案：

**认证层次**：
- **虚拟 API Key**：为每个用户或团队生成唯一的虚拟 Key
- **JWT Token**：支持企业级 OpenID Connect (OIDC) 认证
- **自定义认证**：集成企业现有的身份认证系统

**授权体系**：
- **用户级权限**：基于角色的访问控制（RBAC）
- **团队级权限**：团队成员共享模型访问权限
- **组织级权限**：大型企业的多层级管理

**控制维度**：
- **模型访问**：控制用户可以使用的模型
- **接口访问**：限制可调用的 API 接口
- **流量控制**：请求频率和并发数限制
- **成本控制**：预算限制和消费追踪

我们今天主要关注第一部分，来学习下 LiteLLM 的认证机制。

## 虚拟 Key 认证

在之前的学习中，我们在调用模型接口时使用的 API Key 一直都是 `sk-1234`，这个是我们在配置文件中配置的 **Master Key**，也就是管理员密钥：

```yaml
general_settings:
  master_key: sk-1234
```

对于个人开发者来说，只用一个简单的 API Key 可能就足够了，但是对于团队或企业来说，一个 Key 无法区分不同的用户或应用，而且 Master Key 的权限过大，这时我们就需要引入 Virtual Key 的概念了。

**虚拟 Key（Virtual Key）** 是 LiteLLM 最核心的认证机制，它借鉴了云服务商的 API Key 管理模式，为每个用户或应用生成独立的访问密钥。LiteLLM 的虚拟 Key 提供了一层抽象，使得：

- 你可以为不同的用户、团队、应用生成不同的 Key
- 每个 Key 可以独立配置访问权限和预算限制
- 支持 Key 的轮换和撤销
- 所有使用行为都由 Proxy 记录和追踪

接下来我们生成一个虚拟 Key 验证下。虚拟 Key 的生成需要数据库支持，因此首先配置数据库连接（昨天学习模型的动态管理时已经配过）：

```yaml
general_settings:
  master_key: sk-1234
  database_url: "postgresql://postgres:password@127.0.0.1:5432/litellm"
```

然后通过 `/key/generate` 接口生成 Key：

```bash
$ curl 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "models": ["gpt-4o"],
    "metadata": {"user": "zhangsan@example.com"}
  }'
```

接口响应如下：

```json
{    
  "key": "sk-qC5b02PjnQVdq3FPYY37wQ",
  "key_name": "sk-...37wQ",
  "models": [
    "gpt-4o"
  ],
  "metadata": {
    "user": "zhangsan@example.com"
  },
  "user_id": null,
  "team_id": null,
  "model_max_budget": {},
  "model_rpm_limit": null,
  "model_tpm_limit": null,
  "max_budget": null,
  "max_parallel_requests": null,
  "guardrails": null,
  "allowed_routes": [],
  // ...
}
```

> 可以看到，接口响应中除了 `key` 之外，还有一些关于用户、团队、请求频率、并发限制等信息，这些内容涉及 LiteLLM 的授权体系和访问控制机制，我们后面再具体学习。

使用这个虚拟 Key 请求 `/chat/completions` 接口：

```bash
$ curl -X POST 'http://127.0.0.1:4000/chat/completions' \
  -H 'Authorization: Bearer sk-qC5b02PjnQVdq3FPYY37wQ' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

接口验证正常，说明虚拟 Key 生成成功。

### 支持多种 Header 格式

LiteLLM 的灵活设计使其能够支持多种 Header 格式，兼容不同的客户端库和工具：

| Header 名称 | 用途 | 优先级 |
|-----------|------|------|
| `x-litellm-api-key` | LiteLLM 自定义 Key | 1 (最高) |
| `Authorization` | OpenAI 兼容格式 | 2 |
| `API-Key` | Azure 风格 | 3 |
| `x-api-key` | Anthropic 格式 | 4 |
| `x-goog-api-key` | Google AI Studio | 5 |
| `Ocp-Apim-Subscription-Key` | Azure APIM | 6 |
| 其他自定义 Header | 配置化支持 | 7 |

比如像下面这样请求也是可以的：

```bash
$ curl -X POST 'http://127.0.0.1:4000/chat/completions' \
  -H 'x-litellm-api-key: sk-qC5b02PjnQVdq3FPYY37wQ' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

这样的设计让 LiteLLM 可以轻松地代理来自各种来源的请求，而无需修改客户端代码。

### 虚拟 Key 的存储和验证

为了保证安全性，虚拟 Key 在数据库中采用 **哈希值存储**，这样做的好处是，即使数据库被泄露，攻击者也无法直接使用 Key（因为数据库中只有哈希值）。

另外，LiteLLM 使用 **分层缓存策略** 进行虚拟 Key 的验证：

![](./images/api-key-verification.png)

通过分层缓存，大多数请求不需要访问数据库，大大提高了虚拟 Key 的验证性能。

### 客户端凭据透传

除了传统的服务器端认证，LiteLLM 还支持让客户端直接传递自己的 API Key，这在某些场景下可能有用，比如开发者使用自己的 API Key 进行测试，或者用户希望使用自己的 API Key，但又不希望配置到 LiteLLM 里。

通过下面的参数启用客户端凭据透传：

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
      configurable_clientside_auth_params: ["api_key", "api_base"] # 支持透传的字段
```

客户端调用示例如下：

```python
import openai

client = openai.OpenAI(
  api_key="sk-1234",
  base_url="http://localhost:4000"
)

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "user", "content": "Hello"}],
  extra_body={
    "api_key": "sk-client-xxx",  # 客户端自己的 API 密钥
    "api_base": "https://api.openai.com/v1"
  }
)
```

LiteLLM 会遍历 `configurable_clientside_auth_params` 参数，将客户端传递的参数和系统配置的参数进行合并。

> 有意思的，客户端不仅可以传 `api_key` 或 `api_base` 等字段，甚至可以传整个 `model_list`，将 LiteLLM 的配置完全架空。

## JWT 认证与 OIDC 集成

虽然虚拟 Key 是 LiteLLM 最核心的认证方式，但对于某些企业场景，这种认证方式可能不够灵活，企业往往已经有一套比较成熟的 **身份认证系统（Identity Provider, IDP）**，比如：

- **Azure AD**：Microsoft 的企业身份平台
- **Keycloak**：开源身份和访问管理解决方案
- **Google Cloud Identity**：Google 的企业 SSO
- **Okta**：专业的身份管理服务

他们更希望能直接复用这套认证机制。

LiteLLM 支持通过 **JWT 令牌** 与这些系统集成，而无需维护独立的用户数据库。

> 注意，这是一个企业级特性，需要购买授权。

### OIDC 简介

LiteLLM 和身份认证系统之间的交互遵循 [OIDC](https://openid.net/) 标准。

**OpenID Connect (OIDC)** 是一个基于 OAuth 2.0 的身份认证协议，它在 OAuth 2.0 的基础上增加了身份层，使得应用可以验证用户的身份，它已经成为企业级应用的标准认证方式。

OIDC 的核心优势如下：

- **标准化**：遵循 OAuth 2.0 和 OpenID Connect 规范
- **单点登录**：支持 SSO，用户一次登录，全组织访问
- **令牌安全**：JWT 令牌可以包含丰富的用户信息，支持签名和加密
- **广泛支持**：被所有主流云服务和身份提供商支持

下面是 OIDC 规范，对此感兴趣的朋友可以看看：

* https://openid.net/developers/how-connect-works/

### JWT 简介

**JWT（JSON Web Token）** 是一种基于 JSON 的轻量级身份认证与信息交换标准（RFC 7519），广泛用于分布式系统、API 接口、前后端分离架构中，核心作用是在客户端与服务器之间安全传递 **可验证的声明**（如用户身份、权限范围等），无需服务器存储会话状态。

在传统的会话认证（如 Session）中，服务器需要存储用户的会话信息，当用户量增大或服务分布式部署时，会面临会话同步复杂、服务器存储压力大等问题。而 JWT 通过 **客户端存储令牌 + 服务器验证令牌** 的模式，解决了这些痛点，其核心优势包括：

- **无状态**：服务器无需存储会话数据，仅通过令牌本身即可验证合法性，降低服务器存储成本，便于服务水平扩展（多台服务器可共享认证逻辑）；
- **跨域友好**：JWT 基于 HTTP 头传递，天然支持跨域场景（如前后端分离、多服务间调用）；
- **轻量灵活**：基于 JSON 格式，体积小、传输快，且可自定义声明字段，满足不同业务需求；
- **自包含**：令牌本身包含了用户身份、权限等核心信息，减少服务器查询数据库的次数（无需每次认证都查用户表）；

一个 JWT 令牌由三部分组成，用点号分隔：

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIn0.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

分别代表：

- **Header**：算法和令牌类型信息
- **Payload**：用户信息和声明（Claims）
- **Signature**：数字签名，用于验证数据完整性

可以通过下面的网站验证和查看 JWT 令牌中的内容：

* https://www.jwt.io/

### 基于 Keycloak 的 JWT 认证实战

下面我使用 [Keycloak](https://www.keycloak.org/) 这款开源的身份认证系统来演示下如何在 LiteLLM 中实现 JWT 认证。

![](./images/keycloak.png)

这是一款由 Red Hat 主导开发并维护的开源 **身份和访问管理（IAM）** 工具，旨在为现代应用（包括 Web 应用、移动应用、API 服务等）提供统一、安全且标准化的 **身份认证（Authentication）** 与 **授权（Authorization）** 能力，帮助开发者快速集成身份管理功能，无需重复造轮子。

#### Keycloak 环境准备

首先使用下面的命令启动 Keycloak 服务：

```bash
$ docker run \
  -p 8080:8080 \
  -e KC_BOOTSTRAP_ADMIN_USERNAME=admin \
  -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:26.4.2 start-dev
```

服务启动成功后，在浏览器访问 `http://localhost:8080/` 并使用默认的用户名和密码登录：

![](./images/keycloak-admin-ui.png)

点击 “Manage realms” 菜单，创建一个名为 `litellm` 的 **领域（Realm）**，这是 Keycloak 中最高级别的隔离单位，相当于 **租户**：

![](./images/keycloak-create-realm.png)

创建完成后会自动切到这个领域，然后点击 “Users” 菜单，在这个领域下创建一个用户，用户名为 `zhangsan`：

![](./images/keycloak-create-user.png)

创建完成后进入该用户的详情，点击 “Credentials” 菜单，再点击 “Set password” 按钮，为用户设置一个长期密码（注意将 Temporary 勾掉）：

![](./images/keycloak-create-user-set-password.png)

然后再点击 “Clients” 菜单，创建一个客户端：

![](./images/keycloak-create-client.png)

其中 Client ID 命名为 `litellm`，点击 Next 进入 “Capability Config” 页面：

![](./images/keycloak-create-client-capability.png)

将 “Client authentication” 选项开启，同时在 “Authentication flow” 中将 “Direct access grants” 开启。接着，点击 Next 进入 “Login Settings” 页面，保持默认即可，点击 Save 按钮，完成客户端的创建。

#### 开启 JWT 认证

至此 Keycloak 环境准备就绪，接下来让 LiteLLM 开启 JWT 认证。第一步，通过环境变量设置 Keycloak 的公钥端点：

```bash
# 注意 `litellm` 是领域名称
export JWT_PUBLIC_KEY_URL="http://localhost:9009/realms/litellm/protocol/openid-connect/certs"
```

这个 URL 是 OpenID Connect 标准的 **JWKS（JSON Web Key Set）** 端点，方便客户端批量获取所需密钥，里面包含了用于验证签名或加密的公钥。

第二步，在配置中启用 JWT 认证：

```yaml
general_settings:
  master_key: sk-1234
  database_url: "postgresql://postgres:password@127.0.0.1:5432/litellm"
  enable_jwt_auth: true # 开启 JWT 认证
```

第三步，重启 LiteLLM Proxy 服务：

```bash
$ litellm -c config.yaml
```

第四步，使用 Client ID、Client Secret、用户名、密码，调用 Keycloak 获取 JWT 令牌：

```bash
$ curl -X POST \
  http://localhost:9009/realms/litellm/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=litellm" \
  -d "client_secret=0CtlgEvGHU3XNjDAmwHPn5p8wT78JGEp" \
  -d "username=zhangsan" \
  -d "password=12345678"
```

其中 Client Secret 可以在 Client 详情中找到：

![](./images/keycloak-clients-details.png)

接口返回结果如下：

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5...",
  "expires_in": 300,
  "refresh_expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzUxMiIsInR5...",
  "token_type": "Bearer",
  "not-before-policy": 0,
  "session_state": "dca8f2d7-eac4-d6e7-799b-f7b80da4d841",
  "scope": "profile email"
}
```

这个 `access_token` 就是 JWT 令牌，我们可以用它来调用 `/chat/completions` 接口：

```bash
$ curl -X POST 'http://127.0.0.1:4000/chat/completions' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5...' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

LiteLLM 会根据从 `JWT_PUBLIC_KEY_URL` 获取的公钥对该令牌进行验证（类似数字签名的原理），这就是 LiteLLM 的 JWT 认证流程。

## 自定义认证

虽然 LiteLLM 提供了虚拟 Key、JWT 等多种认证方式，但在某些高度定制化的场景中，你可能需要实现自己的认证逻辑。比如：

- **现有系统集成**：你有一套自定义的用户认证系统
- **特殊业务规则**：需要根据特定条件验证用户
- **外部服务集成**：需要调用外部服务进行认证
- **多步认证**：需要组合多个认证因素

LiteLLM 允许你提供自定义的认证函数，完全控制身份认证过程。其核心是实现一个异步函数，该函数接收请求和 API Key，然后返回一个认证对象：

```python
from fastapi import Request
from litellm.proxy._types import UserAPIKeyAuth

async def user_api_key_auth(request: Request, api_key: str) -> UserAPIKeyAuth: 
  """
  自定义认证函数

  参数:
    request: FastAPI 请求对象，包含 HTTP 请求的所有信息
    api_key: 从请求头中提取的 API Key

  返回:
    UserAPIKeyAuth: 认证成功时返回用户认证对象

  异常:
    Exception: 认证失败时抛出异常
  """
  try: 
    if api_key.startswith("my-custom-key-"):
      return UserAPIKeyAuth(api_key=api_key)
    raise Exception("Invalid API key")
  except: 
    raise Exception("Authentication failed")
```

将上面的内容保存到 `custom_auth.py` 文件中，并放置于和 `config.yaml` 文件同级的目录下。在配置文件中指定自定义认证函数的位置：

```yaml
general_settings:
  master_key: sk-1234
  database_url: "postgresql://postgres:password@127.0.0.1:5432/litellm"
  custom_auth: custom_auth.user_api_key_auth  # 模块路径.函数名
```

然后重启 LiteLLM Proxy 服务，此时，任何 `my-custom-key-` 开头的 Key 都能通过验证了：

```bash
$ curl -X POST 'http://127.0.0.1:4000/chat/completions' \
  -H 'Authorization: Bearer my-custom-key-888' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

值得注意的是，在认证流程中，自定义认证是最优先执行的，因此如果开启了该功能，Master Key 和 虚拟 Key 就不起作用了。为了同时兼容，企业版的 LiteLLM 支持一个更灵活的混合模式：

```yaml
general_settings:
  custom_auth: custom_auth.user_api_key_auth
  custom_auth_settings:
    mode: "auto"  # 支持虚拟 Key 和自定义认证混用
```

当自定义认证失败后，LiteLLM 会继续沿用虚拟 Key 的验证流程。

## 小结

通过这篇文章，我们系统地学习了 LiteLLM Proxy 的认证机制，这是构建企业级 LLM 网关的核心基础。主要内容包括：

- **虚拟 Key 认证**：LiteLLM 最核心的认证方式，通过为每个用户或应用生成独立的 API Key，实现细粒度的权限隔离和使用追踪；采用哈希存储和分层缓存策略确保了安全性和性能的平衡；支持多种 Header 格式使其能够兼容各种客户端和工具；
- **JWT 认证与 OIDC 集成**：为企业用户提供了一条与现有身份认证系统无缝集成的路径，无需在 LiteLLM 中维护独立的用户数据库，充分利用企业已有的 IAM 基础设施；
- **自定义认证**：完全开放的认证扩展机制，允许企业根据特定的业务规则实现复杂的认证逻辑，支持与任何现有系统的集成；企业版提供了混合模式，可以同时支持虚拟 Key 和自定义认证；

LiteLLM 的认证设计体现了分层的思想：从基础的虚拟 Key 面向个人开发者和小型团队，到 JWT/OIDC 面向已有 IAM 的企业，再到自定义认证面向有特殊需求的场景。这种分层的、可扩展的设计，使得 LiteLLM 能够适应从个人项目到大规模企业级应用的各种场景。

在后续的学习中，我们将继续深入 LiteLLM 的权限管理和访问控制系统，学习如何为不同的用户和团队分配不同的权限，如何追踪使用情况和成本，如何设置预算限额防止滥用。敬请期待！

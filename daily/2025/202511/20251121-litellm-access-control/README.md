# 学习 LiteLLM 的访问控制

在前两篇文章中，我们深入探讨了 LiteLLM 的认证机制和用户管理体系，认证机制解决了 **你是谁** 的问题，用户管理则从组织、团队到用户的多层架构，以及基于角色的访问控制（RBAC）模型解决的是 **你能做什么** 的问题。

而今天我们要学习的访问控制机制则是用户管理的延续，从更细的粒度控制用户的行为，没有适当的访问控制，你的 LLM 网关可能会面临很多风险，比如：用户访问了不应该访问的模型，导致成本失控；恶意用户滥用 API，造成拒绝服务攻击；缺乏配额管理，导致某些用户耗尽所有资源。

LiteLLM 提供了一套完整的访问控制机制：

1. **模型访问控制**：控制用户可以使用哪些模型
2. **接口访问控制**：控制用户可以调用哪些 API 接口
3. **配额管理**：管理用户的请求频率、并发数、成本预算等资源使用限制

下面我们从最基础的模型访问控制开始，逐步深入学习。

## 模型访问控制

模型访问控制是 LiteLLM 访问控制的第一道防线，它决定了用户或团队是否可以使用特定的模型或模型组。

### 虚拟 Key 级别的模型限制

最简单的模型访问控制方式是为虚拟 Key 指定允许的模型列表。其实我们之前在创建虚拟 Key 时已经用过，通过 `models` 参数来限制它可以访问的模型：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "models": ["gpt-4o"],
    "metadata": {"user": "zhangsan@example.com"}
  }'
```

生成的密钥只能调用 `gpt-4o` 这个模型，如果尝试调用其他模型，则会收到错误响应：

```json
{
  "error": {
    "message": "key not allowed to access model. This key can only access models=['gpt-4o']. Tried to access deepseek",
    "type": "key_model_access_denied",
    "param": "model",
    "code": "401"
  }
}
```

### 团队级别的模型限制

我们还可以为团队指定允许的模型列表。首先创建一个团队，并为其指定允许的模型：

```bash
$ curl -X POST 'http://127.0.0.1:4000/team/new' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "team_alias": "demo_team",
    "models": ["gpt-4o"]
  }'
```

或者在 Admin UI 后台创建：

![](./images/create-team.png)

然后为该团队创建虚拟 Key：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "team_id": "950db486-fa2c-46e7-bfbc-3ac39e15fad2"
  }'
```

此时，团队成员使用该密钥只能调用 `gpt-4o` 这个模型，当团队成员使用该密钥访问未授权模型时，LiteLLM 会返回错误信息：

```json
{
  "error": {
    "message": "team not allowed to access model. This team can only access models=['gpt-4o']. Tried to access deepseek",
    "type": "team_model_access_denied",
    "param": "model",
    "code": "401"
  }
}
```

> 注意，如果使用团队级别的模型限制，调用 `/key/generate` 时 `models` 参数是不生效的。

同样地，我们也可以针对组织或用户来限制模型的访问，做法基本类似，调用 `/organization/new` 或 `/user/new` 时传入 `models` 参数即可，此处略过。

### 模型访问组

对于需要动态管理模型访问权限的场景，LiteLLM 提供了 **模型访问组** 的功能，允许将多个模型组织成一个逻辑组，便于批量分配权限。

首先，在配置文件中定义模型访问组：

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
    model_info:
      access_groups: ["beta-models"]  # 👈 模型访问组

  - model_name: claude
    litellm_params:
      model: anthropic/claude-sonnet-4-20250514
      api_key: os.environ/ANTHROPIC_API_KEY
    model_info:
      access_groups: ["beta-models"]  # 👈 模型访问组
```

然后，创建虚拟 Key 时指定访问组：

```bash
$ curl -X POST 'http://localhost:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "models": ["beta-models"]
  }'
```

这个 Key 可以访问所有标记为 `beta-models` 的模型，如果后续添加了新的模型到这个组，也会自动授权。模型访问组的主要优势在于：

- **动态管理**：可以随时向访问组添加新模型，所有使用该组的用户自动获得访问权限
- **批量操作**：一次可以为多个用户分配相同的模型权限
- **版本控制**：可以创建不同的访问组用于不同环境（如 dev、staging、prod）

对于需要更灵活访问控制的场景，LiteLLM 还支持通配符模型。你可以使用模式匹配来控制对具有特定前缀或后缀的模型的访问：

```yaml
model_list:
  - model_name: openai/*
    litellm_params:
      model: openai/*
      api_key: os.environ/OPENAI_API_KEY
    model_info:
      access_groups: ["default-models"]

  - model_name: openai/o1-*
    litellm_params:
      model: openai/o1-*
      api_key: os.environ/OPENAI_API_KEY
    model_info:
      access_groups: ["restricted-models"]
```

根据配置，`default-models` 访问组的用户可以访问 `openai/gpt-4` 但不能访问 `openai/o1-mini`。

用户可以通过 `/v1/models` 接口查看自己有权访问的模型：

```bash
$ curl -X GET 'http://localhost:4000/v1/models' \
  -H 'Authorization: Bearer sk-3zO1MHhHFme9aGXfWCiMXg'
```

## 接口访问控制

除了限制用户能调用哪些模型，LiteLLM 还支持限制用户能调用哪些 API 接口。

### 基于角色的接口权限

在用户管理体系中，我们学习了基于角色的访问控制（RBAC），不同角色的用户自动拥有不同的接口权限：

- **代理管理员（Proxy Admin）** 拥有所有接口的访问权限，包括：
    - 用户管理接口：`/user/*`
    - 团队管理接口：`/team/*`
    - 密钥管理接口：`/key/*`
    - 组织管理接口：`/organization/*`
- **内部用户（Internal User）** 只能访问自己的密钥管理接口、自己的使用情况接口和 LLM 调用接口等
- **团队成员（Team Member）** 的接口权限由团队管理员精确控制，LiteLLM 支持对每个接口进行单独的权限配置。

### 限制可调用的接口

除此之外，在生成虚拟 Key 时我们还可以指定 `allowed_routes` 参数来限制用户能调用的接口：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "models": ["gpt-4o"],
    "allowed_routes": ["/v1/chat/completions", "/v1/embeddings"]
  }'
```

这样，这个 Key 就只能调用 `/v1/chat/completions` 和 `/v1/embeddings` 这两个接口，其他接口如获取模型列表、查询成本等都会被拒绝。

## 请求速率限制

LiteLLM 支持三种类型的速率限制：

- **RPM（Requests Per Minute）**：每分钟请求数限制
- **TPM（Tokens Per Minute）**：每分钟令牌数限制
- **Max Parallel Requests**：最大并发请求数限制

我们可以在 `config.yaml` 文件中对指定模型进行全局限制：

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
      rpm: 10
      tpm: 10000
```

或者在创建虚拟 Key 时加上这三个参数：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "models": ["gpt-4o"],
    "rpm_limit": 3,
    "tpm_limit": 100,
    "max_parallel_requests": 1
  }'
```

通过上面这个命令生成的 Key 每分钟最多只能发送 3 个请求，最多只能消耗 100 个 Token，并且同时最多只能有 1 个并发请求。

> 值得注意的是，RPM 和 TPM 超过限制时，并不会报错，而是排队等待；只有并发数超过限制才会报 429 Too Many Requests 错误。

如果虚拟 Key 对应多个模型，也可以为每个模型单独设置速率限制：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "models": ["gpt-4o", "gpt-3.5-turbo"],
    "model_rpm_limit": {
      "gpt-4o": 30,
      "gpt-3.5-turbo": 100
    },
    "model_tpm_limit": {
      "gpt-4o": 5000,
      "gpt-3.5-turbo": 10000
    }
  }'
```

> 没有 `model_max_parallel_requests` 参数，暂时无法为每个模型单独设置并发路数。

### 灵活的限制范围

和模型限制一样，LiteLLM 也支持在组织、团队或内部用户上配置速率限制。其中团队级别的速率限制可以是针对整个团队的，也可以是针对团队内单个成员的：

```bash
$ curl -X POST 'http://localhost:4000/team/new' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "team_alias": "demo_team",
    "rpm_limit": 100,    # 团队整体 RPM 限制
    "tpm_limit": 10000,  # 团队整体 TPM 限制
    "team_member_rpm_limit": 10,   # 单个成员 RPM 限制
    "team_member_tpm_limit": 1000  # 单个成员 TPM 限制
  }'
```

值得注意的是，要启用团队成员速率限制，启动 LiteLLM 之前必须要设置环境变量 `EXPERIMENTAL_MULTI_INSTANCE_RATE_LIMITING=true`，如果不这样做，团队成员的速率限制将不会生效。

> 当你部署多实例时，也需要设置这个环境变量。

另外，速率限制还可以配置在终端用户上。LiteLLM 的用户分为两种：**内部用户（Internal User）** 和 **终端用户（End User）**，内部用户是管理和使用 LiteLLM 平台的内部人员，终端用户是通过 LiteLLM 平台获得 LLM 服务的外部用户，也被称为 **客户（Customer）**，他们没有自己的 API Key，在调用接口时通过 `user` 参数进行区分：

```bash
$ curl -X POST 'http://127.0.0.1:4000/chat/completions' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "user": "demo_customer",
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

要对终端用户进行限流，需要先创建一个配额：

```bash
$ curl -X POST 'http://127.0.0.1:4000/budget/new' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "budget_id" : "free-tier",
    "rpm_limit": 3
  }'
```

然后使用该配额创建一个终端用户：

```bash
# 也可以使用 /end_user/new 接口
$ curl -X POST 'http://127.0.0.1:4000/customer/new' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id" : "demo_customer",
    "budget_id": "free-tier"
  }'
```

这样就限制了这个终端用户一分钟只能请求 3 次。

### 动态速率限制

在多个用户共享同一个模型部署的场景中，静态的速率限制可能导致资源分配不合理的情况。上文提到，速率限制可以配置在全局的配置文件中，假设我们给 A 模型限制了一分钟 60 次请求，如果某个用户突然疯狂发送请求，可能会导致其他用户的请求全部被限制。

为此，LiteLLM 提供了 **动态速率限制** 的功能，可以根据活跃密钥的数量动态分配 TPM/RPM 配额。

启用动态速率限制只需在配置文件中添加回调即可：

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
      rpm: 10 # 全局 10 RPM

litellm_settings:
  callbacks: ["dynamic_rate_limiter_v3"]
```

它的工作原理是：

1. 计算当前活跃密钥数量
2. 将模型的 TPM/RPM 配额平均分配给所有活跃密钥
3. 定期调整分配比例以适应请求模式的变化

因此，如果同时有 5 个 Key 在发送请求，每个 Key 都能得到 2 RPM 的配额（10/5）。如果只有 2 个 Key，每个能得到 5 RPM。这样就确保了资源的公平分配。

### 优先级预留

对于更复杂的场景，还可以为不同的优先级预留资源。比如，生产环境的应用应该获得 90% 的资源，而开发环境只有 10% 的资源：

```yaml
litellm_settings:
  callbacks: ["dynamic_rate_limiter_v3"]
  priority_reservation:
    "prod": 0.9        # 生产环境：90%
    "dev": 0.1         # 开发环境：10%
  priority_reservation_settings:
    default_priority: 0  # 未指定优先级的：0%
    saturation_threshold: 0.5  # 模型使用率达到 50% 时启用严格模式（非严格模式下，使用率可以超出限制）
```

创建 Key 时指定优先级：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "models": ["gpt-4o"],
    "metadata": {"priority": "prod"}
  }'
```

标记为 `prod` 的 Key 会优先获得资源，LiteLLM 会确保这个 Key 至少获得 90% 的使用率，而标记为 `dev` 的 Key 只能获得 10% 的使用率。

## 成本追踪

我们在学习 LiteLLM 的模型管理时曾经提到过，LiteLLM 维护了一个完整的模型成本映射表，每次调用都会自动计算成本。默认情况下，成本是根据 **输入和输出的 Token 数** 乘以 **模型的单位价格** 来计算的：

```
cost = (input_tokens × input_cost_per_token) + (output_tokens × output_cost_per_token)
```

如果默认的价格不符合你的情况，可以在 `config.yaml` 中覆盖默认价格：

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
    model_info:
      input_cost_per_token: 0.00001  # 自定义价格
      output_cost_per_token: 0.00002
```

> 价格单位为 USD

或者在全局设置中配置供应商折扣：

```yaml
cost_discount_config:
  openai: 0.1         # OpenAI 打 9 折
  anthropic: 0.15     # Anthropic 打 8.5 折
  vertex_ai: 0.2      # Vertex AI 打 8 折
```

折扣会在成本计算后自动应用，LiteLLM 会返回原始成本和折扣后的成本。

成本追踪数据存储在数据库中，你可以通过多种方式查询：

```bash
# 查询单个 Key 的成本
$ curl 'http://127.0.0.1:4000/key/info?key=sk-xyz' \
  -H 'Authorization: Bearer sk-1234'

# 查询用户的总消费
$ curl 'http://127.0.0.1:4000/user/info?user_id=user-123' \
  -H 'Authorization: Bearer sk-1234'

# 查询团队的消费
$ curl 'http://127.0.0.1:4000/team/info?team_id=team-xyz' \
  -H 'Authorization: Bearer sk-1234'

# 生成成本报告（企业版特性）
$ curl 'http://127.0.0.1:4000/global/spend/report?start_date=2025-11-01&end_date=2025-11-30&group_by=team' \
  -H 'Authorization: Bearer sk-1234'
```

LiteLLM 还支持[与计费系统集成](https://docs.litellm.ai/docs/proxy/billing)，比如可以自动将成本数据推送到 [Lago](https://docs.getlago.com/welcome) 平台：

```yaml
litellm_settings:
  callbacks: ["lago"]
```

## 预算限制

有了成本追踪，就能很容易实现预算限制了。LiteLLM 支持在多个层级设置预算限制，最直接的方式是在生成 Key 时设置 `max_budget`：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "models": ["gpt-4o"],
    "max_budget": 100.0
  }'
```

这个 Key 现在最多只能消耗 $100，一旦超过预算，后续的请求会被拒绝。

> 或者通过 `soft_budget` 参数设置软预算限制，超过这个值时发送警告但不阻止请求。

和请求速率限制类似，我们还可以为用户设置总预算，即使用户有多个 Key，这些 Key 的消费会统计到用户的总预算中；或者为团队设置总预算，团队下的所有成员使用的 Key 的消费都会累计到团队的总预算中；或者通过 `model_max_budget` 参数为不同模型设置不同预算；或者通过 `/budget/new` 创建配额，然后为终端用户设置总预算。

### 预算周期与自动重置

有时候我们希望用户的预算能够定期重置。比如免费用户每个月重置 $10 的额度，这就需要用到 `budget_duration` 参数：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "models": ["gpt-4o"],
    "max_budget": 10.0,
    "budget_duration": "30d"
  }'
```

支持的时间周期包括：

- `"30s"` - 30 秒
- `"30m"` - 30 分钟
- `"1h"` - 1 小时
- `"1d"` - 1 天
- `"30d"` - 30 天（一个月）

### 临时预算增加

有时候，用户由于突然的业务需求可能需要超出预算。对于这种场景，LiteLLM 支持临时预算增加功能：

```bash
curl -L -X POST 'http://localhost:4000/key/update' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "key": "sk-your-key",
    "temp_budget_increase": 100,
    "temp_budget_expiry": "2025-11-30"
  }'
```

临时预算增加也是一个企业特性，它有以下特点：

- 固定过期时间，过期后自动失效
- 不影响原有的预算配置
- 支持多次临时增加
- 只能加在 API Key 上，无法为用户、团队、组织增加临时预算

### 标签级别的预算

对于需要跨多个维度跟踪成本的企业场景，LiteLLM 还支持按照 **标签（Tag）** 来分配预算，这对于按照功能、项目、成本中心来追踪成本特别有用：

```bash
$ curl -X POST 'http://127.0.0.1:4000/tag/new' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "marketing-chatbot",
    "description": "Marketing team chatbot",
    "max_budget": 200.0,
    "budget_duration": "30d"
  }'
```

然后在请求时添加标签：

```bash
$ curl -X POST 'http://127.0.0.1:4000/chat/completions' \
  -H 'Authorization: Bearer sk-xyz' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "hello"}],
    "metadata": {
      "tags": ["marketing-chatbot", "campaign-2024"]
    }
  }'
```

## 小结

LiteLLM 的访问控制机制构成了一个多维度的安全防护体系，从三个核心维度确保平台的稳定运行和成本可控：

- **访问范围控制**：通过模型访问限制防止未授权模型使用，避免成本失控；模型访问组提供动态、批量化的权限管理能力；接口访问控制精确限制用户可调用的 API 端点；
- **资源配额管理**：通过 RPM、TPM、并发三种速率限制策略确保公平的资源分配；动态速率限制根据活跃用户数智能调整配额，避免资源浪费或抢占；优先级预留机制保障关键业务的资源需求；
- **成本预算控制**：实时成本追踪提供透明的费用可见性；多层级预算限制（Key/用户/团队/标签）满足不同场景需求；预算周期管理与临时预算增加提供灵活的额度控制；

这套完整的访问控制体系不仅保障了 LiteLLM 网关的安全性，更通过精细化的资源管理和成本控制，为企业级 AI 应用提供了可靠的治理框架。合理配置这些机制，可以在保证用户体验的同时，最大化资源利用效率并控制运营成本。

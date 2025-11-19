# 学习 LiteLLM 的用户管理体系

在上一篇文章中，我们学习了 LiteLLM 的认证机制，从基础的虚拟 Key 到企业级的 JWT/OIDC 认证，了解了如何确保 API 访问的安全性。然而，认证只是第一步，解决的是 **你是谁** 的问题；接下来我们需要解决的是 **你能做什么** 的问题，这就是 **用户管理** 和 **权限控制** 要解决的问题。

## 核心概念

LiteLLM 的用户管理体系建立在四个核心概念上：

1. **组织（Organization）** 可以包含多个团队，是 LiteLLM 中最高层级的管理单位，每个组织相当于一个独立的租户；
2. **团队（Team）** 是组织内部的工作单位，可以包含多个内部用户；团队的设计非常灵活，你可以按部门划分，也可以按项目划分；
3. **内部用户（Internal Users）** 可以创建 API Key、进行 API 调用、查看使用情况等；一个用户可以拥有多个 API Key，并且可以属于多个团队；
4. **API Key** 用于 LiteLLM API 的身份验证，我们在上一篇详细介绍过，它可以与团队相关联，或与用户相关联，或同时与两者相关联；

他们的关系如下：

![](./images/user-heirarchy.png)

### 三种密钥类型

正如上文所说，API Key 可以与团队或用户相关联，基于不同的组合，API Key 分为三种类型：

1. **用户密钥（User-only Key）**：它关联到特定用户，跟随用户生命周期，用于个人预算和追踪，当删除用户时密钥自动失效；适用于个人用户开发测试；
2. **团队密钥（Team Key / Service Account Key）**：它关联到特定团队，不绑定个人身份，团队内共享资源，用户离开团队不影响密钥有效性；适用于生产服务、CI/CD 流水线、共享服务账户等；
3. **用户+团队密钥（User + Team Key）**：同时关联用户和团队，能定位个人在团队上下文中的身份，同时追踪个人+团队的使用情况，当删除用户时密钥失效；适用于团队成员在团队资源上的个人工作、个人问责制的团队项目等；

### 在 Admin UI 上创建密钥

当我们在 Admin UI 上为用户创建 API Key 时，可以按需选择不同的组合：

![](./images/create-key-user-or-team.png)

或者为团队创建 API Key，这个密钥也被称为 **服务账户密钥**：

![](./images/create-key-service-account.png)

注意，团队密钥在使用时，区分不了用户，LiteLLM 提供了一个可选的配置参数：

```yaml
general_settings:
  service_account_settings: 
    enforced_params: ["user"] # 强制要求所有请求包含 user 参数
```

要求所有通过服务账户的请求都必须包含 `user` 参数，以便进行用户级别的审计。

### 使用接口创建密钥

我们也可以直接使用接口来创建这三种密钥。创建仅用户密钥：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "zhangsan@example.com"
  }'
```

> 注意，这个 `user_id` 不必是系统已有用户，仅仅是一个标记而且。当然，你也可以先在平台上创建一个用户，然后将这里的 `user_id` 换成该用户的 ID。两者的区别在于创建的用户可以登录平台，查看或管理自己的 API Key 等。

创建团队服务账户密钥：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/service-account/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "team_id": "<team_id>"
  }'
```

创建用户+团队密钥：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "zhangsan@example.com",
    "team_id": "<team_id>"
  }'
```

> 注意，这个 `team_id` 必须先在平台上创建团队获得。

## 基于角色的访问控制

了解了上面的层次结构之后，接下来学习 LiteLLM 的权限控制机制。LiteLLM 采用了 **RBAC（基于角色的访问控制）** 模型，这是业界最成熟的权限管理方式之一。RBAC 是一种将权限与角色关联，而不是与用户直接关联的访问控制方法。这种方式的优势在于：

- **简化管理**：不必为每个用户单独分配权限，只需为角色分配权限
- **权限复用**：多个用户可以共享同一个角色
- **动态调整**：调整角色权限即可影响所有相关用户

LiteLLM 定义了两类角色系统：**全局代理角色（Global Proxy Roles）** 和 **组织/团队特定角色（Organization/Team Specific Roles）**，理解这些角色是使用 LiteLLM 权限管理的基础。

### 全局代理角色

全局代理角色又分为 **代理管理员（Proxy Admin）**、**代理查看者（Proxy Admin Viewer）**、**内部用户（Internal User）**、**内部用户查看者（Internal User Viewer）** 四种，这些角色在整个 LiteLLM 平台范围内生效，不受组织或团队边界限制。

#### 代理管理员

这是最高权限角色，控制整个 LiteLLM 平台，只有运行 LiteLLM 实例的人才应该有这个角色：

```
✅ 创建和管理所有组织
✅ 创建和管理所有团队（跨所有组织）
✅ 创建和管理所有用户
✅ 为任何人创建/删除 API 密钥
✅ 查看整个平台的消费成本
✅ 更新团队预算、速率限制
✅ 管理团队成员
```

#### 代理查看者

这是一个只读的管理员角色，可查看所有信息但不能修改，适合财务或审计人员：

```
可以做：
✅ 查看所有组织、团队和用户
✅ 查看整个平台的消费数据
✅ 查看所有 API 密钥信息
✅ 登录到管理面板

不能做：
❌ 创建或删除密钥
❌ 添加或删除用户
❌ 修改预算或速率限制
```

#### 内部用户

这是一般用户角色，拥有基本的操作权限，如管理自己的密钥和查看自己的消费，适用于普通员工：

```
可以做：
✅ 创建和删除自己的 API 密钥（如果允许）
✅ 查看自己的消费成本
✅ 使用 API 密钥进行 LLM 调用

不能做：
❌ 添加新用户
❌ 查看其他用户的信息
❌ 创建或管理团队
```

#### 内部用户查看者

⚠️ **注意**：这个角色已经被新的组织/团队特定角色所取代。建议迁移到更灵活的 `org_admin` 或 `team_admin` 角色。

### 组织/团队特定角色

这些是 LiteLLM 企业版中的角色，提供了更细粒度的权限控制，主要分为 **组织管理员（Org Admin）**、**团队管理员（Team Admin）** 以及 **团队成员（User）** 四种：

#### 组织管理员

该角色拥有特定组织内的所有管理权限，适用于部门主管、组织负责人等：

```
可以做：
✅ 创建团队（在自己的组织内）
✅ 添加用户到团队（在自己的组织内）
✅ 查看组织的消费成本
✅ 为组织内的用户创建 API 密钥

不能做：
❌ 创建其他组织
❌ 修改组织预算和速率限制
❌ 添加全局代理级别的模型
```

#### 团队管理员

该角色拥有特定团队内的所有管理权限，适用于团队负责人，比如项目经理、小组组长、产品负责人等：

```
可以做：
✅ 添加或删除团队成员
✅ 为团队成员创建/删除密钥
✅ 更新团队成员的预算和速率限制
✅ 修改团队设置（预算、速率限制、模型访问）
✅ 配置团队成员权限
✅ 为团队添加自定义模型（如微调模型）

不能做：
❌ 创建新团队
❌ 修改团队的全局预算和速率限制
❌ 访问其他团队的资源
```

#### 团队成员

该角色对应团队内的普通成员，拥有团队内的基础权限，团队管理员可以对团队成员的权限进行精确控制，LiteLLM 支持的权限项包括：

| 权限 | 请求方法 | 描述 |
|------|----------|------|
| `/key/info` | GET | 查看密钥信息 |
| `/key/health` | GET | 检查密钥健康状态 |
| `/key/list` | GET | 列出团队所有密钥 |
| `/key/generate` | POST | 创建新密钥 |
| `/key/service-account/generate` | POST | 创建服务账户密钥 |
| `/key/update` | POST | 修改现有密钥 |
| `/key/delete` | POST | 删除密钥 |
| `/key/regenerate` | POST | 轮换密钥 |
| `/key/block` | POST | 禁用密钥 |
| `/key/unblock` | POST | 启用密钥 |

## 用户管理实操

创建一个名为 XYZ Corp 的组织：

```bash
$ curl -X POST 'http://127.0.0.1:4000/organization/new' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "organization_alias": "XYZ Corp"
  }'
```

得到组织 ID：

```json
{
  "organization_id": "42bea353-4697-4f01-a362-25fd096aeb5a",
  "organization_alias": "XYZ Corp",
  // ...
}
```

为组织创建一个组织管理员：

```bash
$ curl -X POST 'http://127.0.0.1:4000/organization/member_add' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "organization_id": "42bea353-4697-4f01-a362-25fd096aeb5a", 
    "member": {
      "role": "org_admin", 
      "user_id": "desmond@example.com"
    }
  }'
```

注意，该接口会自动在系统中创建一个 `user_id` 为 `desmond@example.com` 的用户，角色为 `org_admin` 组织管理员。

为该用户创建 API Key：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "desmond@example.com"
  }'
```

调用结果如下：

```json
{
  "user_id": "desmond@example.com",
  "key": "sk-xTiqwzA2xJWzac2xk8og7w",
  "key_name": "sk-...og7w",
  // ...
}
```

然后组织管理员就可以通过他的 API Key 去创建团队了：

```bash
$ curl -X POST 'http://127.0.0.1:4000/team/new' \
  -H 'Authorization: Bearer sk-xTiqwzA2xJWzac2xk8og7w' \
  -H 'Content-Type: application/json' \
  -d '{
    "team_alias": "engineering_team",
    "organization_id": "42bea353-4697-4f01-a362-25fd096aeb5a"
  }'
```

得到团队 ID：

```json
{
  "team_alias": "engineering_team",
  "team_id": "36100710-1fb1-4d6a-abd7-1fda8d171771",
  "organization_id": "42bea353-4697-4f01-a362-25fd096aeb5a",
  // ...
}
```

组织管理员可以为团队创建一个团队管理员：

```bash
$ curl -X POST 'http://127.0.0.1:4000/team/member_add' \
  -H 'Authorization: Bearer sk-xTiqwzA2xJWzac2xk8og7w' \
  -H 'Content-Type: application/json' \
  -d '{
    "team_id": "36100710-1fb1-4d6a-abd7-1fda8d171771", 
    "member": {
      "role": "admin", 
      "user_id": "stonie@example.com"
    }
  }'
```

同样的，该接口会自动在系统中创建一个 `user_id` 为 `stonie@example.com` 的用户，角色为 `admin` 团队管理员。

也为该用户创建 API Key：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "stonie@example.com"
  }'
```

调用结果如下：

```json
{
  "user_id": "stonie@example.com",
  "key": "sk-jhSg1qFKYEIg8ndYmmmFHg",
  "key_name": "sk-...mFHg",
  // ...
}
```

> 这里看官方文档，应该使用组织管理员的 API Key 去生成团队管理的 API Key，但是我在测试时报错 `User can only create keys for themselves`，因此使用了代理管理员的 API Key。

团队管理员可以添加或移除团队成员、修改团队的预算和费率限制、配置团队成员的权限等，下面是添加成员的接口示例：

```bash
$ curl -X POST 'http://127.0.0.1:4000/team/member_add' \
  -H 'Authorization: Bearer sk-jhSg1qFKYEIg8ndYmmmFHg' \
  -H 'Content-Type: application/json' \
  -d '{
    "team_id": "36100710-1fb1-4d6a-abd7-1fda8d171771", 
    "member": {
      "role": "user", 
      "user_id": "zhangsan@example.com"
    }
  }'
```

为该用户生成 API Key：

```bash
$ curl -X POST 'http://127.0.0.1:4000/key/generate' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "zhangsan@example.com",
    "team_id": "36100710-1fb1-4d6a-abd7-1fda8d171771"
  }'
```

调用结果如下：

```json
{
  "user_id": "zhangsan@example.com",
  "key": "sk-If8su0G3z3GlgwaA6acpLg",
  "key_name": "sk-...cpLg",
  // ...
}
```

> 这里看官方文档，应该使用团队管理员的 API Key 去生成用户的 API Key，但是我在测试时报错 `User can only create keys for themselves`，因此使用了代理管理员的 API Key。

## 用户自助服务

上面创建的这些用户，无论是组织管理员、团队管理员还是团队用户，目前都无法登录平台，只能通过 API Key 来进行管理操作，这是相当繁琐的。LiteLLM 支持用户自助服务，它让用户可以在不依赖管理员的情况下管理自己的密钥和查看使用情况。

首先，为他们生成邀请链接：

```bash
$ curl -X POST 'http://127.0.0.1:4000/invitation/new' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "desmond@example.com"
  }'
```

该接口生成的是邀请 ID：

```json
{
  "id": "35186fe0-5b96-4e75-a285-f17fbf3add0d",
  "user_id": "desmond@example.com",
  // ...
}
```

将邀请 ID 拼接到 `http://127.0.0.1:4000/ui?invitation_id=` 后面，得到类似下面的链接地址：

```
http://127.0.0.1:4000/ui?invitation_id=35186fe0-5b96-4e75-a285-f17fbf3add0d
```

将链接地址发送给用户，他就可以登录平台了：

![](./images/invitation-link.png)

登录平台后，根据用户的角色，展示的菜单也不一样。比如普通用户可以查看或创建自己的 API Key：

![](./images/user-login.png)

注意上面的邮箱地址是空的，虽然也能登录，但是下次用户再登录时就麻烦了（需要管理员编辑用户邮箱）。可以使用下面的接口来创建用户，为用户设置邮箱地址：

```bash
$ curl -X POST 'http://127.0.0.1:4000/user/new' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_email": "stonie@example.com",
    "user_role": "internal_user"
  }'
```

这个接口在创建用户的同时也会为其创建一个 API Key：

```json
{
  "user_id": "72f9e797-0e9a-41f5-a227-03a8a813c7cc",
  "key": "sk-EIKmPPTyBriwpCW1NYV8aw",
  "key_name": "sk-...V8aw",
  "user_email": "stonie@example.com",
  "user_role": "internal_user",
  // ...
}
```

然后使用该用户的 ID 来生成邀请链接：

```bash
$ curl -X POST 'http://127.0.0.1:4000/invitation/new' \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "72f9e797-0e9a-41f5-a227-03a8a813c7cc"
  }'
```

之后用户就可以通过邮箱登录平台了。

## 小结

通过这篇文章，我们系统地学习了 LiteLLM 的用户管理体系，主要内容包括：

- **多层次管理架构**：从组织 → 团队 → 用户的三层结构，组织层用于大型企业的多租户隔离，团队层用于项目组的资源共享和协作，用户层用于个人开发者的独立预算和追踪；
- **灵活的权限控制**：支持代理管理员、代理查看者、内部用户等全局代理角色，以及组织管理员、团队管理员、普通成员等组织/团队特定角色，还可以精确地控制每个用户能执行的操作；
- **用户自助服务**：支持为用户生成邀请链接，允许用户在不依赖管理员的情况下管理自己的密钥和查看使用情况；

在下一篇文章中，我们将学习 LiteLLM 的 **访问控制机制**，包括如何为不同的用户和团队分配不同的模型访问权限，如何设置和执行流量控制策略，以及如何进行成本预算管理和预警。这是用户管理体系的延伸和深化，将帮助我们构建一个完整的 LLM 网关安全体系。敬请期待！

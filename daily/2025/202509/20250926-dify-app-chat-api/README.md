# 梳理 Dify 应用的会话接口

在前面的文章中，我们学习了 Dify 的代码结构和路由系统，了解了 Dify 是如何通过 Flask Blueprint 和 Flask-RESTX 来组织其复杂的 API 架构的。今天，我们将深入探索 Dify 应用的会话 API 接口，分析其具体的实现细节，并结合我们之前学习的内容，看看不同蓝图下的实现以及各自的区别。

## 五种应用 + 三大蓝图

我们知道，Dify 有五种不同的应用类型：

```python
class AppMode(StrEnum):
  # 聊天助手
  CHAT = "chat"
  # 文本生成
  COMPLETION = "completion"
  # 智能体
  AGENT_CHAT = "agent-chat"
  # 工作流
  WORKFLOW = "workflow"
  # 对话流
  ADVANCED_CHAT = "advanced-chat"
```

不同的应用类型对应不同的会话接口，而根据应用的调用方式，这些会话接口又会出现在不同的蓝图下。因此 Dify 的会话接口有很多，如果第一次接触源码的话会很懵。会话接口主要分布在三个蓝图下：

- **Console 蓝图**：从管理控制台调用，又分为从工作室的预览调试和探索的已发布应用两个地方调用，接口统一以 `/console/api` 为前缀
- **Web 蓝图**：从前端的 Web 应用调用，Dify 会为每个应用生成一个公开可访问的页面，这个页面的调用统一以 `/api` 为前缀
- **Service API 蓝图**：第三方通过 HTTP API 或 SDK 集成调用，接口以 `/v1` 为前缀

不同蓝图下虽然接口各异，但都实现了相同的核心功能，它们只是在认证方式和用户类型上有所区别，为不同的使用场景提供最合适的调用方式。下面就来对每个蓝图下的会话接口逐一分析。

### Console 蓝图

当我们在 “工作室” 的预览页面对应用进行调试时：

![](./images/apps.png)

调用下面这些接口：

```python
# 文本生成
api.add_resource(
  CompletionMessageApi, 
  "/apps/<uuid:app_id>/completion-messages"
)
# 聊天助手 或 Agent 应用
api.add_resource(
  ChatMessageApi, 
  "/apps/<uuid:app_id>/chat-messages"
)
# 对话流
api.add_resource(
  AdvancedChatDraftWorkflowRunApi, 
  "/apps/<uuid:app_id>/advanced-chat/workflows/draft/run"
)
# 工作流
api.add_resource(
  DraftWorkflowRunApi, 
  "/apps/<uuid:app_id>/workflows/draft/run"
)
```

我们还可以在 “探索” 中打开应用：

![](./images/explore.png)

此时调用接口如下：

```python
# 文本生成
api.add_resource(
  CompletionApi, 
  "/installed-apps/<uuid:installed_app_id>/completion-messages", 
  endpoint="installed_app_completion"
)
# 聊天助手、Agent 应用 或 对话流
api.add_resource(
  ChatApi, 
  "/installed-apps/<uuid:installed_app_id>/chat-messages", 
  endpoint="installed_app_chat_completion"
)
# 工作流
api.add_resource(
  InstalledAppWorkflowRunApi, 
  "/installed-apps/<uuid:installed_app_id>/workflows/run"
)
```

Console 蓝图下的对话接口最大特点是 URL 上带有 `app_id` 参数，接口直接对该应用发起会话即可。另外，这个蓝图下的接口主要面向平台用户，需要对用户进行登录认证，所以接口的实现上都带有 `@login_required` 装饰器：

```python
class ChatMessageApi(Resource):
  @setup_required
  @login_required
  @account_initialization_required
  @get_app_model(mode=[AppMode.CHAT, AppMode.AGENT_CHAT])
  def post(self, app_model):
    # ...
```

### Web 蓝图

在应用的配置页，我们可以将应用发布成 Web 应用：

![](./images/web.png)

该功能默认开启，会自动生成一个能够在互联网上公开访问的网址。Web 应用的页面适配了不同尺寸的设备，包括 PC，平板和手机，使用者无需登陆，即可使用。当用户通过 Web 应用页面和助手对话时：

![](./images/web-2.png)

调用的接口如下：

```python
# 文本生成
api.add_resource(CompletionApi, "/completion-messages")
# 聊天助手、Agent 应用 或 对话流
api.add_resource(ChatApi, "/chat-messages")
# 工作流
api.add_resource(WorkflowRunApi, "/workflows/run")
```

Dify 还支持将你的 Web 应用嵌入到业务网站中，你可以在几分钟内制作具有业务数据的官网 AI 客服、业务知识问答等应用：

![](./images/web-iframe.png)

Dify 提供了 3 种不同的嵌入方式，分别为：

- **`<iframe>` 标签方式**：将 `<iframe>` 代码复制到你网站用于显示 AI 应用的标签中，如 `<div>`、`<section>` 等标签
- **`<script>` 标签方式**：将 `<script>` 代码复制到你网站 `<head>` 或 `<body>` 标签中，这会在你的网站上显示一个 Dify 聊天机器人气泡按钮
- **安装 Dify Chrome 浏览器扩展方式**：前往 Chrome 应用商店，安装 [Dify Chatbot](https://chromewebstore.google.com/detail/dify-chatbot/ceehdapohffmjmkdcifjofadiaoeggaf) 扩展即可

> Web 应用的嵌入有不少高级技巧，比如自定义聊天机器人的气泡按钮，向 Web 应用传值，甚至可以基于前端模板对 Web 应用进行二次开发。

当用户通过这些方式访问我们的应用时，都统一使用 Web 蓝图下的接口。这个蓝图下的会话接口有着完善的接口文档：

```python
class ChatApi(WebApiResource):
  @api.doc("Create Chat Message")
  @api.doc(description="Create a chat message for conversational applications.")
  @api.doc(
    params={
      "inputs": {"description": "Input variables for the chat", "type": "object", "required": True},
      "query": {"description": "User query/message", "type": "string", "required": True},
      "files": {"description": "Files to be processed", "type": "array", "required": False},
      "response_mode": {
        "description": "Response mode: blocking or streaming",
        "type": "string",
        "enum": ["blocking", "streaming"],
        "required": False,
      },
      "conversation_id": {"description": "Conversation UUID", "type": "string", "required": False},
      "parent_message_id": {"description": "Parent message UUID", "type": "string", "required": False},
      "retriever_from": {"description": "Source of retriever", "type": "string", "required": False},
    }
  )
  @api.doc(
    responses={
      200: "Success",
      400: "Bad Request",
      401: "Unauthorized",
      403: "Forbidden",
      404: "App Not Found",
      500: "Internal Server Error",
    }
  )
  def post(self, app_model, end_user):
    # ...
```

值得注意的是，这个接口没有 `app_id` 参数，那么 Dify 是怎么区分用户是在和哪个应用进行对话呢？答案在于 `WebApiResource` 这个父类：

```python
class WebApiResource(Resource):
  method_decorators = [validate_jwt_token]
```

`WebApiResource` 继承自 Flask-RESTX 的 `Resource` 类，`method_decorators` 是该类的一个属性，用于为资源类中的所有 HTTP 方法自动应用装饰器。Dify 在这里定义了一个 `validate_jwt_token` 装饰器，对 Web 蓝图下的接口验证 JWT 令牌，从而得到应用信息。

Web 应用的访问地址一般是 `http://ip:port/chat/{app_code}`，当用户第一次访问 Web 应用时，会调用 `api/passport` 接口，通过 HTTP 请求头 `X-App-Code` 创建一个 JWT 令牌，后续对话时都会带上这个令牌。

### Service API 蓝图

Dify 基于 **后端即服务** 理念为所有应用提供了 API 接口，为应用开发者带来了诸多便利。可以在应用配置页开启：

![](./images/api.png)

Dify 为每个应用提供了详尽的接口文档：

![](./images/api-2.png)

同时 Dify 还提供了多语言的 SDK，包括 [Python](https://github.com/langgenius/dify/tree/main/sdks/python-client)、[PHP](https://github.com/langgenius/dify/tree/main/sdks/php-client)、[Node.js](https://github.com/langgenius/dify/tree/main/sdks/nodejs-client)、[Java](https://github.com/langgenius/java-client/)、[Go](https://github.com/langgenius/dify-sdk-go)、[Ruby](https://github.com/langgenius/ruby-sdk)，方便开发者在不同技术栈中集成 Dify 的能力。

通过 API 访问的接口如下：

```python
# 文本生成
@service_api_ns.route("/completion-messages")
class CompletionApi(Resource):

# 聊天助手、Agent 应用 或 对话流
@service_api_ns.route("/chat-messages")
class ChatApi(Resource):

# 工作流
@service_api_ns.route("/workflows/run")
class WorkflowRunApi(Resource):
```

不过要访问这些 API 接口，我们得先创建 API 密钥，可以点击文档页面右上角的 “API 密钥” 按钮创建。然后按照接口文档，发送请求如下：

```sh
curl -X POST 'http://localhost:5001/v1/chat-messages' \
  --header 'Authorization: Bearer app-cSZlATg5dglJSxVLLaJoXkgX' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "inputs": {},
    "query": "本是同根生，相煎何太急",
    "response_mode": "blocking",
    "user": "abc-123"
  }'
```

得到应用的响应如下：

```json
{
  "event": "message",
  "task_id": "e705b358-5a75-4fc4-9dfe-c8bbc8095be7",
  "id": "005f66cf-08eb-4aac-9f19-3a6255ecdb66",
  "message_id": "005f66cf-08eb-4aac-9f19-3a6255ecdb66",
  "conversation_id": "5cd66e81-05fd-4a11-8596-586258653213",
  "mode": "chat",
  "answer": "Being born from the same root, why rush to fry each other to death?",
  "metadata": {
    "annotation_reply": null,
    "retriever_resources": [],
    "usage": {
      "prompt_tokens": 63,
      "prompt_unit_price": "5",
      "prompt_price_unit": "0.000001",
      "prompt_price": "0.000315",
      "completion_tokens": 17,
      "completion_unit_price": "15",
      "completion_price_unit": "0.000001",
      "completion_price": "0.000255",
      "total_tokens": 80,
      "total_price": "0.00057",
      "currency": "USD",
      "latency": 2.1960244579822756
    }
  }
}
```

很明显，Service API 蓝图下的接口要实现 API 密钥的认证：

```python
class ChatApi(Resource):
  @service_api_ns.expect(chat_parser)
  @service_api_ns.doc("create_chat_message")
  @service_api_ns.doc(description="Send a message in a chat conversation")
  @service_api_ns.doc(
    responses={
      200: "Message sent successfully",
      400: "Bad request - invalid parameters or workflow issues",
      401: "Unauthorized - invalid API token",
      404: "Conversation or workflow not found",
      429: "Rate limit exceeded",
      500: "Internal server error",
    }
  )
  @validate_app_token(fetch_user_arg=FetchUserArg(fetch_from=WhereisUserArg.JSON, required=True))
  def post(self, app_model: App, end_user: EndUser):
    # ...
```

当我们创建 API 密钥时，Dify 会将 API 密钥和 `app_id` 保存到数据库中，然后用户调用 API 接口时，必须传入 API 密钥，接口通过 `@validate_app_token` 从数据库中获取 API 密钥对应的应用信息。

## 小结

今天我们主要对 Dify 的会话接口做了一个简单的梳理，学习了 Dify 应用的不同访问方式以及各自蓝图下的接口定义，它们之间的差异对比如下：

| 蓝图 | 认证方式 | 装饰器 | 用户类型 |
|------|---------|-------|----------|
| Console | Session | `@login_required` | Account（开发者） |
| Web | JWT Token | `WebApiResource` 基类处理 | EndUser（终端用户），来自浏览器 |
| Service API | API Key | `@validate_app_token` | EndUser（终端用户），来自 API |

在下一篇文章中，我们将继续研究会话接口的源码，来具体看下不同应用的会话是如何实现的。

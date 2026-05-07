# 让外部世界唤醒小龙虾：Webhook 与 Standing Orders

昨天我们让小龙虾装上了发条：Cron 负责按精确时间表干活，Heartbeat 负责主会话隔一会儿自己醒一下。但这两个机制都有一个共同的盲点 —— 它们都是 **基于时间** 的，外部世界发生了什么，它得等下一轮触发才知道。GitHub PR 来了新的 review、Sentry 报了 P0、自家服务部署完成 —— 这些事件都是不规律的，靠 Cron 拉不到，靠 Heartbeat 也只能 30 分钟才看一眼。要让小龙虾能在事件发生的当下立刻响应，得给它再开一道入口：**Webhook**。

光有 Webhook 入口还不够。Cron job 的 `--message` 字段我们见识过了，每次都得把"做什么、按什么规则做、什么情况要升级"重新抄一遍，写多了既冗余又难维护。OpenClaw 给出的方案叫 **Standing Orders**，把 agent 的常驻授权和边界集中写在 workspace 的 `AGENTS.md` 文件里，每次 session 启动都自动加载。Cron job 只需要写一句 "按 standing orders 执行 X 职责块" 即可。

今天我们就把这两块拼起来。

## Webhook、Cron 与 Standing Orders 的分工

动手之前先把三者的边界用一张表讲清楚：

| 机制              | 触发条件                                                             | 职责                  | 典型场景                              |
| --------------- | ---------------------------------------------------------------- | ------------------- | --------------------------------- |
| Cron            | 时间到了（`--at` / `--every` / `--cron`） | 决定 **什么时候** 执行       | 早报、周报、定时提醒                        |
| Standing Orders | 每次 session 启动时自动加载                                        | 决定 **能做什么、不能做什么**   | 授权范围、approval gate、escalation 规则  |
| Webhook         | 外部 HTTP POST 进来                                                  | 决定 **被谁** 唤起        | GitHub 发版、Sentry 告警、Gmail 新邮件     |

文档里有一句话很到位：standing orders 定义 agent **能做什么**，cron jobs 定义 **什么时候** 做，完整的自动化方案往往是两者组合，用 standing orders 把日报这件事的范围、步骤、边界写清楚，再让 cron 在 8:30 把它拉起来执行。而 Webhook 则是补上 **被谁** 唤起这条入口，比如遇到 GitHub 发版这种关键事件时，再通过 webhook 临时插一脚。

> 注意：OpenClaw 中有两种 hook 概念：一种是 **内部 hook**，是 Gateway 在 `/new` `/reset` `/stop` `agent:bootstrap` 这类 **生命周期事件** 上挂的脚本，跟外部 HTTP 没关系；今天我们说的 **Webhook** 是外部 HTTP 入口，响应外部世界的事件。

## Webhook：让外部事件唤起小龙虾

OpenClaw 的 webhook 默认是 **关** 的，要在 Gateway 配置里显式打开。编辑 `~/.openclaw/openclaw.json`，加一段 `hooks` 块：

```json5
{
  "hooks": {
    "enabled": true,
    "token": "shared-secret-replace-me",
    "path": "/hooks",
    "allowedAgentIds": [
      "main"
    ],
    "allowRequestSessionKey": false
  },
}
```

每个字段的含义：

* `enabled`：总开关，必须显式置为 `true`
* `token`：共享密钥，所有进来的请求必须带，**长度足够强随机**，别复用 Gateway 自身的 auth token
* `path`：endpoint 前缀，默认 `/hooks`，**裸根路径 `/` 会被拒绝**
* `allowedAgentIds`：限制可以被显式路由到的 agent ID，默认不限制
* `allowRequestSessionKey`：是否允许调用方自己塞 session key 进来，默认 `false`

启用之后 Gateway 在 `127.0.0.1:18789`（默认）会暴露三个入口：

| 入口                   | 作用                                                                 |
| -------------------- | ------------------------------------------------------------------ |
| `POST /hooks/wake`   | 给 main session 塞一条 system event，相当于戳一下小龙虾让它注意到某件事，可选 `next-heartbeat` 或 `now` |
| `POST /hooks/agent`  | 直接拉起一次 isolated agent turn，等价于一次性的 `cron run`                       |
| `POST /hooks/<name>` | 自定义路径，通过 `hooks.mappings` 把任意 payload 映射成上面两种之一                      |

熟悉的同学可能已经看出来了：这两个入口实际上就是上一篇里 `--system-event` 和 `--message` 那对参数的 HTTP 版本。`/hooks/wake` 走系统事件 + 可选 heartbeat 唤醒，跟 `--session main --system-event` 同源；`/hooks/agent` 构造一个隔离的一次性 job，跟 `--session isolated --message` 同源。

### 鉴权方式

每个进来的请求都必须携带 token，OpenClaw 支持两种 header 形式：

```
Authorization: Bearer <token>
x-openclaw-token: <token>
```

**查询字符串里的 token 一律拒绝**，这是为了防止 token 泄露在反代或 Web Server 的访问日志里。

### 用 curl 模拟一次调用

最简单的验证方式是在本机起一下 curl。先用 wake 端点戳一下：

```
$ curl -X POST http://127.0.0.1:18789/hooks/wake \
    -H 'Authorization: Bearer shared-secret-replace-me' \
    -H 'Content-Type: application/json' \
    -d '{"text":"GitHub 上 v0.42 已发版","mode":"now"}'

{"ok":true,"mode":"now"}
```

`text` 是给 agent 看的事件描述（必填），`mode` 取 `now` 立刻起一次心跳，`next-heartbeat` 等下一轮 tick 再跑。

再试一下 agent 端点，让它直接跑一段独立任务：

```
$ curl -X POST http://127.0.0.1:18789/hooks/agent \
    -H 'Authorization: Bearer shared-secret-replace-me' \
    -H 'Content-Type: application/json' \
    -d '{
      "message":"刚刚 GitHub 上发版了 v0.42，将通知发到 Telegram",
      "name":"release-translate",
      "deliver":"announce",
      "channel":"telegram",
      "to":"7112345678"
    }'

{"ok":true,"runId":"b73a2e76-f635-4218-888a-4b7e5f8ccc02"}
```

`/hooks/agent` 接受的字段比 `wake` 丰富很多：`message` 必填，可选项包括 `name`、`agentId`、`wakeMode`、`deliver`、`channel`、`to` 等。基本上 `cron add --session isolated` 能用的参数，这里都能在请求里指定。发送完成后，稍等片刻，我的 Telegram 就收到了一条消息：

![](./images/hooks-telegram.png)

### Mapped hooks：让 payload 自动落位

直接调 `/hooks/agent` 自己手写 payload 当然也能用，但当你要对接 GitHub Webhook 这种格式固定的外部服务时，每次都让对方帮你按 OpenClaw 的格式打包很不现实 —— 它发的是它自己那一套。比如 GitHub 在每次发版（`release.published` 事件）时 POST 过来的 payload 大致长这样（完整 schema 见 [GitHub Webhook events and payloads 文档](https://docs.github.com/en/webhooks/webhook-events-and-payloads#release)）：

```json
{
  "action": "published",
  "release": {
    "id": 123456789,
    "tag_name": "v0.42",
    "name": "v0.42 — Bug fixes & perf",
    "body": "## What's Changed\n* Fix cron timer drift by @alice in #421\n* Reduce heartbeat token usage by @bob in #423\n...",
    "html_url": "https://github.com/owner/repo/releases/tag/v0.42",
    "draft": false,
    "prerelease": false,
    "published_at": "2026-05-06T08:30:00Z",
    "author": { "login": "alice", "id": 1, "...": "..." }
  },
  "repository": {
    "id": 987654321,
    "name": "repo",
    "full_name": "owner/repo",
    "html_url": "https://github.com/owner/repo",
    "...": "..."
  },
  "sender": { "login": "alice", "...": "..." }
}
```

字段嵌套很深，但这次场景里我们真正想塞进 prompt 的就那么几个：`repository.full_name`、`release.tag_name`、`release.name`、`release.html_url`、`release.body`。OpenClaw 提供了 `hooks.mappings` 配置项，让你能把任意自定义路径绑定到一段字符串模板上，按需把这些字段挑出来渲染成 prompt：

```json5
{
  "hooks": {
    "enabled": true,
    "token": "shared-secret-replace-me",
    "path": "/hooks",
    "mappings": [
      {
        "id": "github-release",
        "match": {
          "path": "github-release"
        },
        "action": "agent",
        "wakeMode": "now",
        "name": "GitHub release notify",
        "messageTemplate": "新版本：{{body.repository.full_name}} {{body.release.tag_name}}\n标题：{{body.release.name}}\n链接：{{body.release.html_url}}\n\n请把 release notes 翻译成中文，挑出对用户可见的变化，附上原始链接，发到 Telegram。",
        "deliver": true,
        "channel": "telegram",
        "to": "7112345678"
      }
    ],
  },
}
```

加了这段之后，外部系统 POST 到 `/hooks/github-release`，OpenClaw 就会按 `messageTemplate` 把 GitHub 的原始 payload 渲染成 prompt，再走一次 isolated agent turn，最后通过 `announce` 兜底投递到 Telegram。

> 字符串模板搞不定的复杂转换（比如签名校验、字段过滤、跨字段拼接）可以走 `transform` 字段：指向 `hooks.transformsDir` 下的一个本地 JS/TS 模块，对 payload 做编程式改写后再交给 agent。这块官方文档中介绍的不多，本文不展开，感兴趣的同学可以研究下 OpenClaw 的源码。

### 把 webhook 暴露到公网

本地 Gateway 默认只监听 `127.0.0.1:18789`，外部根本访问不到。要让 GitHub、Sentry 这些公网服务能调用，常用的方法有：

| 方案                      | 适用场景                                  |
| ----------------------- | ------------------------------------- |
| `ngrok http 18789`      | 开发调试最快的方式，一条命令出公网 HTTPS 隧道；免费版有连接数限制   |
| `cloudflared tunnel`    | Cloudflare 出品，速度稳，绑自有域名免费              |
| Tailscale Funnel        | OpenClaw 的 Gmail PubSub 集成就是用它做的官方推荐方案 |
| Fly.io / Railway 部署     | 生产环境，把 Gateway 整个搬到云上                   |

本机调试最快的就是 ngrok：

```
$ ngrok http 18789
```

运行结果如下：

![](./images/ngrok.png)

拿到 ngrok 给的 HTTPS 地址，把 `https://xxx.ngrok-free.app/hooks/github-release` 填回 GitHub 仓库的 **Settings → Webhooks** 就能联调。Content type 选 `application/json`，Events 勾上 `Releases`：

![](./images/github-settings.png)

完成配置之后，每当仓库发一个新版本时，我们就可以在 Telegram 上收到 agent 的通知了。

> [ngrok](https://ngrok.com/) 是一个反向 HTTP 隧道工具，可以免费使用，运行 `ngrok http <port>` 之后会拿到一个 `https://xxx.ngrok-free.app` 临时域名，把外部 HTTPS 请求加密反向转发到本机端口。不过要注意的是，免费版每次重启 URL 都会变、还有速率限制，本地调试用用还行，正式跑生产建议换 Tailscale Funnel 或 Cloudflare Tunnel。

## Standing Orders：常驻授权与边界

讲完外部入口，再来看常驻指令。Standing orders 不是被时间或事件触发的，它是 agent **每次进入一个 session** 时都会自动加载的一份常驻文件 —— 用户在 Telegram 私聊、cron 拉起的隔离 session、webhook 触发的 agent turn、heartbeat 主会话，都会加载。本质上它就是一段 Markdown，在 session 启动时被注入到 system prompt 里。

### 它是怎么生效的

OpenClaw 在 `src/agents/workspace.ts` 里给 workspace 定义了一组启动注入文件名：

```ts
export const DEFAULT_AGENTS_FILENAME = "AGENTS.md";
export const DEFAULT_SOUL_FILENAME = "SOUL.md";
export const DEFAULT_TOOLS_FILENAME = "TOOLS.md";
export const DEFAULT_IDENTITY_FILENAME = "IDENTITY.md";
export const DEFAULT_USER_FILENAME = "USER.md";
export const DEFAULT_HEARTBEAT_FILENAME = "HEARTBEAT.md";
export const DEFAULT_BOOTSTRAP_FILENAME = "BOOTSTRAP.md";
export const DEFAULT_MEMORY_FILENAME = CANONICAL_ROOT_MEMORY_FILENAME;
```

每次 session 启动时，OpenClaw 会按这份名单去 workspace 目录读文件；再由 `src/agents/pi-embedded-helpers.ts` 里的 `buildBootstrapContextFiles` 把这些文件的内容封装成 embedded context 注入到首轮上下文。**`AGENTS.md` 就是 Standing orders 的载体**，写在里面的内容每次开局都会被 agent 看到。

### 一份完整的职责块

知道了 `AGENTS.md` 是 Standing orders 的载体，下一个问题是：往里面写什么？

理论上你可以塞任何 Markdown，agent 都能读到。但实战中如果只是丢一句"你负责回答群里关于发版的问题"，遇到边界场景 agent 就容易犯傻 —— 比如有人问的根本不是发版而是部署，或者跑了几轮之后 agent 自己脑补出一些你压根没授权它做的动作。

为了把"在哪条边界内做事"讲清楚，OpenClaw 文档推荐了一种结构化模板，叫做 **Program**（本文统一译作 **职责块**）。每个职责块至少包含下面四个字段：

* **Authority**：授权范围 —— 这个职责块允许 agent 做什么
* **Trigger**：触发条件 —— 什么时候才轮到这个职责块上场
* **Approval gate**：审批门槛 —— 哪些动作要先经过人确认才能执行
* **Escalation**：升级规则 —— 出错或越界时停在哪、报告给谁

四个字段之外可以按需加 `Execution steps`（具体步骤）、`What NOT to do`（明确禁止）等扩展段落，给 agent 进一步收紧执行边界。

> **特别注意**：OpenClaw **不会** 按 `Program:` / `Authority:` / `Trigger:` 这些字段做任何特殊解析。所有 markdown 都是整段被注入到 system prompt 里。这套结构纯粹是 **写作约定**，目的是逼着写作者把每个职责的边界、触发条件、审批门槛、升级路径都想清楚。

下面是一个完整的群内答疑职责块，专门负责回答上线状态的问题：

```markdown
## Program: 上线状态答疑

**Authority:** 在团队群里回答关于版本发布状态的问题
**Trigger:** 群成员的消息里出现"上线了吗"、"发布了没"、"最新版本是什么"等关键词
**Approval gate:** 无（只读操作）
**Escalation:** 如果 GitHub API 连续 2 次返回 4xx/5xx，停止回答并提醒 @oncall

### Execution steps

1. 调用 github 工具查询当前仓库最新发版的 tag 和 published_at
2. 对比当前用户问到的版本号或语义（"昨天的"、"v0.42"、"最新一版"）
3. 用一句话回过去，附上发版链接
4. 如果命中需要回答的问题但仓库还没发过版，直接说"还没上线"

### What NOT to do

- 不要主动催促开发者发布
- 不要在群里贴完整的 changelog，只贴链接
- 不要回答与发版状态无关的问题
```

把这段直接追加到 workspace 的 `AGENTS.md` 末尾，下次 agent 进入 session 时，这段职责块就会自动出现在 system prompt 里。

### Execute-Verify-Report

Standing orders 文档里反复强调一个执行纪律：每个 task 都要走 **Execute → Verify → Report** 三步。原文如下：

```markdown
- 每个任务都必须走 Execute-Verify-Report 三步，没有例外。
- "我这就去做"不算执行。先做，再汇报。
- 没有经过验证就说"完成了"是不允许的。拿出证据。
- 执行失败：调整思路重试一次。
- 还失败：带诊断信息汇报失败。绝不静默失败。
- 不要无限重试 —— 最多 3 次，然后升级处理。
```

这套规则是用来对抗 LLM 最常见的"假执行"失败模式：agent 答应你"好的我去做"，但其实只是把 prompt 复读了一遍。把这段写进 `AGENTS.md` 顶部，配合具体的职责块，能显著降低这种失败概率。

我自己的写法是把 Execute-Verify-Report 块单独放在 `AGENTS.md` 最上面，所有职责块共享，下面再按职责块一条条列下来。这样每次新写一个职责块，只用关注 Authority/Trigger/Approval gate/Escalation 这四块，执行纪律不需要重复抄。

### 跟 cron 配合使用

看到这里读者可能会感到疑惑：Standing orders 跟 cron **不是绑定关系**，它对所有 session 都生效，为什么官方将其归在 Automation and tasks 分类下呢？我想可能是因为 cron 是它最受益的一个场景，由于 cron job 之间没有上下文记忆，每条 `--message` 都得自带边界，写多了既冗余又难维护。把边界沉淀进 `AGENTS.md` 之后，cron 的 `--message` 退化成一句话："按 standing orders 执行 X 职责块"，剩下的全交给常驻文件。官方文档给的例子就是这个分工：

> Standing Order："你负责每天的收件箱整理" → 
> Cron Job（每天早 8 点）："按 standing orders 执行收件箱整理" → 
> Agent：读取 standing orders → 执行步骤 → 汇报结果

这套分工的好处是 **改职责块的执行细节不用动 cron，改投递目标不用动职责块** —— "做什么、按什么规则做" 写在 `AGENTS.md` 里，"什么时候做、做完发到哪" 写在 cron 里，两层职责清晰。同样的分工逻辑也适用于 webhook：mapping 里的 `messageTemplate` 也只需要写一句"按 X 职责块处理 {{body}}"，业务规则不用复制。

## 把三件事拼起来：自动发布通知

前面 Mapped hooks 那一节其实已经把 GitHub 发版通知跑通了一遍，但那时候业务规则（翻译要求、字数限制、不该做啥）全塞在 `messageTemplate` 里，每加一条规则 mapping 配置就长一行。这一节我们把这个用例重构下，整套方案分三层：

1. **Standing order**：在 `AGENTS.md` 里定义 release-notify 程序，划清"翻译 release notes、挑出用户可见的变化、附上原文链接、发到 Telegram"这件事的边界
2. **Webhook**：通过 `hooks.mappings` 把 `/hooks/github-release` 路径映射到 agent turn，messageTemplate 里只写"按 release-notify 程序处理 {{body}}"
3. **Cron**：每天 22:00 跑一次 release roundup，把当天所有发版汇总成一段周报，预防 webhook 漏推

`AGENTS.md` 里的职责块：

```markdown
## Program: Release notify

**Authority:** 把外部系统推过来的发版事件翻译并转发给团队
**Trigger:** /hooks/github-release 被外部系统调用 OR cron release-roundup 拉起
**Approval gate:** 无（公开内容，只读操作）
**Escalation:** 如果连续 3 次发版都译不出 changelog，停止并提醒 @oncall

### Execution steps

1. 解析 payload，拿到 repo、tag、release notes 原文
2. 用中文翻译 release notes，重点抓：新功能、Breaking change、Bug fix、Deprecation
3. 不超过 500 字，超长则压缩到三个分类各 5 条以内
4. 通过 message 工具发到 Telegram

### What NOT to do

- 不翻译纯依赖升级的内容（Bump deps from x to y 这种）
- 不要把发版链接里 hash 后面的 query string 复制过来
- 不在群里 @ 任何人
```

webhook mapping 配置如下：

```json5
{
  "hooks": {
    "enabled": true,
    "token": "shared-secret-replace-me",
    "path": "/hooks",
    "allowedAgentIds": ["main"],
    "mappings": [
      {
        "id": "github-release",
        "match": { "path": "github-release" },
        "action": "agent",
        "wakeMode": "now",
        "name": "Release notify (push)",
        "messageTemplate":
          "按 release-notify 程序处理这次发版：repo={{body.repository.full_name}} tag={{body.release.tag_name}} url={{body.release.html_url}}\n\n--- 原始 release notes ---\n{{body.release.body}}",
        "deliver": true,
        "channel": "telegram",
        "to": "7112345678",
      },
    ],
  },
}
```

然后再创建一个 cron 兜底（防止 webhook 漏推一天里某次发版）：

```
$ openclaw cron add \
    --name "Release roundup" \
    --cron "0 22 * * *" \
    --tz "Asia/Shanghai" \
    --session isolated \
    --message "按 release-notify 程序处理今天 24 小时内 GitHub 上所有关注仓库的发版，去重后汇总发到 Telegram。" \
    --announce \
    --channel telegram \
    --to "7112345678" \
    --timeout-seconds 300
```

整体的事件链长这样：

![](./images/example.png)

跑通之后，仓库一发版，几秒钟内 Telegram 就会冒出一条结构化通知；webhook 万一漏了，晚上 22:00 还有一次 cron 兜底。这两个入口都不需要重复 release-notify 程序的细节，改翻译规则只用动 `AGENTS.md`，改投递目标只用动 cron 或 mapping。

## 小结

通过这一篇，我们把 OpenClaw 主动化体系剩下的两块讲完了：

1. **Webhook**：在 `hooks` 配置里 `enabled: true` + 显式 token 之后，Gateway 在 `127.0.0.1:18789` 暴露三个入口 —— `/hooks/wake` 走主会话、`/hooks/agent` 起一次 isolated turn、`/hooks/<name>` 走自定义 mapping；
2. **Mapped hooks**：通过 `hooks.mappings` 把任意 payload 经 `messageTemplate` 渲染后转成 agent turn；
3. **Standing Orders**：写在 workspace 的 `AGENTS.md` 里，**任何 session 启动时**（包括用户聊天、cron、webhook、heartbeat）都会被注入到 system prompt；推荐的职责块模板包含 Authority / Trigger / Approval gate / Escalation 四块；
4. **三者组合**：standing orders 定义授权与边界，cron 定义触发时间，webhook 接外部事件，三者职责清晰、互不耦合；

到这里小龙虾已经能按表干活、能被外部系统唤起、能在每个 session 里都记得自己应当遵守哪些职责块。但仔细翻 OpenClaw 的文档，我们还能看到 **Background Tasks**（后台任务）和 **Task Flow**（多步骤工作流编排）这两种不同的任务机制，我们下一篇就来继续学习它们。

## 参考

* [OpenClaw 官方文档](https://docs.openclaw.ai/)
* [OpenClaw GitHub 仓库](https://github.com/openclaw/openclaw)
* [Automation & Tasks 总索引](https://docs.openclaw.ai/automation)
* [Webhooks 文档（在 cron-jobs 内）](https://docs.openclaw.ai/automation/cron-jobs#webhooks)
* [Standing Orders 官方文档](https://docs.openclaw.ai/automation/standing-orders)
* [Hooks（生命周期）官方文档](https://docs.openclaw.ai/automation/hooks)
* [Gmail PubSub 集成](https://docs.openclaw.ai/automation/gmail-pubsub)
* [Agent Workspace 概念](https://docs.openclaw.ai/concepts/agent-workspace)
* [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)
* [GitHub Webhook events: release](https://docs.github.com/en/webhooks/webhook-events-and-payloads#release)
* [ngrok](https://ngrok.com/)
* [Tailscale Funnel 文档](https://tailscale.com/kb/1223/funnel)

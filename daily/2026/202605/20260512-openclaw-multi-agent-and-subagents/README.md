# 让小龙虾分身：多 Agent 路由与 Sub-agents

上一篇我们把 OpenClaw 的自动化体系拼齐了：Cron 调度时间、Heartbeat 周期觉察、Webhook 接外部事件、Standing Orders 圈定边界、Background Tasks 记账、Task Flow 编排。整套体系跑起来之后，小龙虾已经能按时间表干活、被外部事件唤起、所有后台动作都有据可查了。但如果再仔细看一眼就会发现，它到现在还是一个人在战斗 —— 所有消息都进同一个 agent，共用同一份记忆、同一份工具白名单、同一份 system prompt。

这种单 agent 的模式跑日常需求够用，可只要场景稍微复杂一点就开始捉襟见肘。最直观的痛点是工作和生活混在一起：白天我在公司飞书群里聊的是项目排期、代码 review、客户需求，晚上我在 Telegram 上聊的却是健身打卡、买菜清单、跟家人聊天。这两套上下文完全是两个频道的事，一旦汇到同一个会话里，agent 既不能按场景切换语气，记忆也跟着打架。今天我们就来看看 OpenClaw 是怎么把不同来源的消息分流到不同 agent 的，再顺带看看主 agent 怎么把活派给后台的子 agent 跑。这两套机制官方分别叫 **多 agent 路由（Multi-agent Routing）** 和 **Sub-agents**。

## 为什么需要多个 agent

为什么单 agent 不够用？我能想到三种典型场景，挨个说一下你大概就能体会到了。

第一种是 **工作和生活混用**。同一个人既要在公司飞书群里和同事讨论技术方案，又要在朋友的微信群里聊周末爬山。两边共用一个 agent，要么聊技术时它太活泼，要么聊生活时它太严肃，怎么调都顾此失彼。把工作群路由到一个严肃专业的 agent，朋友群路由到一个轻松点的 agent，这事儿就解决了。

第二种是 **对外服务和自家场景的隔离**。客户在微信上咨询产品，希望走一个带 RAG 的客服 agent，回答必须基于知识库、绝对不能动文件；自己在 Telegram 上私聊，则希望走一个全权限的助理，能改代码、能跑命令、能调内部 API。这两边的 system prompt、工具集、模型选型都不一样，硬塞到一个 agent 里只会两头不讨好。

第三种是 **模型按需匹配**。开发者频道里跑代码 review 想用 Opus 这种大模型，运营频道里答常见问题用便宜的 Sonnet 或 GPT-4o-mini 就够了。每个 agent 自带一份模型配置，用哪个 agent 自然就走哪个模型，按场景对上号，省得每条消息都手动指定一遍。

OpenClaw 把上面这些诉求都收敛到了同一个概念：**一个 agent 就是一份完整的人格作用域**。它有自己独立的工作目录、独立的认证信息、独立的模型清单、独立的会话历史。同一个 Gateway 进程里可以并存好几个 agent，互不干扰。

## 一个 agent 到底隔离了什么

照着官方文档 `docs/concepts/multi-agent.md` 里的定义，我们把隔离维度列一张表：

| 维度          | 说明                                                           |
| ----------- | ------------------------------------------------------------ |
| 工作目录        | 每个 agent 有自己的 workspace，里面装着 `AGENTS.md`、`SOUL.md`、`USER.md` 这些 bootstrap 文件 |
| 状态目录        | 也叫 `agentDir`，存这个 agent 自己的认证文件和模型注册表                |
| 会话存储        | 聊天历史和路由状态，落在 `~/.openclaw/agents/<agentId>/sessions` 目录下 |
| Skills      | 每个 workspace 自己加载一套 skill，可以叠加共享根目录下的公共 skill |
| 工具策略        | 工具白名单和黑名单可以按 agent 单独配                            |
| 沙箱          | 沙箱模式可以做到一个 agent 一个容器                              |
| 模型          | 每个 agent 可以挂不同的模型                                      |

表里的状态目录这一项还有个细节值得单独说一下。每个 agent 的认证档案具体落在 `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` 这个文件里，如果某个 agent 自己没有这份文件，OpenClaw 会自动去默认 agent 那边借一份顶上。这种"借用"对静态的 `api_key` / `token` 和 OAuth 都生效 —— **OAuth 凭据走的是穿透读取**，新 agent 默认就能复用主账号，不需要重新登录；token 过期时由其中一个 agent 持文件锁完成刷新，再写回默认 agent 的存档，其它 agent 在下次取用时自动拿到新值。OAuth 的 refresh token 不会被物理复制到新 agent 的目录，只是实现细节，不影响共享语义。只有当你确实想让某个 agent 走另一个账号时，才需要为它单独跑一次登录。

整套目录结构最后大致是这样：

```
~/.openclaw/
├── openclaw.json                       # 主配置文件
├── workspace/                          # 默认 agent 的工作区
├── workspace-work/                     # 工作 agent 的工作区
├── workspace-personal/                 # 私人 agent 的工作区
└── agents/
    ├── main/
    │   ├── agent/                      # auth-profiles.json + 模型注册
    │   └── sessions/                   # 会话 jsonl
    ├── work/
    │   ├── agent/
    │   └── sessions/
    └── personal/
        ├── agent/
        └── sessions/
```

可以看到每个 agent 都把自己的认证信息和会话记录关在了自己的 `agents/<agentId>/` 目录下，谁也不会去翻别人的家底。

## 创建新 agent 实例

下面我们动手把单 agent 的小龙虾改造成 3 个 agent：`main` 用来兜底，`work` 处理工作场景，`personal` 处理私人场景。

最省事的方式是用 OpenClaw 自带的 `openclaw agents add` 命令：

```bash
$ openclaw agents add work --workspace ~/.openclaw/workspace-work
$ openclaw agents add personal --workspace ~/.openclaw/workspace-personal \
    --model anthropic/claude-opus-4-6
```

命令执行结果如下：

![](./images/agents-add.png)

该命令会自动把 workspace 目录建好、把 `SOUL.md` / `AGENTS.md` / `USER.md` 这几份 bootstrap 文件写进去、把 `agents/<id>/agent` 状态目录和 sessions 目录都拉起来，再把对应的 `agents.list[]` 段追加到 `openclaw.json` 里。

打开 `openclaw.json` 配置文件，可以看到 `agents` 下多了一个 `list` 列表：

```json5
{
  "agents": {
    "defaults": {
      // 默认值，所有 agent 复用
    },
    "list": [
      {
        "id": "main"
      },
      {
        "id": "work",
        "name": "work",
        "workspace": "~/.openclaw/workspace-work",
        "agentDir": "~/.openclaw/agents/work/agent"
      },
      {
        "id": "personal",
        "name": "personal",
        "workspace": "~/.openclaw/workspace-personal",
        "agentDir": "~/.openclaw/agents/personal/agent"
      }
    ],
  },
}
```

> 其中 `agentDir` 这一项尤其要小心：**绝对不能在多个 agent 之间复用同一个目录**，复用会导致认证信息互相覆盖、会话串号。每个 agent 都应该有自己独立的 `agentDir`，路径里带上 agent id 是个好习惯。另外，值得提一句的是，`workspace` 工作目录只是软隔离，**并不是硬沙箱**，它只是个默认的工作目录，工具拿到相对路径会落在这里，但绝对路径仍然能访问主机其它位置。要做硬隔离得开 sandbox，这个我们留到下一篇讲。

新 agent 创建成功后，我们可以使用下面的命令测试一下：

```
$ openclaw agent --message "你是谁" --agent work
```

运行结果如下：

![](./images/agent-message.png)

可以看到，这个 agent 是全新的，还没有孵化过，你可以在 TUI 中和其进行对话，完成初始设置，比如给 work agent 设定工作场景的语气（专业、简洁、不开玩笑），personal agent 则可以写得轻松点。

## 把消息路由到对的 agent

agent 都建好了，但 OpenClaw 默认还是会把所有消息都送到 `default: true` 标的那个 agent 上。要让消息按来源分流，得给每个非默认 agent 配一条对应的路由规则，告诉 OpenClaw 哪个频道、哪个账号、哪个群该走哪个 agent。

和 agent 创建一样，最省事的方式是直接用 `openclaw agents bind` 命令：

```bash
$ openclaw agents bind --agent work --bind feishu:default
$ openclaw agents bind --agent personal --bind telegram
```

第一条把飞书+默认账号的所有消息绑到 `work` agent，第二条把 Telegram 频道绑定到 `personal`，执行完回头看 `openclaw.json`，会发现多了一段 `bindings` 数组：

```json5
{
  // ... 上面的 agents 段保持不变 ...

  "bindings": [
    {
      "type": "route",
      "agentId": "work",
      "match": {
        "channel": "feishu",
        "accountId": "default"
      }
    },
    {
      "type": "route",
      "agentId": "personal",
      "match": {
        "channel": "telegram"
      }
    }
  ]
}
```

每条规则的核心就是 `agentId` + `match` 这一对：消息进来之后，OpenClaw 会拿 `match` 里的字段挨个去对，全部对上才把消息送给对应的 agent；一条规则都没对上的，兜底到默认 agent。

写完之后重启 Gateway 让配置生效，然后再到飞书或 Telegram 里对话：

![](./images/telegram.png)

一个全新的 ”老钳“ 就上线了。

> `openclaw agents bind --bind <channel[:accountId]>` 这种命令行形式只覆盖到"频道 + 账号"这一层。如果你想做更细粒度的匹配，比如把某个特定的飞书群单独路由到 `work`，或者按 DM 发件人 ID 拆分，还得直接编辑 `bindings` 数组。比如下面这条按群 ID 把工作群单独绑到 `work` 的规则：
>
> ```json5
> {
>   "agentId": "work",
>   "match": {
>     "channel": "feishu",
>     "peer": { "kind": "group", "id": "oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxx" },
>   },
> }
> ```

## 从命令行手动触发 agent 轮次

前面创建 work agent 之后，我们顺手用 `openclaw agent --message "你是谁" --agent work` 给它发了条消息，我们这一节详细介绍下这个命令。它绕过路由规则直接把消息塞到指定 agent 的会话里，跑完之后把回复打印到终端，日常排查单个 agent 行为的时候特别方便。

之前那次只是用了它最简单的形态，下面把常用 flag 一并展开看一下：

| Flag                | 含义                                          |
| ------------------- | ------------------------------------------- |
| `--message <text>`  | 这次轮次的初始 prompt（必填）                |
| `--agent <id>`      | 锁定到某个 agent，用它的主会话                |
| `--session-id <id>` | 直接复用一个已有的会话 key                   |
| `--channel`         | **入站**频道，不填则用主会话所在的频道，同时也是默认的出站频道 |
| `--to <dest>`       | **入站**目标（手机号、chat id），用来推导会话 key |
| `--deliver`         | 把回复推到聊天频道，不只打印到终端           |
| `--reply-channel`   | 覆盖**出站**频道（whatsapp / telegram / discord / slack ...） |
| `--reply-to`        | 覆盖**出站**目标（手机号、频道 ID）             |
| `--local`           | 默认情况下 CLI 会走 Gateway 中转，加 `--local` 会强制改用本机内嵌的 runtime；如果 Gateway 不可达，CLI 也会自动 fallback 到 local 模式       |
| `--json`            | 结构化 JSON 输出                              |

这里面 `--channel` / `--to` 和 `--reply-channel` / `--reply-to` 看着很像，实际是**两个方向**的事：

* **`--channel` + `--to`** 决定**入站会话**。OpenClaw 会拿 `<channel> + <to>` 拼出一个会话 key（形如 `whatsapp:+8613800001234`），把这条消息塞进那个会话里跑。它们决定 agent 用谁的视角说话、加载谁的历史。
* **`--reply-channel` + `--reply-to`** 决定**出站去向**。默认情况下加 `--deliver` 之后，回复会原路回到入站对应的频道和目标；只有当你想让出站和入站**不一致**时，才需要这两个 flag 显式覆盖。

绝大多数场景里入站和出站是同一边（用户从飞书发消息进来，回复也回到飞书），完全用不到 `--reply-*`；只有没有真正入站消息的场景，比如 cron 定时触发生成、或者从命令行起一轮然后把结果推到固定播报频道，才需要显式声明出站去哪儿。

下面是两种用法的示例：

```
# 1. 只声明入站，出站走默认 —— 模拟从 Telegram 渠道发来消息，回复原路返回
$ openclaw agent --agent personal --channel telegram --to "71123456789" \
    --message "我的快递到哪了" --deliver

# 2. 不带入站，出站显式声明 —— cron 触发 work agent 生成周报，结果推到 Telegram 的 work 群
$ openclaw agent --agent work --message "总结这周的工作情况" \
    --deliver --reply-channel telegram --reply-to "-5000412345"
```

第一条只声明了入站（`--to` + `--channel`），出站走默认，回复自动回到 Telegram 上，根本不用设置 `--reply-*`；第二条反过来，没有入站消息，OpenClaw 推不出默认的回复目标，所以必须用 `--reply-channel` + `--reply-to` 显式告诉它推到 Telegram 的指定群。

总的来说，`openclaw agent` 既能给人手动用，也能丢到 cron 里跑，本质上就是一个从命令行触发 agent 轮次的小工具。

## 让 agent 自己派活给子 agent

如果说 `openclaw agent` 是**从外面**起一次 agent 轮次，那么 sub-agents 这套玩法就是**从里面**派：主 agent 跑到一半，自己决定把某个子任务派给一个后台的子 agent 去跑，跑完结果再回流到主 agent 这边。这件事就是 `sessions_spawn` 这个工具干的。

### 怎么跑起来

子 agent 是从已有的 agent 轮次派生出来的**后台**轮次。它在自己的会话里跑（会话 key 形如 `agent:<agentId>:subagent:<uuid>`），跑完之后通过 announce 步骤把结果 push 回请求者所在的聊天里。每一次子 agent 的运行也会被记成一条 background task，也就是上一篇讲的 `subagent` 这种 runtime。

主 agent 派活给子 agent 的整体时序大致是这样：

![](./images/subagents.png)

这里要特别注意一点：`sessions_spawn` 是 **非阻塞** 的，调用之后会立刻返回 `{ status: "accepted", runId, childSessionKey }`，而不会等子任务跑完。官方文档里特别强调：完成是 push 模式的，不要在主 agent 里写一个 `sessions_list` 加 `exec sleep` 的死循环去等结果，子任务跑完之后会自己冒泡上来。

我们在 main 会话里测试一下：

![](./images/subagents-test.png)

可以看到 main 会话成功调用了 `sessions_spawn` 工具，并且立即收到了返回结果：

```json
{
  "status": "accepted",
  "childSessionKey": "agent:main:subagent:f9c4eec1-3b88-4e87-b095-eac7a9d8beb9",
  "runId": "897aee90-735e-447a-b99e-a859f39ad995",
  "mode": "run",
  "note": "Auto-announce is push-based. After spawning children, do NOT call sessions_list, sessions_history, exec sleep, or any polling tool. Track expected child session keys. If any required child completion has not arrived yet, call sessions_yield to end the turn and wait for completion events as user messages. Only send your final answer after ALL expected completions arrive. If a child completion event arrives AFTER your final answer, reply ONLY with NO_REPLY.",
  "modelApplied": true
}
```

此时，我们在 main 会话里并没有阻塞，还可以正常进行其他对话。过了一会，等子 agent 完成了任务，结果会被 push 回 main 会话中：

![](./images/subagents-test-2.png)

### 几个关键参数

`sessions_spawn` 的常用参数列在下面：

| 参数                 | 含义                                                   |
| ------------------- | ---------------------------------------------------- |
| `task`              | 子任务描述（必填）                                            |
| `agentId`           | 派给哪个 agent，默认为空，就是请求者自己                                 |
| `model`             | 覆盖子任务的模型，给重活配便宜模型时常用                                 |
| `thinking`          | 覆盖子任务的 thinking 等级                                   |
| `runTimeoutSeconds` | 子任务超时秒数，0 表示不超时                                      |
| `context`           | `isolated`（默认）或 `fork`                              |
| `runtime`           | 子任务跑在哪种运行时上：`subagent`（默认，内置子 agent runtime）或 `acp`（走 ACP 协议接外部 agent runtime） |
| `sandbox`           | `inherit` 或 `require`，后者强制要求子运行时在沙箱里跑 |

其中 `context` 这个参数挺有意思：

* **`isolated`**（默认）：开一份干净的子会话记录，token 成本低。文档里强烈推荐用这个，把任务在 `task` 字段里讲清楚直接派出去
* **`fork`**：把当前整段会话记录分支到子会话里，子任务能继承所有上下文，但 token 成本翻倍。**只在子任务确实需要当前对话的细微上下文时才用**，不是写不清楚 task 文本时的替代品

另外要记住的是，`sessions_spawn` 本身**不接受**任何投递参数（`target` / `channel` / `to` 这些都不能传）。要让子 agent 把结果 deliver 到某个具体频道，得让它自己在轮次里调用 `message` 或者 `sessions_send` 这类工具。

### 用 `allowAgents` 限制派给谁

默认情况下，子 agent 只能派给 **请求者自己这一个 agent**。如果你希望主 agent 能把活派给别的 agent（比如把客服任务派给 support agent），就得显式打开 `subagents.allowAgents` 这一项：

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "subagents": {
          "allowAgents": ["main", "personal", "work"]
        }
      }
    ]
  }
}
```

`allowAgents` 这个数组里也可以写 `["*"]` 表示允许任意 agent。这里有个小细节要注意：**如果你写了非空列表又想让主 agent 派任务给自己，必须把 `"main"` 显式列在里面**，不会自动包含。

## 小结

通过这一篇，我们把 OpenClaw 的多 agent 体系整个走了一遍：

1. **为什么单 agent 不够用** —— 工作和生活混用、对外服务和自家场景混用、不同任务想配不同模型，这些都是单 agent 的痛点；
2. **一个 agent 隔离了什么** —— 工作目录、`agentDir`、会话历史、认证、工具、沙箱、模型，全都按 agent 一份一份独立维护；
3. **怎么创建 agent** —— 通过 `openclaw agents add` 命令一行搞定 workspace、bootstrap 文件、状态目录、会话目录，并自动完成 `openclaw.json` 的配置；
4. **怎么按来源分流消息** —— 通过 `openclaw agents bind` 命令为非默认 agent 配一条路由规则，核心是 `agentId` + `match` 对，匹配越具体优先级越高，没匹配到就兜底到默认 agent；
5. **怎么从命令行与 agent 对话** —— `openclaw agent` 的参数分两组：`--channel` / `--to` 决定**入站会话**，`--reply-channel` / `--reply-to` 决定**出站去向**，加上 `--deliver` 才会真把回复推到聊天频道；
6. **让 agent 自己派活给后台子 agent** —— 主 agent 跑到一半调用 `sessions_spawn` 把任务派出去，非阻塞，子任务在独立会话里跑，跑完通过 announce 步骤推回。

到这里，小龙虾已经能在多个频道上以不同人格运行，agent 之间也能互相派活了。但 Gateway 本身仍然跑在一台机器上，所有 agent 共享一个进程。如果我希望从办公室的 Mac 远程连到家里的 Gateway 服务器、或者把某些不可信的 agent 关进 Docker 沙箱里跑，又该怎么做呢？我们下一篇就来看看 OpenClaw 的 Sandbox 和远程访问。

## 参考

* [OpenClaw 官方文档](https://docs.openclaw.ai/)
* [OpenClaw GitHub 仓库](https://github.com/openclaw/openclaw)
* [Multi-agent routing 官方文档](https://docs.openclaw.ai/concepts/multi-agent)
* [Agent runtime 官方文档](https://docs.openclaw.ai/concepts/agent)
* [Agent workspace 官方文档](https://docs.openclaw.ai/concepts/agent-workspace)
* [Channel routing 官方文档](https://docs.openclaw.ai/channels/channel-routing)
* [Agent send 官方文档](https://docs.openclaw.ai/tools/agent-send)
* [Sub-agents 官方文档](https://docs.openclaw.ai/tools/subagents)
* [Multi-agent sandbox tools 官方文档](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools)
* [Background tasks 官方文档](https://docs.openclaw.ai/automation/tasks)

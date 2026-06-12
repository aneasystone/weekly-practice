# 画布节点类型（`-t`）— 索引

本目录按 **画布节点 `type`** 拆成独立文件；每个文件只写**该类型特有**的说明（生成器参数、属性参数、特殊用法）。**通用约定**（`--prompt` / `-s` vs `-u` 对比 / 连线 / `--run`）**统一在本页维护**，各 type 文件**链接**回来，避免复读。

## 类型索引

| 类型             | 文档                             | `libtv node -t` 新建 | `libtv node` 更新 `params`         | `libtv node --run` |
| ---------------- | -------------------------------- | -------------------- | ---------------------------------- | ------------------ |
| **`text`**       | [text.md](./text.md)             | 是                   | 是                                 | 是                 |
| **`image`**      | [image.md](./image.md)           | 是                   | 是                                 | 是                 |
| **`video`**      | [video.md](./video.md)           | 是                   | 是                                 | 是                 |
| **`audio`**      | [audio.md](./audio.md)           | 是                   | 是                                 | 是                 |
| **`script`**     | [script.md](./script.md)         | 是                   | 是                                 | 是                 |
| **`storyboard`** | [storyboard.md](./storyboard.md) | 是                   | 是                                 | 是                 |
| **`video-clip`** | [video-clip.md](./video-clip.md) | 是                   | 是（浅合并，无生成器 schema 校验） | 是                 |

画布上仍可能存在但 **CLI 不支持**的类型：**`custom`** / **`group`** 等——创建 / 更新 / 运行均勿走 [`libtv node`](../commands/node.md)；分组改用 [`libtv group`](../commands/group.md)；[`libtv model search --type <type>`](../commands/model.md) 也只接受上表中**带生成模型**的六个类型（`text` / `image` / `video` / `audio` / `script` / `storyboard`）。

## 查模型与 schema

| 命令                                        | 用途                                                                                                                         |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **`libtv model search --type <node-type>`** | 列出该类型当前环境可用的 **`modelKey`** 与展示名；无关键字即「列出全部」（详见 [commands/model.md](../commands/model.md)）。 |
| **`libtv model search <keyword>`**          | 按关键词检索（不分大小写子串匹配）；可叠加 `--type`。                                                                        |
| **`libtv model <modelKey>`**                | 对 `modelKey` / `modelName` **全等**匹配后输出完整 **`schema`** JSON，对照写 `-s/--set`。                                    |

**`schema` 各块释义**（`properties` / `config` / `rules` / `modeType`）：[../model-schema/schema.md](../model-schema/schema.md)。

## `-s/--set` vs `-u/--update`（权威对比）

> 两者都是 `key=value`（首个 `=` 拆分，值支持 `true/false/数字/JSON`），但**落地位置完全不同**，**不能互换**。**展示名永远走 [`--name`](../commands/node.md)**（`-u name=…` 会被拒绝）。

| 维度         | **`-s, --set`**                                                                                                                                                     | **`-u, --update`**                                                                       |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 写入位置     | **`data.params.*`**                                                                                                                                                 | **`data.*`**（**不含** `params`）                                                        |
| 语义         | **生成器参数** —— 模型这次**怎么生成**（`prompt` / `model` / `count` / `settings` / `advancedSettings` / `modeType` …）                                             | **节点自身属性** —— 节点本体承载的**内容**（`content` / `rows` / …），**不影响**模型参数 |
| schema 校验  | 严格：按当前 `modelKey` 的 `properties` / `config` / `rules` 校验；**`originalField`** 自动归位到 `params.settings` / `params.advancedSettings`；`count` 超范围报错 | 不走生成器 schema；仅**白名单式键名拒写**（见下）并按 JSON 浅写到 `data` 顶层            |
| 触发 `--run` | 是                                                                                                                                                                  | 是                                                                                       |
| 典型写法     | `-s prompt=...` / `-s model=nebula-ultra` / `-s ratio=16:9` / `-s count=2` / `-s settings.quality=2K`（或拍平 `-s quality=2K`）                                     | `-u content='["Hello"]'` / `-u rows='[{...}]'` / `-u title="..."`                        |

### `-u` 明确拒写的键

| 键                                                                       | 替代                                                                                                               |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| **`params`**                                                             | 用 **`-s / --set`** 或 **`--prompt`**                                                                              |
| **`name` / `label`**                                                     | 用 **`--name <text>`**（仅 [默认子命令 `libtv node <node>`](../commands/node.md) 生效；label 同步时会归一为 name） |
| **`type`**                                                               | 节点类型**不可**通过 CLI 变更                                                                                      |
| **`action` / `taskInfo` / `prevTaskInfo` / `generatorType` / `isStale`** | 由画布 / 任务链路维护，**不可**手写                                                                                |

> 经验法则：**「会让模型输出不同结果的 → `-s`；只是改节点里放什么（文本 / 行等内容）→ `-u`」。展示名永远走 `--name`**。

### `-s` 的拍平规则

若 key 属于当前模型 schema 中 `config.settings` / `config.advancedSettings` 的字段（含 **`originalField`** 别名），CLI 会**自动写入**对应的 `params.settings` / `params.advancedSettings`。推荐 **`-s ratio=16:9`**、**`-s quality=2K`** 这类逐键拍平写法。

## 各类型 `-u` 典型可写 `data` 顶层字段（速查）

> 白名单**不**硬编码；下表列出当前各节点 `data` 类型定义里**常用于 CLI 编辑**的字段。完整字段以 `packages_tv/libtv-cli/src/canvas-node/<type>/node-data.ts` 为准；未列字段在不违反上面「`-u` 拒写键」的前提下也能写入，但可能被下游消费忽略。

| 类型                    | 常用 `-u` 键                                                                                                                                                                                 |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text`                  | **`content`**（`string[]`）                                                                                                                                                                  |
| `image`                 | **`rotateAngle`**、**`alt`**、**`showGenerator`**、**`url`**、**`originalUrl`**、**`scriptRowHiddenUuid`**                                                                                   |
| `video`                 | **`url`**、**`poster`**、**`scriptRowHiddenUuid`**                                                                                                                                           |
| `audio`                 | **`url`**（其它属性以 `node-data.ts` 为准，多为上传 / 任务链路写入）                                                                                                                         |
| `script` / `storyboard` | **`rows`**、**`title`**、**`viewMode`**（`table` \| `creative`）、**`shotColumns`**、**`activeViewId`**、**`sourceType`**、**`scriptModel`**、**`linkedImageGroupId`**、**`imageGenConfig`** |
| `video-clip`            | **`cropRange`**、**`clipTimelineData`**、**`saveToNodeOnComplete`**、**`url`**、**`poster`**                                                                                                 |

## 文档内模型示例来源

下文中 **`modelKey`** 与 **`libtv model <modelKey>`** 输出抽样采自 **2026-04-14** 对默认环境执行 [`libtv model search --type …`](../commands/model.md) / `libtv model …` 的结果；线上列表会变更，以你本机实时命令为准。

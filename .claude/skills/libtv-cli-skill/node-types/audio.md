# 节点类型：`audio` — 音频 / 语音生成节点

## 整体节点用途

**音频 / 语音生成节点**：按模型能力产出**配音、BGM、纯乐器**等音频。大部分音频模型 `schema` **没有** `modeType.items`，入边 / 媒体条数不由该结构表达，而由 `rules` 与画布连接规则决定。常见相邻节点：上游 `text`（作为文案）；下游 `video` / `video-clip`（合成驱动）。

**通用约定**：[README.md](./README.md)。**`schema` 各块含义**：[../model-schema/schema.md](../model-schema/schema.md)。

## 案例

见 [../examples/node-types/audio.md](../examples/node-types/audio.md)。

## 常见生成器参数（`-s / --set`）

写入 **`data.params`**；落在 `config.advancedSettings` / `config.settings` 的字段可**拍平**写顶层。写入嵌套对象时，`params.advancedSettings` / `params.settings` 的键一般为 schema 的 **`originalField`**，缺省为字段名（与 `libtv model <modelKey>` 的 `properties.*` 一致）。

| 字段                                | 说明                                                                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`prompt`**                        | 文案或描述（按模型而定）。                                                                                                                                    |
| **`model`**                         | 音频模型 **`modelKey`**（如 `vocal-v3`、`vocal-music`、`mureka-8`）。                                                                                         |
| **`scene`**                         | 业务场景 / 子模式字符串（`schema` 顶层 `scene` / `sceneName` 提示用途）。若模型默认带 `scene`，新建时 CLI 按 schema 填初始值，更新时 `--set scene=…` 可覆盖。 |
| **`count`**                         | 条数。                                                                                                                                                        |
| **`settings` / `advancedSettings`** | 模型表单字段分桶；键集合随 `modelKey` 变化，务必对照 `libtv model <modelKey>` 输出。                                                                          |

### 抽样：`vocal-v3`（`libtv model vocal-v3`）

`config.advancedSettings`: `["voice", "stability"]`（**无** `config.settings` 列表）。

| schema 字段            | 写入位置                                       | `-s / --set` 写法                           | 备注                                       |
| ---------------------- | ---------------------------------------------- | ------------------------------------------- | ------------------------------------------ |
| `properties.voice`     | `params.advancedSettings.voice_id`             | `voice=…` 或 `voice_id=…`                   | `originalField: voice_id`。                |
| `properties.stability` | `params.advancedSettings.stability`            | `stability=0 / 0.5 / 1`                     | 默认 `0.5`。                               |
| `properties.duration`  | `params` **顶层**（未列入 `advancedSettings`） | `duration=60000` 或 `music_length_ms=60000` | `originalField: music_length_ms`（毫秒）。 |

### 抽样：`vocal-music`（`libtv model vocal-music`）

- `config.advancedSettings`: `["duration"]`。
- **`duration`** → **`music_length_ms`**（毫秒枚举如 **`30000`**、**`60000`**）。

### 抽样：`mureka-8`（`libtv model mureka-8`）

- `config.advancedSettings`: `["instrumental"]`。
- **`instrumental`**（展示名「纯乐器」）→ **`params.advancedSettings.force_instrumental`**（**`originalField`: `force_instrumental`**，switch 默认 **`1`**）。

## 常见属性参数（`-u / --update`）

`audio` 节点 `data` 顶层以**上传 / 任务链路**写入为主；`node-data.ts` 只定义了 `url`（`string[]`）等少量字段。日常需要人工改时，几乎都是：

| 想改的东西                                            | 正确入口                                         |
| ----------------------------------------------------- | ------------------------------------------------ |
| `prompt` / `model` / `voice` / `stability` 等生成相关 | `-s / --set`（写 `data.params`）                 |
| 展示名                                                | `--name`（等价于 `-u name=…`，但禁用 `-u name`） |

若确需手工改 `data.url` 等，对照 `packages_tv/libtv-cli/src/canvas-node/audio/node-data.ts` 写即可（不违反 [README.md](./README.md) 的「`-u` 明确拒写的键」）。

## 特殊用法

- **列出 / 查询音频模型**：`libtv model search --type audio`、`libtv model <modelKey>`（见 [../commands/model.md](../commands/model.md)）。
- 音频模型通常用 `rules` 约束「至少要 `prompt`」或其它组合；能否生成以 `libtv model <modelKey>` 输出为准。

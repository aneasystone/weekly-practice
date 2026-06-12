# 节点类型：`script` — 脚本（剧情 / 结构化文本工作流）节点

## 整体节点用途

**脚本节点**：承载**剧情 / 结构化文本工作流**，节点本体是一张「分镜表」（`data.rows`、列元数据、视图模式等），也可按所选模型直接生成一张或多张结构化行。与 [`storyboard`](./storyboard.md) **共用同一套生成器数据结构**（`data.type` 恒为 `script`，React Flow `type` 区分）。

**通用约定**：[README.md](./README.md)。**`schema` 各块含义**：[../model-schema/schema.md](../model-schema/schema.md)（文本侧同 [text.md](./text.md)，配图侧同 [image.md](./image.md)）。

## 案例

见 [../examples/node-types/script.md](../examples/node-types/script.md)。

## 常见生成器参数（`-s / --set`）

写入 **`data.params`**，走所选 `modelKey` 的 schema 校验。`model` 必须在 **`scriptText`** 维度的 support 列表中；若改图片配图侧使用，则用 `scriptImage` 维度的图片模型。

| 字段                                | 说明                                                                             |
| ----------------------------------- | -------------------------------------------------------------------------------- |
| **`prompt`**                        | 主提示。                                                                         |
| **`model`**                         | `scriptText` 侧 **`modelKey`**（剧情 / 结构化文本）；配图侧见下。                |
| **`count`**                         | 生成次数 / 条数，须在模型允许范围内。                                            |
| **`scene`**                         | 脚本业务场景；新建默认常为 **`script-generate`**；其它取值以 schema / 产品为准。 |
| **`settings` / `advancedSettings`** | 是否存在分桶、有哪些键，**完全由该 `modelKey` 的 schema 决定**。                 |

### `scriptText` 模型（如 `aurora-3-prime`）

`libtv model aurora-3-prime` 抽样：`config` 中**无** `settings` / `advancedSettings` 列表；主要为 `properties.modeType`（多模态槽位）与 `rules`（常要求 `prompt`）。`--set modeType=…` 等与 [text.md](./text.md) 相同思路。

### `scriptImage` 模型（如 `nebula-ultra`）

[`libtv model search --type script`](../commands/model.md) 里 `scriptImage` 下列出的实为**图片**模型；其 `settings` / `advancedSettings` 与 [image.md](./image.md) 中 `nebula-ultra` 表一致（`quality`、`ratio`、`searchable` 等），`--set` 亦可拍平。

## 常见属性参数（`-u / --update`）

写入 **`data`** 顶层，**不**经生成器 schema 校验——这是改「分镜表数据」的主要入口。

| 键                       | 类型                                      | 说明                                                                                                                           |
| ------------------------ | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **`rows`**               | `StoryboardRowCli[]`                      | 分镜行数据（`id` / `shotNumber` / `plotDescription` / `characters` / `shotSize` / `dialogue` / `imageGenerationPrompt` / …）。 |
| **`title`**              | `string`                                  | 脚本 / 分镜标题。                                                                                                              |
| **`viewMode`**           | `'table' \| 'creative'`                   | 视图模式。                                                                                                                     |
| **`shotColumns`**        | `ShotColumnMetaCli[]`                     | 自定义列元数据。                                                                                                               |
| **`activeViewId`**       | `string`                                  | 当前激活视图 id。                                                                                                              |
| **`sourceType`**         | `'text' \| 'video' \| 'image' \| 'mixed'` | 来源类型。                                                                                                                     |
| **`scriptModel`**        | `string`                                  | 脚本生成时使用的模型记录（**非**下次生成的 `params.model`）。                                                                  |
| **`linkedImageGroupId`** | `string`                                  | 关联的图片分组 id。                                                                                                            |
| **`imageGenConfig`**     | `ScriptImageGenConfigCli`                 | 图片生成配置快照。                                                                                                             |

> 生成参数（`prompt` / `model` / `count` / `scene`）请用 `-s`；展示名用 `--name`。

## 特殊用法

- **上游为参考图**：把 `image` 资源节点连到 `script` 节点左侧后 `--run`，可用作分镜生成的参考素材（上游类型与条数约束见 `scriptText` 侧 schema）。
- **生成分镜图组**：脚本节点已有分镜行后，用 [`libtv script storyboard <脚本>`](../commands/script.md) 对齐画布「生成分镜」——在右侧新建分镜图组、按行派生 `image` 子节点并逐张 run。分镜图模型 / 参数取自脚本节点 `imageGenConfig`，可用 `-s` 覆盖（如 `-s model=seedream-4 -s aspectRatio=16:9`）。
- **列出 / 查询脚本模型**：`libtv model search --type script`（同时返回 `scriptText` 与 `scriptImage` 两套）；`libtv model <modelKey>`。详见 [../commands/model.md](../commands/model.md)。
- 分镜行批量写入的典型流水线：见 [../examples/node-types/script.md](../examples/node-types/script.md)。

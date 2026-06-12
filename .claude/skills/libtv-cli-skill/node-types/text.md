# 节点类型：`text` — 文本生成节点

## 整体节点用途

**文本生成节点**：把「提示词 + 模型」产出一段或多段文本（结果写回 `data.content`），常作为**剧情 / 旁白 / 结构化说明**等的入口，也可做上游是图片 / 视频的多模态「图→文 / 视频→文」。典型边：上游常为 `image` / `video` 资源节点（`image2text` / `video2text` 模态）；下游常为 `script` / `storyboard` / `image` 节点。

**通用约定**（`-s` vs `-u`、`--name`、连线、`--run`）：[README.md](./README.md)。**`schema` 各块含义**：[../model-schema/schema.md](../model-schema/schema.md)（文本侧 `image2text` / `video2text` 见 §2.4）。

## 案例

见 [../examples/node-types/text.md](../examples/node-types/text.md)。

## 常见生成器参数（`-s / --set`）

写入 **`data.params`**，走所选 `modelKey` 的 schema 校验。典型键：

| 字段                                | 说明                                                                                                                                                             |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`prompt`**                        | 提示全文（等价于 `--prompt`，后者会覆盖 `-s prompt=…`）。                                                                                                        |
| **`model`**                         | **文本模型 `modelKey`**（如 `aurora-3-prime`）。字段集以 [`libtv model <modelKey>`](../commands/model.md) 输出为准。                                             |
| **`count`**                         | 生成条数，需符合当前模型 schema。                                                                                                                                |
| **`modeType`**                      | 多模态槽位选择（如 `image2text` / `video2text`）；取值见 `schema.properties.modeType.items`。                                                                    |
| **`settings` / `advancedSettings`** | 若 `libtv model <modelKey>` 的 `config` 未声明分桶列表，该模型通常**没有**表单分桶字段，仅 `properties` 顶层能力（如 `modeType`）与 `rules`。`-s` 可拍平写顶层。 |

### 抽样：`aurora-3-prime` / `qwen-3-vl-flash`

- `config`：**无** `settings` / `advancedSettings` 数组。
- `properties.modeType.items`：如 **`image2text`**、**`video2text`** 等多模态槽位；需要时用 `--set modeType=image2text`（枚举以 schema 为准）。
- `rules`：常见要求 **`prompt`** 非空。

## 常见属性参数（`-u / --update`）

写入 **`data`** 顶层，**不**经生成器 schema 校验。

| 键            | 类型       | 说明                                                       |
| ------------- | ---------- | ---------------------------------------------------------- |
| **`content`** | `string[]` | 节点展示的文本条目（例如生成结果写回；手工编辑也走此键）。 |

> 生成参数（`prompt` / `model` / `count` 等）请用 `-s`；展示名请用 `--name`——`-u name=…` 会被拒绝，详见 [README.md](./README.md) 的「`-u` 明确拒写的键」。

## 特殊用法

- 把 `text` 节点**连到 `image` 的左侧**后触发 `--run`，可作为图片模型的提示词来源（见 [../commands/node.md](../commands/node.md) 中默认子命令的 `--left` / `--right` 说明）。
- 若所选文本模型在 `config` 中后续增加 `settings` / `advancedSettings`，按 `-s 字段名=值` 拍平即可；以实时 `libtv model <modelKey>` 输出为准。
- 列出 / 查询文本模型：`libtv model search --type text`、`libtv model <modelKey>`（见 [../commands/model.md](../commands/model.md)）。

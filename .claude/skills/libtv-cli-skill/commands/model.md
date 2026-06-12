# `libtv model` — 生成模型检索与 schema

在写 [`libtv node -s model=…`](./node.md) / [`libtv node create -s model=…`](./node.md) 之前，用 **`search`** 在 supportModels 中找候选；用**默认子命令** `libtv model <name...>` 对 **`modelKey` / `modelName`** 全等解析，拉取完整 **`tool_spec`** schema（与画布侧 `getModelSchema` 同源）。

数据来源：在线 supportModels 配置（带本地缓存）；拿不到时行为以实现为准。**`schema` 各块含义**（`properties` / `config` / `rules` / `modeType`）：[../model-schema/schema.md](../model-schema/schema.md)。

本命令调接口，**需已登录**（[`libtv login`](./login.md)）。

## 子命令

| 子命令                              | 作用                                                                                   |
| ----------------------------------- | -------------------------------------------------------------------------------------- |
| **`libtv model search [name...]`**  | 在 supportModels 内检索候选；可选 `--type` 限定节点类型；无 `name` 时需配合 `--type`。 |
| **（默认）`libtv model <name...>`** | 对 `modelKey`/`modelName` **trim 后全等** 匹配并输出完整 schema JSON。                 |

### `libtv model search [name...]`

用法骨架：`libtv model search [name...] [flags]`

**位置参数**

- **`[name...]`**（可省略）：检索关键词；shell 里多词会拼成一段再检索。**不能**与不传 `--type` 同时省略，否则会报错。

**选项**

| 选项                     | 必填 | 说明                                                                                                                                                                                   |
| ------------------------ | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-t, --type <node-type>` | 否   | 画布节点类型枚举，取值：`text` / `image` / `video` / `audio` / `script` / `storyboard`。`script` / `storyboard` 会同时扫 `scriptText` 与 `scriptImage` 两类模态。**不支持** `custom`。 |
| `--help`                 | 否   | 打印该子命令帮助。                                                                                                                                                                     |

**匹配规则**（在已选模态列表内，`query` 为 trim 后整段关键词）：

| 输入                             | 行为                     | `matchKind`     |
| -------------------------------- | ------------------------ | --------------- |
| `modelKey` 与 `query` 全等       | 只返回这些命中           | `modelKey`      |
| `modelName` 不区分大小写子串包含 | 退而求其次的子串匹配     | `modelName`     |
| 仅 `--type`、无 `name`           | 返回该类型下**全部**条目 | `all` 或 `none` |
| 无 `--type` 且无 `name`          | 报错（必须至少传一个）   | —               |

**输出**：stdout JSON，含 `query` / `matchKind` / `matches`；有 `--type` 时还含 `nodeType`。

### `libtv model <name...>`（默认子命令）

用法骨架：`libtv model <name...>`

**位置参数**

- **`<name...>`**（必填）：模型 **id（`modelKey`）** 或**展示名（`modelName`）**；多词会拼成一段。

**行为**：对 supportModels + `/api/tool_spec/list` 的记录做 `modelKey` / `modelName` **trim 后全等**解析。

| 情况                                                | 结果                                                                                                                    |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 唯一命中                                            | stdout JSON，含 `nameOrId` / `modelName` / `modelKey` / `toolKey` / `modality` / `schema`（完整字段、类型、可选值等）。 |
| supportModels 阶段**全等匹配到多个不同 `modelKey`** | 返回 **409** 类错误，需改用唯一 `modelKey`。                                                                            |

## 示例

```bash
# case 1: 按关键词检索（不分大小写子串匹配）
libtv model search qwen

# case 2: 缩小到 image 模态下的 qwen
libtv model search --type image qwen

# case 3: 列出某节点类型下所有可用模型（无关键字；这是 `list` 的正确写法）
libtv model search --type image
libtv model search --type script   # 会同时覆盖 scriptText 与 scriptImage

# case 4: 全字匹配 modelKey，拉出完整 schema（常用于在写 -s/--set 之前参考）
libtv model qwen-3-vl-flash

# case 5: 展示名含空格时用引号
libtv model "某展示名含空格"

# case 6: 串接 jq 速查某字段（以 settings 列表为例）
libtv model nebula-ultra | jq '.schema.config.settings'
```

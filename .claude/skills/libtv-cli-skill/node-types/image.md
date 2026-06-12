# 节点类型：`image` — 图片生成节点

## 整体节点用途

**图片生成节点**：既可做**文生图**（无上游参考图），也可做**图生图 / 参考图**（上游若干张 `image` 资源节点）。画布上的 `image` 节点同时承担「展示产物 / 承载 URL」这一身份，因此**生成参数**（`-s`）与**节点自身属性**（`-u`）都很常用。常见相邻节点：上游 `image` / `text`；下游 `image` / `video` / `storyboard` / `video-clip`。

**通用约定**：[README.md](./README.md)。**`schema` 各块含义**（`properties` / `config` / `rules` / `modeType`）：[../model-schema/schema.md](../model-schema/schema.md)。

## 案例

见 [../examples/node-types/image.md](../examples/node-types/image.md)。

## 常见生成器参数（`-s / --set`）

写入 **`data.params`**，走所选 `modelKey` 的 schema 校验；schema 标在 `config.settings` / `config.advancedSettings` 的字段可**拍平**写顶层（CLI 会按 schema 自动归位）。

| 字段                   | 说明                                                                         |
| ---------------------- | ---------------------------------------------------------------------------- |
| **`prompt`**           | 提示词。                                                                     |
| **`model`**            | 图片模型 **`modelKey`**。                                                    |
| **`count`**            | 出图张数；允许值由 schema 的 `properties.count` 决定。                       |
| **`settings`**         | 表单「基础设置」的键集合，见 `libtv model <modelKey>` 的 `config.settings`。 |
| **`advancedSettings`** | 「高级设置」的键集合，见 `config.advancedSettings`。                         |

### 抽样：`nebula-ultra`（`libtv model nebula-ultra`）

| Schema 字段      | 落入桶             | 写入 `params.*` 的键（`originalField` 缺省同字段名） | 取值提示                                            |
| ---------------- | ------------------ | ---------------------------------------------------- | --------------------------------------------------- |
| **`quality`**    | `settings`         | **`quality`**                                        | `1K` / `2K` / `4K`（默认 **`2K`**）                 |
| **`ratio`**      | `settings`         | **`ratio`**                                          | `auto`、`1:1`、`16:9`、`9:16` 等（默认 **`16:9`**） |
| **`searchable`** | `advancedSettings` | **`searchable`**                                     | 联网开关，switch，默认 **`1`**                      |

其它（如 `fineTuneType` / `fineTuneModels` / `magicList` / `focusRegion` / `originImage` / `scene` / `cameraControl`）是否在 `settings` 桶内，以各模型 `libtv model <modelKey>` 输出为准；未进桶的写在 `params` 顶层。`rules` 可能要求 **`prompt`** 或 **`media`**（参考图入边）。

## 常见属性参数（`-u / --update`）

写入 **`data`** 顶层，**不**经生成器 schema 校验。

| 键                            | 类型       | 说明                                                       |
| ----------------------------- | ---------- | ---------------------------------------------------------- |
| **`rotateAngle`**             | `number`   | 旋转角度。                                                 |
| **`alt`**                     | `string`   | 文本替代说明。                                             |
| **`showGenerator`**           | `boolean`  | 是否展示生成器面板。                                       |
| **`url`** / **`originalUrl`** | `string[]` | 图片 URL / 原始 URL（一般由生成 / 上传写入，手工改谨慎）。 |
| **`scriptRowHiddenUuid`**     | `string`   | 与脚本 / 分镜行的关联 UUID。                               |

> 生成参数（`prompt` / `model` / `ratio` / `quality` 等）请用 `-s`；展示名用 `--name`——`-u name=…` 会被拒绝，见 [README.md](./README.md) 的「`-u` 明确拒写的键」。

## 特殊用法

- **图生图 / 参考图**：先用 [`libtv upload`](../commands/upload.md) 建 `image` 资源节点，再用 [`libtv node <本节点> --left <资源节点>`](../commands/node.md) 或管道把上游连到本节点左侧；入边数量约束见 schema 的 `modeType.items`（如 `image2image: [0,7]`）。
- **图片工具栏 Slash 快捷**：画布里图片节点工具栏的**九宫格**与生成器 `/` 面板，在 CLI 侧对应 [`libtv image shortcut`](../commands/image.md)：先 `libtv image shortcut list` 抄 `scene` / `label`，再 `libtv image shortcut <scene|label> -n <源图节点>`。`gridType ∈ {4,9,16,25}` 走**原地改图**，其它走**右侧新建节点**（入边 = 源节点）。
- **列出 / 查询图片模型**：`libtv model search --type image`、`libtv model <modelKey>`（见 [../commands/model.md](../commands/model.md)）。

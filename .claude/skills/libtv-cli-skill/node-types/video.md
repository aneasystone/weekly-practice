# 节点类型：`video` — 视频生成节点

## 整体节点用途

**视频生成节点**：按当前模型的 `modeType`（文生 / 单图生 / 首尾帧 / 多图参考 / 视频参考 / 音频驱动 / 全能参考 等）产出一条或多条视频；节点本体也承载最终视频 URL 与封面。常见相邻节点：上游 `image` / `video` / `audio` 资源节点；下游 `video-clip`、`script` / `storyboard` 的配图行等。

**通用约定**：[README.md](./README.md)。**`schema` 各块含义** 与 `modeType.items` / `rules` 逻辑：[../model-schema/schema.md](../model-schema/schema.md)（§2 / §4）。

## 案例

见 [../examples/node-types/video.md](../examples/node-types/video.md)（以 Seedance 2.0 `star-video2` 为例）。

## 常见生成器参数（`-s / --set`）

写入 **`data.params`**；schema 标在 `settings` / `advancedSettings` 的字段可拍平写顶层。

| 字段                                | 说明                                                                                       |
| ----------------------------------- | ------------------------------------------------------------------------------------------ |
| **`prompt`**                        | 提示词。                                                                                   |
| **`model`**                         | 视频模型 **`modelKey`**。                                                                  |
| **`modeType`**                      | 生成模式；可选键见当前模型的 `schema.properties.modeType.items`（见下表常见枚举）。        |
| **`count`**                         | 条数，需符合 schema。                                                                      |
| **`settings` / `advancedSettings`** | 与模型表单项对应；`-s` 直接写字段名，由 CLI 写入对应嵌套对象（缺省键名同 schema 字段名）。 |

### `modeType` 常见枚举

| 枚举值                  | 文案             |
| ----------------------- | ---------------- |
| **`text2video`**        | 文生视频（默认） |
| **`singleImage2video`** | 图生视频         |
| **`frames2video`**      | 首尾帧           |
| **`image2video`**       | 图片参考         |
| **`video2video`**       | 视频参考         |
| **`videoEdit2video`**   | 视频编辑         |
| **`audio2video`**       | 音频驱动         |
| **`mixed2video`**       | 全能参考         |

> 不同模型支持哪些 `modeType`、每种下 `settings` / `advancedSettings` 的字段集合**完全由该模型 schema 决定**；以 `libtv model <modelKey>` 输出为准。

### 抽样：Seedance 2.0（`star-video2`，`libtv model star-video2`）

本模型的 `config.settings` 为固定列表（**不**随 `modeType` 拆多套字段；其它 `modelKey` 可能不同）：

| 拍平键               | 落入桶             | 写入 `params.*` 的键（`originalField` 缺省同字段名） | 取值提示                                                                                |
| -------------------- | ------------------ | ---------------------------------------------------- | --------------------------------------------------------------------------------------- |
| **`ratio`**          | `settings`         | **`ratio`**                                          | `adaptive`（展示 Auto）、`16:9`、`4:3`、`1:1`、`3:4`、`9:16`、`21:9`（默认 **`16:9`**） |
| **`resolution`**     | `settings`         | **`resolution`**                                     | **`480p`** / **`720p`**（默认 **`720p`**）                                              |
| **`duration`**       | `settings`         | **`duration`**                                       | 整数秒 **4–15**（默认 **`5`**）                                                         |
| **`enableSound`**    | `settings`         | **`enableSound`**                                    | **`on`** / **`off`**（默认 **`on`**）                                                   |
| **`search_enabled`** | `advancedSettings` | **`search_enabled`**                                 | 联网开关，switch，默认 **`1`**                                                          |

## 常见属性参数（`-u / --update`）

写入 **`data`** 顶层，**不**经生成器 schema 校验。

| 键                        | 类型       | 说明                                            |
| ------------------------- | ---------- | ----------------------------------------------- |
| **`url`**                 | `string[]` | 视频 URL（一般由生成 / 上传写入，手工改谨慎）。 |
| **`poster`**              | `string`   | 封面图 URL。                                    |
| **`scriptRowHiddenUuid`** | `string`   | 与脚本 / 分镜行的关联 UUID。                    |

> 生成参数（`modeType` / `ratio` / `duration` / …）请用 `-s`；展示名用 `--name`。

## 特殊用法

- **参考图 / 参考视频 / 音频驱动**：先用 [`libtv upload`](../commands/upload.md) 建对应资源节点，再以 `--left` 或管道连到本节点左侧；允许的**类型与条数**由当前 `modeType` 下的 `modeType.items[modeType]` 与 `mixed2videoConfig` 等共同约束（见 [../model-schema/schema.md §2](../model-schema/schema.md)）。
- **列出 / 查询视频模型**：`libtv model search --type video`、`libtv model <modelKey>`（见 [../commands/model.md](../commands/model.md)）。

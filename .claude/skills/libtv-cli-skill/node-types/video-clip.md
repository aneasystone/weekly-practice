# 节点类型：`video-clip` — 视频合成（时间线 / 剪辑类）节点

## 整体节点用途

**视频合成节点**：把若干 `video` / `audio` 等上游素材按时间线组合成一条视频。**核心编辑对象在 `data` 顶层**（而非 `params`）——**`cropRange` / `clipTimelineData` / `saveToNodeOnComplete` / `url` / `poster`** 等。本节点**不**走「`model` + `tool_spec`」schema 校验，CLI 对 `params` 做 **JSON patch 式浅合并**；`--run` 走视频合成任务链路，与 `text` / `image` 等选 `modelKey` 拉 schema 的流程不同。

**通用约定**：[README.md](./README.md)。其它节点涉及的 **`schema` 各块释义**：[../model-schema/schema.md](../model-schema/schema.md)。

## 案例

见 [../examples/node-types/video-clip.md](../examples/node-types/video-clip.md)。

## 常见生成器参数（`-s / --set`）

写入 **`data.params`**，**不**做生成器 schema 校验；具体可填键以网页合成面板为准。新建默认 `params` 为 **`{}`**，展示名位置参数为「视频合成」或用户自定义。

> 本类型 **没有统一「全站」字段表**；若产品后续为 `video-clip` 增加表单字段，可先 `libtv node "<显示名>"`（仅查询）打出节点 JSON，对照网页 / 接口文档再填 `-s`。

## 常见属性参数（`-u / --update`）

写入 **`data`** 顶层，**不**经生成器 schema 校验——本类型的核心写入入口。

| 键                         | 类型                            | 说明                                                                                                                     |
| -------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **`cropRange`**            | `[number, number]`              | 裁剪区间（秒）。                                                                                                         |
| **`clipTimelineData`**     | `SerializedClipTimelineDataCli` | 时间线序列化数据（`videoSourceNodeIds` / `audioSourceNodeIds` / `clips` / `totalDuration` / `scale` / `cropRange` 等）。 |
| **`saveToNodeOnComplete`** | `boolean`                       | 合成完成时是否回写节点。                                                                                                 |
| **`url`** / **`poster`**   | `string[]` / `string`           | 合成产物 URL / 封面（一般由任务链路写入）。                                                                              |

> 展示名用 `--name`；`-u name=…` 会被拒绝。完整 `-s` vs `-u` 区分见 [README.md](./README.md)。

## 特殊用法

- **不在 `libtv model` 的节点类型范围**：`libtv model search --type video-clip` 会被拒绝——`video-clip` 不在可选 `--type` 枚举（`text` / `image` / `video` / `audio` / `script` / `storyboard`）内，见 [../commands/model.md](../commands/model.md)。
- **上游素材**：先用 [`libtv upload`](../commands/upload.md) 或 `libtv node create -t video/audio ...` 建资源节点，再用 `libtv node --left/--left-add` 或管道连到本节点的左侧；再把这些素材节点的 id 写进 `clipTimelineData.videoSourceNodeIds` / `audioSourceNodeIds`。
- **`--run`**：在 `data` 顶层时间线数据就位后触发合成，任务进度与结果约定见 [../examples/pipes/README.md](../examples/pipes/README.md)。

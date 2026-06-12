# 节点类型：`storyboard` — 分镜表节点

## 整体节点用途

**分镜表节点**：画布上以「行 + 列 + 视图模式」组织镜头信息；与 [`script`](./script.md) **共用一套生成器数据结构**——`data.type` 恒为 **`script`**，React Flow `type` 为 **`storyboard`**。因此 CLI 改参、校验、`--run` 与脚本节点同一套路：`model` 仍须落在 **`scriptText`** support 里；[`libtv model search --type storyboard`](../commands/model.md) 返回的是 `scriptText` + `scriptImage` 两组模型。

**通用约定**：[README.md](./README.md)。**`schema` 各块含义**：[../model-schema/schema.md](../model-schema/schema.md)（与 [script.md](./script.md) 一致）。

## 案例

见 [../examples/node-types/storyboard.md](../examples/node-types/storyboard.md)。

## 常见生成器参数（`-s / --set`）

与 [script.md](./script.md) 的「常见生成器参数（`-s / --set`）」一致：**`prompt`**、**`model`**、**`count`**、**`scene`**、**`settings` / `advancedSettings`**。

- 若 `model` 来自 **`scriptText`** 列表，多数模型 schema **无**分桶字段。
- 若使用 **`scriptImage`** 里的图片模型，则分桶字段与 [image.md](./image.md) 的图片 `settings` / `advancedSettings` 一致，`--set` 可拍平逻辑字段名。

## 常见属性参数（`-u / --update`）

与 [script.md](./script.md) 的「常见属性参数（`-u / --update`）」一致（两者共用 `ScriptNodeDataCli`，`data.type` 恒为 `script`）：`rows` / `title` / `viewMode` / `shotColumns` / `activeViewId` / `sourceType` / `scriptModel` / `linkedImageGroupId` / `imageGenConfig`。

## 特殊用法

- **从 `script` 节点派生到 `storyboard`**：两者数据结构相同，常见做法是先用 `script` 生成剧情结构，再用 `storyboard` 做镜头层视图展示；两节点间的连线与数据同步行为以画布实现为准（不在 `libtv node` 的直接能力范围内）。
- **列出 / 查询可用模型**：`libtv model search --type storyboard`（等价于 `script`）；对具体 `modelKey` 查完整 schema：`libtv model <modelKey>`。详见 [../commands/model.md](../commands/model.md)。

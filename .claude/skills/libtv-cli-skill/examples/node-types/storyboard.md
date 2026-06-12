# `storyboard` — 分镜表节点

**覆盖**：建分镜节点、连上游「剧情 / script」、触发生成，以及用 `-u` 直接维护 `rows` / `title` / `viewMode`。字段语义以 [`../../node-types/storyboard.md`](../../node-types/storyboard.md) 为准；与 [`script`](./script.md) 共用 `rows` 结构。

**前置条件**：同 [../README.md 的通用前置条件](../README.md#通用前置条件)；画布上已有节点「上游剧情」（`script` 或 `text` 节点均可）。

```bash
# 1) 建节点 + 设置生成参数
libtv node "分镜1" -t storyboard --prompt "按镜头列点描述" \
  --set model=aurora-3-prime

# 2) 连上游并触发生成
libtv node "分镜1" --left 上游剧情 --run

# 3) 只改表元数据（-u 走 data 顶层）
libtv node "分镜1" -u title="第一幕" -u viewMode=table
libtv node "分镜1" -u rows='[{"shotNumber":1,"plotDescription":"开场：雨夜街道"}]'
```

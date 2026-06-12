# `script` — 脚本（剧情）节点

**覆盖**：建剧本节点、连上游（参考图 / 资料）再触发生成、用 `-u` 直接写 `rows` / `title` / `viewMode`。字段语义以 [`../../node-types/script.md`](../../node-types/script.md) 为准。

**前置条件**：同 [../README.md 的通用前置条件](../README.md#通用前置条件)；画布上已有节点「参考图」。

```bash
# 1) 建节点 + 设置生成参数
libtv node "剧本" -t script --prompt "三幕结构，主角是一名侦探" \
  --set model=aurora-3-prime \
  --set count=1

# 2) 连上游参考并触发一次生成
libtv node "剧本" --left 参考图 --run

# 3) 只改节点自身分镜表（-u 走 data 顶层、不经生成器 schema）
libtv node "剧本" -u title="侦探第一幕" -u viewMode=table
libtv node "剧本" -u rows='[{"shotNumber":1,"plotDescription":"开场：雨夜街道"}]'
```

关键点：

- `script` 与 [`storyboard`](./storyboard.md) 在 CLI 上共享 `rows` / `title` / `viewMode` 等字段语义；区别主要在后端业务分类与上下游语义。
- `-u rows='[…]'` 接受 JSON 字符串，CLI 内部会解析；深层字段（如 `rows[0].plotDescription`）目前必须整块赋值。

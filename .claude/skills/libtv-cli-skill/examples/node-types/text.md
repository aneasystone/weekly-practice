# `text` — 文本节点

**覆盖**：建节点 / 改生成参数 / 回写内容 / 改显示名。字段语义与取值范围以 [`../../node-types/text.md`](../../node-types/text.md) 为准。

**前置条件**：同 [../README.md 的通用前置条件](../README.md#通用前置条件)。

```bash
# 1) 建节点 + 设置提示词 / 模型 / 条数
libtv node "旁白" -t text --prompt "写一段自嘲的独白" \
  --set model=aurora-3-prime \
  --set count=1

# 2) 把生成结果回写到节点自身内容（不会触发模型重跑；走 -u）
libtv node "旁白" -u content='["你好世界","第二段"]'

# 3) 改展示名（展示名永远走 --name，等价 -u name=…）
libtv node "旁白" --name "主角独白"
```

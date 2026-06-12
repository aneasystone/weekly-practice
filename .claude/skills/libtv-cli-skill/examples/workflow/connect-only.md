# 工作流：只连线不改参（确保 / 增量 add / rm）

**覆盖**：`--left` / `--left-add` / `--left-rm` 三种用法，以及 stdin 串联上游。连线语义见 [../../commands/node.md](../../commands/node.md)。

**前置条件**：同 [README.md 的通用前置条件](../README.md#通用前置条件)；画布上已有节点「参考图 A」「参考图 B」「参考图 C」「剧情」。

```bash
# case A: 确保「剧情」的入边**就是**这 2 条（缺则补、多则剪）
libtv node "剧情" --left 参考图A --left 参考图B

# case B: 追加一条入边，不动其它入边
libtv node "剧情" --left-add 参考图C

# case C: 移除一条入边，保留其余
libtv node "剧情" --left-rm 参考图A

# case D: 上游来自 stdin（把 `libtv node "参考图A"` 的 nodeKey 喂给下游）
libtv node "参考图A" | libtv node "剧情"
```

关键点：

- `--left / --left-add / --left-rm` 的值可以是**显示名**或 `nodeKey`，只要在当前范围内唯一。
- **同时**出现 `--left` 与 `--left-add` / `--left-rm` 会被拒绝（同一次命令里只允许一种模式）。
- 仅改入边、不触发生成；要触发请加 `--run`。

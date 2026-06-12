# 工作流：一条命令建节点 + 连上游 + 触发生成

**覆盖**：`libtv node create` 把「建节点 / 改参数 / 连上游 / 触发生成」合并为一步，等价于顺序跑 [`create-and-run.md`](./create-and-run.md) 的 2–4 步。

**前置条件**：同 [README.md 的通用前置条件](../README.md#通用前置条件)；画布上已存在显示名为「参考图」的上游节点。

```bash
libtv node create -t text --name 剧情 \
  --prompt "根据参考图写一段分镜旁白" \
  --set model=aurora-3-prime \
  --left 参考图 \
  --run
```

关键点：

- `--name <显示名>` 是**可选**——不传时后端自动命名；传了就写进 `data.name`。
- `--left <上游>` 的值接受**显示名**或 `nodeKey`（只要在当前项目 / 分组范围内唯一）。
- `--run` 建完后立即触发生成；省略则仅建节点、不触发。

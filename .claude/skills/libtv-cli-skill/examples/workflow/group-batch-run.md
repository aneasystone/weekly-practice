# 工作流：建分组 → 绑定若干子节点 → 整组执行

**覆盖**：`libtv group create` / `libtv group use` / `libtv group <group> --node …` / `libtv group <group> --run` 的组合。普通分组语义见 [../../commands/group.md](../../commands/group.md)。

**前置条件**：同 [README.md 的通用前置条件](../README.md#通用前置条件)；画布已有节点「镜头 A」「镜头 B」「镜头 C」。

```bash
# 1) 建普通分组并把工作目录绑定到它（省去后续 -g）
libtv group create 首集分镜 | libtv group use -r

# 2) 把 3 个子节点绑到该分组（也可以创建节点时用 -g 直接落入）
libtv group 首集分镜 --node 镜头A --node 镜头B --node 镜头C

# 3) 查看分组内节点
libtv group 首集分镜 --list

# 4) 整组触发生成
libtv group 首集分镜 --run
```

关键点：

- `libtv group use -r` 中的 `-r` 读取上游 stdin 的 **`nodeKey`** 并写入 `.libtv/project.json` 的 `groupNodeKey`。
- 绑定到分组后，后续 `libtv node`（未显式 `-g` / `-p`）默认限定在该分组内。
- 清除分组绑定：`libtv group unuse`；清除项目绑定：`libtv project unuse`。
